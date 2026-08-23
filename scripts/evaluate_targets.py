#!/usr/bin/env python3
import argparse, json, subprocess, sys
from pathlib import Path

ap=argparse.ArgumentParser(description='Evaluate all reference/candidate targets from replica-config.json.')
ap.add_argument('--config', default='.ui-replica/replica-config.json')
ap.add_argument('--report', default='.ui-replica/fidelity-report.json')
args=ap.parse_args()
config_path=Path(args.config)
config=json.loads(config_path.read_text(encoding='utf-8'))
base=config_path.parent.parent if config_path.parent.name=='.ui-replica' else Path.cwd()
script=Path(__file__).with_name('compare.py')
ev=config.get('evaluation',{})
results=[]

for target in config.get('targets',[]):
    name=target.get('name','target')
    ref=Path(target['reference'])
    cand=Path(target['candidate'])
    if not ref.is_absolute(): ref=base/ref
    if not cand.is_absolute(): cand=base/cand
    out=base/'.ui-replica'/'diff'/name
    out.mkdir(parents=True,exist_ok=True)
    regions=target.get('critical_regions',[])
    regions_path=out/'regions.json'
    regions_path.write_text(json.dumps(regions,indent=2),encoding='utf-8')
    cmd=[sys.executable,str(script),str(ref),str(cand),'--out-dir',str(out),
         '--pixel-threshold',str(ev.get('pixel_threshold',16)),
         '--hotspot-block',str(ev.get('hotspot_block',4)),
         '--top-hotspots',str(ev.get('top_hotspots',8)),
         '--regions-json',str(regions_path)]
    proc=subprocess.run(cmd,text=True,capture_output=True)
    metrics_path=out/'metrics.json'
    if metrics_path.exists():
        data=json.loads(metrics_path.read_text(encoding='utf-8'))
    else:
        data={'status':'FAIL','reason':'compare_script_failed','stderr':proc.stderr[-3000:]}
    results.append({'name':name,'reference':str(ref),'candidate':str(cand),'result':data})

valid=[r for r in results if r['result'].get('global')]
avg=None
if valid:
    avg=sum(r['result']['global']['image_composite'] for r in valid)/len(valid)
worst_target=None
if valid:
    w=min(valid,key=lambda r:r['result']['global']['image_composite'])
    worst_target={'name':w['name'],'image_composite':w['result']['global']['image_composite']}

critical=[]
for r in valid:
    for reg in r['result'].get('regions',[]):
        if reg.get('critical',True):
            critical.append({'target':r['name'],'name':reg['name'],'score':reg['metrics']['image_composite']})
worst_region=min(critical,key=lambda x:x['score']) if critical else None

report={
    'status':'OK' if all(r['result'].get('status') in ('OK','DIAGNOSTIC') for r in results) else 'FAIL',
    'targets_evaluated':len(results),
    'average_image_composite':avg,
    'worst_target':worst_target,
    'worst_critical_region':worst_region,
    'targets':results,
    'notes':['Aggregate image scores are progress signals; acceptance still requires semantic review of typography, assets, state, and remaining hotspots.']
}
report_path=Path(args.report)
if not report_path.is_absolute(): report_path=base/report_path
report_path.parent.mkdir(parents=True,exist_ok=True)
report_path.write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
