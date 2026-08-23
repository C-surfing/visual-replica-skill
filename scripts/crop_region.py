#!/usr/bin/env python3
import argparse
from pathlib import Path
from PIL import Image

ap = argparse.ArgumentParser(description='Crop the same UI region from one or more screenshots.')
ap.add_argument('images', nargs='+')
ap.add_argument('--x', type=int, required=True)
ap.add_argument('--y', type=int, required=True)
ap.add_argument('--width', type=int, required=True)
ap.add_argument('--height', type=int, required=True)
ap.add_argument('--out-dir', default='.ui-replica/crops')
args = ap.parse_args()
out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)
box=(args.x,args.y,args.x+args.width,args.y+args.height)
for src in args.images:
    p=Path(src); img=Image.open(p)
    dest=out/f'{p.stem}-x{args.x}-y{args.y}-w{args.width}-h{args.height}.png'
    img.crop(box).save(dest)
    print(dest)
