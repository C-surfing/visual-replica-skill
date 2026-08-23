#!/usr/bin/env python3
import argparse, json, math
from collections import deque
from pathlib import Path
import numpy as np
from PIL import Image, ImageChops, ImageEnhance, ImageFilter, ImageDraw


def load_rgb(path):
    return Image.open(path).convert('RGB')


def np_rgb(img):
    return np.asarray(img).astype(np.float32)


def gray_np(img):
    return np.asarray(img.convert('L')).astype(np.float32) / 255.0


def edge_map(img):
    edge_img = img.convert('L').filter(ImageFilter.FIND_EDGES)
    arr = np.asarray(edge_img).astype(np.float32) / 255.0
    # Suppress tiny raster noise while preserving UI boundaries.
    arr = np.clip((arr - 0.04) / 0.96, 0, 1)
    return arr, edge_img


def safe_ssim(a, b):
    try:
        from skimage.metrics import structural_similarity
        return float(structural_similarity(
            np.asarray(a.convert('L')),
            np.asarray(b.convert('L')),
            data_range=255,
        ))
    except Exception:
        return None


def estimate_translation(ref, cand):
    """Approximate whole-image translation using phase correlation.

    Returns the shift that best aligns candidate to reference. Positive dx means
    candidate should move right; positive dy means candidate should move down.
    """
    a = gray_np(ref)
    b = gray_np(cand)
    # Downsample very large screenshots for speed and robustness.
    max_side = max(a.shape)
    scale = 1.0
    if max_side > 1200:
        scale = 1200.0 / max_side
        size = (max(32, int(ref.width * scale)), max(32, int(ref.height * scale)))
        a = gray_np(ref.resize(size, Image.Resampling.BILINEAR))
        b = gray_np(cand.resize(size, Image.Resampling.BILINEAR))

    a = a - a.mean()
    b = b - b.mean()
    fa = np.fft.fft2(a)
    fb = np.fft.fft2(b)
    cross = fa * np.conj(fb)
    denom = np.abs(cross)
    cross /= np.where(denom < 1e-9, 1.0, denom)
    corr = np.abs(np.fft.ifft2(cross))
    y, x = np.unravel_index(np.argmax(corr), corr.shape)
    h, w = corr.shape
    if x > w // 2:
        x -= w
    if y > h // 2:
        y -= h
    # This correlation convention yields the shift to apply to candidate.
    dx = float(x / scale)
    dy = float(y / scale)
    peak = float(corr.max())
    return {'dx': dx, 'dy': dy, 'confidence_peak': peak}


def metrics(ref, cand, threshold):
    a, b = np_rgb(ref), np_rgb(cand)
    absd = np.abs(a - b)
    err = absd.mean(axis=2) / 255.0
    per_pixel_max = absd.max(axis=2)
    changed = per_pixel_max > threshold

    mae = float(err.mean())
    changed_ratio = float(changed.mean())
    pixel_similarity = float(1.0 - mae)

    ea, _ = edge_map(ref)
    eb, _ = edge_map(cand)
    edge_similarity = float(np.clip(1.0 - np.abs(ea - eb).mean(), 0, 1))

    weights = 1.0 + 4.0 * np.maximum(ea, eb)
    edge_weighted_error = float((err * weights).sum() / weights.sum())
    edge_weighted_similarity = float(np.clip(1.0 - edge_weighted_error, 0, 1))

    ssim = safe_ssim(ref, cand)

    # Image-only composite. Typography/asset/state still need semantic review.
    parts = [
        (edge_similarity, 0.30),
        (edge_weighted_similarity, 0.30),
        (pixel_similarity, 0.20),
    ]
    if ssim is not None:
        parts.append((ssim, 0.20))
    else:
        total = sum(w for _, w in parts)
        parts = [(v, w / total) for v, w in parts]
    composite = float(sum(v * w for v, w in parts))

    return {
        'changed_pixel_ratio': changed_ratio,
        'mae_normalized': mae,
        'pixel_similarity': pixel_similarity,
        'edge_similarity': edge_similarity,
        'edge_weighted_similarity': edge_weighted_similarity,
        'ssim': ssim,
        'image_composite': composite,
    }


def multiscale_metrics(ref, cand, threshold):
    scales = [0.25, 0.5, 1.0]
    result = []
    for s in scales:
        if s == 1.0:
            rr, cc = ref, cand
        else:
            size = (max(8, round(ref.width * s)), max(8, round(ref.height * s)))
            rr = ref.resize(size, Image.Resampling.LANCZOS)
            cc = cand.resize(size, Image.Resampling.LANCZOS)
        m = metrics(rr, cc, threshold)
        result.append({'scale': s, 'size': rr.size, 'metrics': m})
    return result


def connected_hotspots(ref, cand, threshold=16, block=4, top_n=8, min_blocks=2):
    a, b = np_rgb(ref), np_rgb(cand)
    err = np.abs(a - b).max(axis=2)
    h, w = err.shape
    bh = math.ceil(h / block)
    bw = math.ceil(w / block)
    coarse = np.zeros((bh, bw), dtype=bool)
    coarse_error = np.zeros((bh, bw), dtype=np.float32)

    for yy in range(bh):
        y0, y1 = yy * block, min(h, (yy + 1) * block)
        for xx in range(bw):
            x0, x1 = xx * block, min(w, (xx + 1) * block)
            cell = err[y0:y1, x0:x1]
            coarse[yy, xx] = float((cell > threshold).mean()) >= 0.20
            coarse_error[yy, xx] = float(cell.mean() / 255.0)

    seen = np.zeros_like(coarse, dtype=bool)
    comps = []
    for sy in range(bh):
        for sx in range(bw):
            if seen[sy, sx] or not coarse[sy, sx]:
                continue
            q = deque([(sy, sx)])
            seen[sy, sx] = True
            cells = []
            while q:
                y, x = q.popleft()
                cells.append((y, x))
                for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < bh and 0 <= nx < bw and coarse[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        q.append((ny, nx))
            if len(cells) < min_blocks:
                continue
            ys = [c[0] for c in cells]
            xs = [c[1] for c in cells]
            x0 = min(xs) * block
            y0 = min(ys) * block
            x1 = min(w, (max(xs) + 1) * block)
            y1 = min(h, (max(ys) + 1) * block)
            mean_err = float(np.mean([coarse_error[y,x] for y,x in cells]))
            area_ratio = ((x1-x0)*(y1-y0))/(w*h)
            impact = mean_err * area_ratio
            comps.append({
                'x': x0, 'y': y0, 'width': x1-x0, 'height': y1-y0,
                'area_ratio': float(area_ratio),
                'mean_error': mean_err,
                'impact': float(impact),
            })
    comps.sort(key=lambda c: c['impact'], reverse=True)
    return comps[:top_n]


def parse_regions(path):
    if not path:
        return []
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ('critical_regions', 'regions'):
            if isinstance(data.get(key), list):
                return data[key]
    raise ValueError('regions JSON must be a list or contain critical_regions/regions')


def crop_region(img, r):
    x, y = int(r['x']), int(r['y'])
    w, h = int(r['width']), int(r['height'])
    return img.crop((x, y, x+w, y+h))


def main():
    p = argparse.ArgumentParser(description='High-fidelity UI screenshot comparison.')
    p.add_argument('reference')
    p.add_argument('candidate')
    p.add_argument('--out-dir', default='.ui-replica/diff')
    p.add_argument('--pixel-threshold', type=int, default=16)
    p.add_argument('--regions-json')
    p.add_argument('--hotspot-block', type=int, default=4)
    p.add_argument('--top-hotspots', type=int, default=8)
    p.add_argument('--allow-resize', action='store_true', help='Diagnostic only. Never use resized metrics for acceptance.')
    args = p.parse_args()

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    ref = load_rgb(args.reference)
    cand_original = load_rgb(args.candidate)
    cand = cand_original
    resized = False

    if ref.size != cand.size:
        if not args.allow_resize:
            report = {
                'status': 'FAIL', 'reason': 'dimension_mismatch',
                'reference_size': ref.size, 'candidate_size': cand.size,
                'acceptance_allowed': False,
            }
            (out/'metrics.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
            print(json.dumps(report, indent=2))
            raise SystemExit(3)
        cand = cand.resize(ref.size, Image.Resampling.LANCZOS)
        resized = True

    global_m = metrics(ref, cand, args.pixel_threshold)
    scales = multiscale_metrics(ref, cand, args.pixel_threshold)
    shift = estimate_translation(ref, cand)
    hotspots = connected_hotspots(ref, cand, args.pixel_threshold, args.hotspot_block, args.top_hotspots)

    diff = ImageChops.difference(ref, cand)
    diff.save(out/'diff.png')
    ImageEnhance.Contrast(diff).enhance(4).save(out/'diff-amplified.png')

    ea, _ = edge_map(ref)
    eb, _ = edge_map(cand)
    edge_diff = Image.fromarray((np.abs(ea-eb)*255).clip(0,255).astype(np.uint8))
    edge_diff.save(out/'edge-diff.png')

    overlay = Image.blend(ref, cand, 0.5)
    overlay.save(out/'overlay.png')

    hotspot_img = overlay.copy()
    draw = ImageDraw.Draw(hotspot_img)
    for i, h in enumerate(hotspots, 1):
        box = (h['x'], h['y'], h['x']+h['width'], h['y']+h['height'])
        draw.rectangle(box, outline=(255, 0, 0), width=max(1, ref.width//400))
        draw.text((h['x']+3, h['y']+3), f'#{i}', fill=(255, 0, 0))
    hotspot_img.save(out/'hotspots.png')

    region_results = []
    for r in parse_regions(args.regions_json):
        rr, cc = crop_region(ref, r), crop_region(cand, r)
        if rr.width <= 0 or rr.height <= 0:
            continue
        region_results.append({
            'name': r.get('name', 'region'),
            'weight': float(r.get('weight', 1.0)),
            'critical': bool(r.get('critical', True)),
            'box': {k: int(r[k]) for k in ('x','y','width','height')},
            'metrics': metrics(rr, cc, args.pixel_threshold),
        })

    if region_results:
        tw = sum(r['weight'] for r in region_results)
        regional_composite = sum(r['metrics']['image_composite']*r['weight'] for r in region_results) / max(tw, 1e-9)
    else:
        regional_composite = None

    report = {
        'status': 'DIAGNOSTIC' if resized else 'OK',
        'acceptance_allowed': not resized,
        'reference_size': ref.size,
        'candidate_size_original': cand_original.size,
        'resized_for_diagnostic': resized,
        'pixel_threshold': args.pixel_threshold,
        'global': global_m,
        'multiscale': scales,
        'translation_to_align_candidate_to_reference_px': shift,
        'hotspots': hotspots,
        'regions': region_results,
        'regional_composite': regional_composite,
        'diagnostic_hints': [],
        'notes': [
            'image_composite is a progress signal, not proof of perceptual identity',
            'cross-OS/font/browser comparisons may contain irreducible rasterization noise',
            'translation estimate is diagnostic; never shift the screenshot post-capture for acceptance',
        ],
    }

    if abs(shift['dx']) >= 3 or abs(shift['dy']) >= 3:
        report['diagnostic_hints'].append('Meaningful global translation detected: inspect viewport/safe-area/shell/header before child offsets.')
    if hotspots and hotspots[0]['area_ratio'] > 0.08:
        report['diagnostic_hints'].append('Largest mismatch hotspot covers a substantial area: prioritize its root container before micro-polish.')
    if global_m['pixel_similarity'] > 0.95 and global_m['edge_similarity'] < 0.90:
        report['diagnostic_hints'].append('Color is broadly close but edge structure is weaker: prioritize geometry/alignment.')

    (out/'metrics.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
