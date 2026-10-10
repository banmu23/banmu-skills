#!/usr/bin/env python3
"""Public build integrity and owned-role readiness; never proves visual truth."""
import argparse,hashlib,json,struct,zlib
from pathlib import Path
from visual_contract import validate_design,ContractError
def png_info(path):
    data = path.read_bytes()
    if data[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError(f'Not PNG: {path}')
    pos, size, ended = 8, None, False
    while pos < len(data):
        if pos + 12 > len(data):
            raise ValueError(f'Truncated chunk: {path}')
        n = struct.unpack('>I', data[pos:pos + 4])[0]
        kind = data[pos + 4:pos + 8]
        body = data[pos + 8:pos + 8 + n]
        if pos + 12 + n > len(data):
            raise ValueError(f'Truncated PNG: {path}')
        crc = struct.unpack('>I', data[pos + 8 + n:pos + 12 + n])[0]
        if zlib.crc32(kind + body) & 0xffffffff != crc:
            raise ValueError(f'CRC mismatch: {path}')
        if kind == b'IHDR':
            size = struct.unpack('>II', body[:8])
        pos += n + 12
        if kind == b'IEND':
            ended = True
            break
    if not ended or not size or min(size) <= 0:
        raise ValueError(f'Invalid PNG structure: {path}')
    return size, hashlib.sha256(data).hexdigest()

def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--run',type=Path);p.add_argument('--require-ready',action='store_true');p.add_argument('--trial',action='store_true');a=p.parse_args();root=a.root.resolve();errors=[]
 for rel in ['SKILL.md','VERSION','LICENSE','NOTICE.md','references/workflow.json','references/role-profile.json','scripts/visual_contract.py']:
  if not (root/rel).is_file():errors.append('Missing '+rel)
 role=json.loads((root/'references/role-profile.json').read_text());ready=False
 anchor=role.get('main_anchor')
 if role.get('confirmed') is True and role.get('owner_id') and role.get('family') and anchor:
  q=Path(anchor);q=q if q.is_absolute() else root/q
  ready=False
  try: png_info(q);ready=bool(role.get('style') and role.get('character_rules'))
  except (OSError,ValueError):pass
 base_ready=ready;ready=base_ready and role.get('trial_passed') is True
 if a.require_ready and not (base_ready if a.trial else ready):errors.append('自有角色未完成授权、确认与真实主参考校验，先引导安装魔改和试图')
 if a.run:
  if not ready:errors.append('Cannot validate completed images without ready owned-role references')
  d=json.loads(a.run.read_text());rr=a.run.parent.resolve()
  def artifact(v):
   if not isinstance(v,str) or not v or Path(v).is_absolute():raise ContractError('Invalid task evidence')
   q=(rr/v).resolve()
   if not q.is_relative_to(rr) or not q.is_file() or not q.stat().st_size:raise ContractError('Missing task evidence')
   return q
  try:validate_design(d['images'],d.get('group_review'),artifact,sole_human=role.get('sole_human') is True)
  except (ContractError,KeyError) as e:errors.append(str(e))
  for im in d['images']:
   q=rr/im['file'];data=q.read_bytes()
   try: png_info(q)
   except (OSError,ValueError) as e:errors.append(str(e))
   if data[:8]!=b'\x89PNG\r\n\x1a\n' or hashlib.sha256(data).hexdigest()!=im['sha256']:errors.append('Invalid PNG/hash '+im['id'])
   else:
    w,h=struct.unpack('>II',data[16:24])
    if abs(h-w*9/16)>1:errors.append('Wrong aspect '+im['id'])
   if not im.get('generation_origin') or not im.get('tool'):errors.append('Missing actual generation '+im['id'])
 print(json.dumps({'ok':not errors,'ready_for_generation':ready,'ready_for_trial':base_ready,'errors':errors,'scope':'package/records only; own character setup and actual trial required'},ensure_ascii=False));return int(bool(errors))
if __name__=='__main__':raise SystemExit(main())
