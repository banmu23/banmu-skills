#!/usr/bin/env python3
"""Create a private workflow record without overwriting an existing one."""
import argparse,hashlib,json
from pathlib import Path

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--directory',required=True);a=p.parse_args()
 root=Path(a.directory).expanduser().resolve();root.mkdir(parents=True,exist_ok=True)
 source=Path(__file__).resolve().parents[1]
 data=json.loads((source/'references/run-template.json').read_text())
 data['workflow_sha256']=hashlib.sha256((source/'references/workflow.json').read_bytes()).hexdigest()
 profile=json.loads((source/'references/runtime-profile.json').read_text())
 data['plan']['audience']=profile.get('audience','customer')
 if data['plan']['audience']=='internal':
  data['plan']['owner_id']=profile['owner_id'];data['plan']['visual_family']=profile['preferred_family']
 target=root/'run.json'
 with target.open('x',encoding='utf-8') as f:f.write(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'created':str(target),'next':'填写实际方案、来源与证据，模板不能直接通过'},ensure_ascii=False))
if __name__=='__main__':main()
