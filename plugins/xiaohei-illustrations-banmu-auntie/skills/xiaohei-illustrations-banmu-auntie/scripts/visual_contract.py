#!/usr/bin/env python3
"""Validate recorded design/QA/placement evidence, never infer visual truth."""
import argparse,json
from pathlib import Path
CHECKS=('meaning','identity','anatomy_gaze','expression','chinese','physical_relation','scene','lighting','clarity')
class ContractError(ValueError):pass
def require(c,m):
 if not c:raise ContractError(m)
def nonempty(v):return isinstance(v,str) and bool(v.strip())
def validate_design(images,group,artifact,draft=None,sole_human=False):
 require(images,'缺少待验收生成图')
 ids=set()
 for im in images:
  ident=im.get('id');require(nonempty(ident) and ident not in ids,'图片ID缺失或重复');ids.add(ident)
  for k in ('anchor','purpose','scene','placement'):
   require(nonempty(im.get(k)),ident+'缺少具体'+k)
  if draft is not None:require(im['anchor'] in draft,ident+'精确锚点不在实际文案中')
  ex=im.get('expression',{});li=im.get('lighting',{})
  require(isinstance(ex,dict) and all(nonempty(ex.get(k)) for k in ('intent','brows_eyes','mouth','gaze','body')),ident+'表情须明确情绪、眉眼、嘴型、视线、身体反应')
  require(isinstance(li,dict) and all(nonempty(li.get(k)) for k in ('key_light','depth','materials','contact_shadow')),ident+'缺少具体光影、纵深、材质或接触阴影')
  require(im.get('edit_mode') in ('new','preserve-scene'),ident+'须明确新建或保护场景编辑')
  if im['edit_mode']=='preserve-scene':
   require(nonempty(im.get('preserve')),ident+'未说明保留哪些正确部分')
   require(nonempty(im.get('original_path')),ident+'缺少被编辑原图');artifact(im['original_path'])
   require(im.get('qa_checks',{}).get('preservation') is True,ident+'原场景保护尚未验收')
  if sole_human:require(im.get('human_count')==1,ident+'违反已确认唯一人物策略')
  checks=im.get('qa_checks',{})
  require(all(checks.get(k) is True for k in CHECKS),ident+'缺少或未通过逐项目视记录')
  artifact(im.get('qa_evidence'))
 require(isinstance(group,dict) and all(group.get(k) is True for k in ('passed','coverage','scene_expression','quality')),'缺少整组覆盖、场景表情及质感复核')
 artifact(group.get('evidence'))
 return {'ok':True,'checked_images':len(images),'scope':'recorded design and evidence only; no visual truth inferred'}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--run',required=True);a=p.parse_args();rp=Path(a.run).resolve();root=rp.parent;d=json.loads(rp.read_text())
 def artifact(value):
  require(nonempty(value),'缺少QA证据路径');v=Path(value);require(not v.is_absolute(),'证据须任务内相对路径');v=(root/v).resolve();require(v.is_relative_to(root) and v.is_file() and v.stat().st_size>0,'证据不存在或越界');return v
 try:
  r=validate_design(d['images'],d['group_review'],artifact,sole_human=d.get('sole_human') is True);print(json.dumps(r,ensure_ascii=False));return 0
 except (ContractError,KeyError,OSError,ValueError) as e:print(json.dumps({'ok':False,'next_action':str(e)},ensure_ascii=False));return 1
if __name__=='__main__':raise SystemExit(main())
