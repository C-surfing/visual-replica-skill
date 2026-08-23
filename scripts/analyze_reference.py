#!/usr/bin/env python3
import argparse, json
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter, ImageDraw


def dominant_colors(img, n=10):
    small = img.convert('RGB').copy()
    small.thumbnail((512, 512))
    q = small.quantize(colors=n, method=Image.Quantize.MEDIANCUT)
    palette = q.getpalette()
    counts = q.getcolors() or []
    total = sum(c for c, _ in counts) or 1
    out = []
    for count, idx in sorted(counts, reverse=True):
        rgb = tuple(palette[idx*3:idx*3+3])
        out.append({'rgb': rgb, 'hex': '#%02x%02x%02x' % rgb, 'ratio': count/total})
    return out


def group_peaks(values, percentile=92, min_gap=3, max_peaks=18):
    vals = np.asarray(values, dtype=float)
    if vals.size == 0 or float(vals.max()) <= 1e-9:
        return []
    thresh = np.percentile(vals, percentile)
    idx = np.where(vals >= thresh)[0]
    if idx.size == 0:
        return []
    groups = []
    cur = [int(idx[0])]
    for i in idx[1:]:
        i = int(i)
        if i - cur[-1] <= min_gap:
            cur.append(i)
        else:
            groups.append(cur); cur = [i]
    groups.append(cur)
    scored = []
    for g in groups:
        center = int(round(np.average(g, weights=vals[g] + 1e-9)))
        score = float(vals[g].max() / (vals.max() + 1e-9))
        scored.append({'position': center, 'strength': score, 'band': [min(g), max(g)]})
    scored.sort(key=lambda x: x['strength'], reverse=True)
    return scored[:max_peaks]


def main():
    ap = argparse.ArgumentParser(description='Extract conservative visual evidence from a reference UI screenshot.')
    ap.add_argument('reference')
    ap.add_argument('--out-dir', default='.ui-replica/analysis')
    ap.add_argument('--colors', type=int, default=10)
    args = ap.parse_args()

    out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)
    img = Image.open(args.reference).convert('RGB')
    gray = img.convert('L')
    edges = gray.filter(ImageFilter.FIND_EDGES)
    e = np.asarray(edges).astype(np.float32) / 255.0

    # Ignore outermost raster border, which often dominates FIND_EDGES.
    if e.shape[0] > 4 and e.shape[1] > 4:
        e[:2,:] = e[-2:,:] = 0
        e[:,:2] = e[:,-2:] = 0

    vertical_projection = e.mean(axis=0)
    horizontal_projection = e.mean(axis=1)
    vpeaks = group_peaks(vertical_projection)
    hpeaks = group_peaks(horizontal_projection)

    analysis = {
        'reference': args.reference,
        'size': {'width': img.width, 'height': img.height},
        'aspect_ratio': img.width / max(img.height, 1),
        'dominant_colors': dominant_colors(img, args.colors),
        'edge_density': float((e > 0.12).mean()),
        'vertical_edge_peaks': vpeaks,
        'horizontal_edge_peaks': hpeaks,
        'notes': [
            'peaks are image-space evidence, not semantic component detections',
            'use repeated/strong peaks as candidate alignment anchors and verify visually',
        ],
    }
    (out/'reference-analysis.json').write_text(json.dumps(analysis, indent=2), encoding='utf-8')

    overlay = img.copy()
    draw = ImageDraw.Draw(overlay)
    width = max(1, img.width // 500)
    for p in vpeaks[:10]:
        x = p['position']; draw.line((x,0,x,img.height), fill=(255,0,0), width=width)
    for p in hpeaks[:10]:
        y = p['position']; draw.line((0,y,img.width,y), fill=(0,128,255), width=width)
    overlay.save(out/'reference-anchors.png')
    edges.save(out/'reference-edges.png')
    print(json.dumps(analysis, indent=2))

if __name__ == '__main__':
    main()
