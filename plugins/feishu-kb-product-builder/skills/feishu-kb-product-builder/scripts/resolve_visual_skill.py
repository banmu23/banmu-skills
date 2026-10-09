#!/usr/bin/env python3
"""Resolve the newest approved visual Skill inside the user's own role family."""
import argparse
import hashlib
import json
import re
from pathlib import Path

HERE=Path(__file__).resolve().parents[1]
class ResolutionError(ValueError): pass

def version_key(value):
    text=str(value).strip().strip('"\'')
    match=re.fullmatch(r'[vV]?(\d+)(?:\.(\d+))?(?:\.(\d+))?',text)
    if not match: raise ResolutionError('版本不明确，先核对真实 VERSION 或 metadata.version')
    return tuple(int(x or 0) for x in match.groups())

def inspect(candidate):
    p=Path(candidate['path']).expanduser().resolve()
    source=p/'SKILL.md'
    if not source.is_file(): raise ResolutionError('候选 Skill 缺少真实 SKILL.md')
    text=source.read_text(encoding='utf-8')
    front=text.split('---',2)[1] if text.startswith('---') else ''
    found=re.search(r'^name:\s*["\']?([^\n"\']+)',front,re.M)
    if not found: raise ResolutionError('候选缺少可核对的 Skill 名称')
    name=found.group(1).strip()
    if candidate.get('name') and candidate['name']!=name:
        raise ResolutionError('候选名称与实际 SKILL.md 不一致')
    if (p/'VERSION').is_file(): version=(p/'VERSION').read_text().strip()
    else:
        m=re.search(r'^\s+version:\s*["\']?([^\n"\']+)',front,re.M)
        if not m: raise ResolutionError('候选没有可核对的真实版本')
        version=m.group(1).strip()
    return {**candidate,'path':str(p),'name':name,'version':version,
            'rank':version_key(version),'skill_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'package_sha256':hashlib.sha256(json.dumps([(str(f.relative_to(p)),hashlib.sha256(f.read_bytes()).hexdigest()) for f in sorted(p.rglob('*')) if f.is_file() and '__pycache__' not in f.parts and f.name!='.DS_Store'],ensure_ascii=False).encode()).hexdigest()}

def resolve(run,profile=None,skill_roots=None):
    if profile is None: profile=json.loads((HERE/'references/runtime-profile.json').read_text())
    plan=run.get('plan',{})
    audience=plan.get('audience',profile.get('audience','customer'))
    if audience not in ('internal','customer'): raise ResolutionError('先明确内部或客户场景')
    owner=profile.get('owner_id') if audience=='internal' else plan.get('owner_id')
    family=profile.get('preferred_family') if audience=='internal' else plan.get('visual_family')
    if not owner: raise ResolutionError('先确认客户角色归属 owner_id')
    candidates=list(run.get('visual_candidates',[]))
    if audience=='internal' and family:
        roots=skill_roots or [Path.home()/'.codex/skills',Path.home()/'.agents/skills']
        for root in roots:
            for p in Path(root).glob(family+'*'):
                if (p/'SKILL.md').is_file():
                    candidates.append({'path':str(p),'owner_id':owner,'family':family,'approved':True})
    owned=[c for c in candidates if c.get('owner_id')==owner and c.get('approved') is True]
    if family: owned=[c for c in owned if c.get('family')==family]
    if not owned: raise ResolutionError('没有已确认的自有视觉小黑 Skill：先安装基础能力并魔改、确认与试图验收')
    families={c.get('family') for c in owned}
    if len(families)!=1 or None in families:
        raise ResolutionError('存在多个自有角色家族，先确认本次角色家族，再选其最新版本')
    checked=[]
    for c in owned:
        item=inspect(c)
        if not any(old['path']==item['path'] for old in checked): checked.append(item)
    highest=max(x['rank'] for x in checked)
    newest=[x for x in checked if x['rank']==highest]
    if len({x['package_sha256'] for x in newest})>1:
        raise ResolutionError('同版本候选内容不同，不能按修改时间猜选；请明确本次使用哪一份')
    result=sorted(newest,key=lambda x:x['path'])[0]
    return {k:v for k,v in result.items() if k!='rank'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run',required=True);parser.add_argument('--profile')
    args=parser.parse_args()
    run=json.loads(Path(args.run).read_text())
    profile=json.loads(Path(args.profile).read_text()) if args.profile else None
    try: print(json.dumps(resolve(run,profile),ensure_ascii=False,indent=2))
    except (ResolutionError,KeyError,OSError,ValueError) as e:
        print(json.dumps({'ok':False,'next_action':str(e)},ensure_ascii=False));return 1
    return 0
if __name__=='__main__': raise SystemExit(main())
