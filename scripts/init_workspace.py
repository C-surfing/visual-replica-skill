#!/usr/bin/env python3
import argparse, json, shutil
from pathlib import Path

ap=argparse.ArgumentParser(description='Initialize .ui-replica working artifacts without touching application code.')
ap.add_argument('--root', default='.')
ap.add_argument('--force', action='store_true')
args=ap.parse_args()
project=Path(args.root).resolve(); skill=Path(__file__).resolve().parent.parent
work=project/'.ui-replica'
for d in ['reference','analysis','candidate','diff','crops','states']:
    (work/d).mkdir(parents=True,exist_ok=True)
for src_name,dst_name in [
    ('visual-spec.template.json','visual-spec.json'),
    ('replica-config.template.json','replica-config.json'),
    ('iteration-ledger.template.json','iteration-ledger.json'),
]:
    src=skill/'templates'/src_name; dst=work/dst_name
    if args.force or not dst.exists(): shutil.copyfile(src,dst)
print(work)
