#!/usr/bin/env python3
import argparse, json
from pathlib import Path

ap=argparse.ArgumentParser(description='Append one measured UI-replica iteration to the ledger.')
ap.add_argument('--ledger', default='.ui-replica/iteration-ledger.json')
ap.add_argument('--observed', action='append', default=[])
ap.add_argument('--hypothesis', action='append', default=[])
ap.add_argument('--file', action='append', default=[])
ap.add_argument('--score-before', type=float)
ap.add_argument('--score-after', type=float)
ap.add_argument('--decision', choices=['keep','revise','rollback'], required=True)
ap.add_argument('--note')
args=ap.parse_args()
p=Path(args.ledger); p.parent.mkdir(parents=True, exist_ok=True)
try: data=json.loads(p.read_text()) if p.exists() else []
except Exception: data=[]
entry={
  'iteration': len(data)+1,
  'observed': args.observed,
  'hypothesis': args.hypothesis,
  'files_changed': args.file,
  'score_before': args.score_before,
  'score_after': args.score_after,
  'decision': args.decision,
  'note': args.note,
}
data.append(entry)
p.write_text(json.dumps(data, indent=2), encoding='utf-8')
print(json.dumps(entry, indent=2))
