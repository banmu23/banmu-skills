#!/usr/bin/env python3
"""Validate ordered workflow gates and real local evidence; not an AI/visual verifier."""
import argparse
import hashlib
import json
import struct
import zlib
from datetime import datetime,timezone
from pathlib import Path
from resolve_visual_skill import resolve,ResolutionError
from visual_contract import validate_design,ContractError

HERE=Path(__file__).resolve().parents[1]
WORKFLOW=HERE/'references/workflow.json'
ORDER=json.loads(WORKFLOW.read_text())['gates']
DOC_STAGES=['copy','beautify','originals','visual','page']
class GateError(ValueError): pass
def require(condition,message):
    if not condition: raise GateError(message)
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def canonical(value): return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def png_size(data):
    require(data[:8]==b'\x89PNG\r\n\x1a\n','生成图必须是真实 PNG 文件')
    offset=8;size=None;has_data=False
    while offset+12<=len(data):
        length=struct.unpack('>I',data[offset:offset+4])[0]
        kind=data[offset+4:offset+8];end=offset+8+length
        require(end+4<=len(data),'PNG 文件不完整')
        payload=data[offset+8:end];crc=struct.unpack('>I',data[end:end+4])[0]
        require(zlib.crc32(kind+payload)&0xffffffff==crc,'PNG 校验失败')
        if offset==8:
            require(kind==b'IHDR' and length==13,'PNG 缺少有效 IHDR')
            size=struct.unpack('>II',payload[:8])
        if kind==b'IDAT': has_data=True
        if kind==b'IEND':
            require(length==0 and end+4==len(data) and has_data,'PNG 缺少图像数据或结束标记')
            return size
        offset=end+4
    raise GateError('PNG 文件缺少 IEND')

class Guard:
    def __init__(self,path):
        self.path=Path(path).resolve();self.root=self.path.parent
        self.run=json.loads(self.path.read_text(encoding='utf-8'))
        require(self.run.get('workflow_version')=='V3','运行记录不是 V3')
        require(self.run.get('workflow_sha256')==sha(WORKFLOW),'流程图版本/哈希不一致，先迁移并复核，不继承旧通过状态')
        self.state_path=self.root/'state.json'
        self.state=json.loads(self.state_path.read_text()) if self.state_path.exists() else {'schema':2,'checkpoints':{}}
        self.files=[]
    def artifact(self,value,expected=None):
        require(isinstance(value,str) and value.strip(),'缺少必要产物/证据路径')
        p=Path(value)
        require(not p.is_absolute(),'任务证据必须使用任务目录内的相对路径')
        p=(self.root/p).resolve()
        require(p.is_relative_to(self.root),'证据路径不能越出任务目录')
        require(p.is_file() and p.stat().st_size>0,'证据/产物不存在或为空：'+value)
        actual=sha(p)
        if expected is not None: require(actual==expected,'文件已变化，原确认或证据失效：'+value)
        self.files.append({'path':value,'sha256':actual})
        return p
    def key(self,stage,doc=None): return f'doc:{doc}:{stage}' if stage in DOC_STAGES else stage
    def predecessors(self,stage,doc):
        if stage=='plan': return []
        if stage=='access': return [('plan',None)]
        if stage in DOC_STAGES:
            i=DOC_STAGES.index(stage)
            order=self.run['plan']['required_docs']
            require(doc in order,'文档不在本期确认执行清单中')
            previous=order[order.index(doc)-1] if order.index(doc)>0 else None
            return [('plan',None),('access',None)]+([(DOC_STAGES[i-1],doc)] if i else ([('page',previous)] if previous else []))
        return [('plan',None),('access',None)]+[('page',d) for d in self.run['plan']['required_docs']]
    def definition(self,stage,doc):
        self.files=[]
        plan=self.run['plan'];mode=plan.get('mode')
        require(mode in ('auto','manual'),'先确定自动或手动模式')
        if stage=='plan':
            require(plan.get('confirmed') is True,'产品方案未经客户确认')
            self.artifact(plan.get('evidence'))
            require(plan.get('required_docs') and len(set(plan['required_docs']))==len(plan['required_docs']),'本期必需文档清单缺失或重复')
            require(all(isinstance(d,str) and d and ':' not in d for d in plan['required_docs']),'文档 ID 必须是非空字符串且不能含冒号')
            require(plan.get('owner_id'),'缺少资料/角色 owner_id')
            require(plan.get('deliverable') in ('content-package','feishu-live'),'先确定内容包或在线知识库交付目标')
            require(plan.get('sources'),'没有已读取的真实来源')
            ids=set()
            for s in plan['sources']:
                require(s.get('id') and s['id'] not in ids,'来源 ID 缺失或重复');ids.add(s['id'])
                require(s.get('read_confirmed') is True,'来源尚未实际读取')
                self.artifact(s.get('path'),s.get('sha256'))
                require(s.get('sha256'),'来源快照缺少哈希')
            payload=plan
        elif stage=='access':
            access=self.run['access'];self.artifact(access.get('evidence'))
            require(access.get('mode')==mode,'接入结果与确认模式不一致')
            if mode=='auto': require(set(access.get('verified',[]))>={'read','write','media'},'自动模式尚未实际验证读取、写入和传图')
            nodes=access.get('nodes',[]);ids={n.get('id') for n in nodes}
            require(len(ids)==len(nodes) and None not in ids,'知识库节点 ID 缺失或重复')
            homes=[n for n in nodes if n.get('kind')=='home']
            require(len(homes)==1 and homes[0].get('level')==1 and homes[0].get('parent') is None,'必须只有一个一级首页')
            byid={n['id']:n for n in nodes}
            for n in nodes:
                if n['kind']=='home': continue
                require(n.get('kind') in ('module','body'),'不允许额外后台页面类型')
                parent=byid.get(n.get('parent'))
                require(parent,'节点父页不存在')
                expected=(2,'home') if n['kind']=='module' else (3,'module')
                require((n.get('level'),parent.get('kind'))==expected,'必须首页→二级模块→三级正文，不能错层')
            require(set(plan['required_docs'])<=ids,'必需页面不在骨架中')
            execution=plan['required_docs']
            require(execution[0]==homes[0]['id'],'先完成首页再开始模块与正文')
            for did in execution[1:]:
                parent=byid[did]['parent']
                require(parent in execution[:execution.index(did)],'执行清单必须先父页、后子页')
            payload=access
        elif stage in DOC_STAGES:
            require(doc in self.run.get('documents',{}),'缺少当前文档记录')
            d=self.run['documents'][doc]
            require(d.get('kind') in ('home','module','body'),'文档类型错误')
            skeleton={n['id']:n for n in self.run['access']['nodes']}
            require(doc in skeleton and skeleton[doc]['kind']==d['kind'],'文档类型与骨架不一致')
            if stage=='copy':
                require(d.get('source_ids'),'本篇未绑定已读取来源')
                require(set(d['source_ids'])<={s['id'] for s in plan['sources']},'本篇跨出已确认来源范围')
                require(d.get('draft_sha256'),'草稿缺少哈希')
                self.artifact(d.get('draft'),d['draft_sha256'])
                a=d['approval'];require(a.get('confirmed') is True,'本篇文案尚未确认')
                require(a.get('content_sha256')==d['draft_sha256'],'文案确认没有绑定当前草稿')
                self.artifact(a.get('evidence'))
                points=d.get('comprehension_points',[])
                require(points or d['kind']!='body','正文缺少逐节理解点清单')
                anchors=[p.get('anchor') for p in points]
                require(all(isinstance(x,str) and x for x in anchors) and len(set(anchors))==len(anchors),'理解点锚点缺失或重复')
                draft=(self.root/d['draft']).read_text(encoding='utf-8')
                for point in points:
                    require(point['anchor'] in draft,'理解点锚点不在实际文案中')
                    require(type(point.get('required_visual')) is bool,'每个理解点须判断是否必须配图')
                payload={k:d[k] for k in ('kind','source_ids','draft','draft_sha256','approval','comprehension_points')}
            elif stage=='beautify':
                b=d['beautify'];require(b.get('method') in ('skill','equivalent','manual'),'缺少实际美化方式')
                require(b.get('passed') is True,'排版、美化或导航尚未通过')
                require(b.get('copy_sha256')==d['draft_sha256'],'美化对应的文案已失效')
                self.artifact(b.get('evidence'));payload=b
            elif stage=='originals':
                o=d['originals'];self.artifact(o.get('evidence'))
                images=o.get('images',[])
                require(type(o.get('source_total')) is int and o['source_total']==len(images),'源图总数与逐张清单不一致')
                require(all(im.get('id') for im in images) and len({im['id'] for im in images})==len(images),'原图 ID 缺失或重复')
                for im in images:
                    require(type(im.get('usable')) is bool,'未判断每张原图是否可用')
                    if not im['usable']: require(im.get('reason'),'不可用原图必须说明原因');continue
                    require(im.get('sha256'),'可用原图缺少哈希')
                    self.artifact(im.get('path'),im['sha256'])
                    require(im.get('inserted' if mode=='auto' else 'included') is True,'遗漏可用原图')
                    require(im.get('anchor'),'原图没有对应正文位置')
                payload=o
            elif stage=='visual':
                v=d['visual'];images=v.get('images',[])
                if not images:
                    require(d['kind'] in ('home','module') and v.get('navigation_only') is True and v.get('not_applicable_reason'),'正文不能零生成图；纯导航页不适用必须有依据')
                    require(not any(p.get('required_visual') for p in d['comprehension_points']),'有重要理解点的页面不能走零图导航分支')
                    self.artifact(v.get('coverage_evidence'));payload=v
                else:
                    actual=resolve(self.run)
                    used=v['skill']
                    require(all(used.get(k)==actual.get(k) for k in ('name','path','owner_id','family','version','skill_sha256','package_sha256')),'调用的不是归属正确、已确认家族的最新自有视觉 Skill')
                    require(used.get('actual_call_verified') is True,'视觉 Skill 没有真实调用结果')
                    self.artifact(used.get('call_evidence'));self.artifact(used.get('owner_evidence'))
                    self.artifact(v.get('coverage_evidence'))
                    require(v.get('coverage_review_passed') is True,'逐节配图充分性尚未复核')
                    ids=set()
                    for im in images:
                        require(im.get('id') and im['id'] not in ids,'生成图 ID 缺失或重复');ids.add(im['id'])
                        require(im.get('sha256'),'生成图缺少哈希')
                        file=self.artifact(im.get('path'),im['sha256'])
                        data=file.read_bytes()
                        w,h=png_size(data)
                        require(w>0 and h>0 and abs(h-w*9/16)<=1,'生成图必须 16:9，不能拉伸或方图充数')
                        require(im.get('visual_pass') is True,'生成图尚未逐图目视通过')
                        self.artifact(im.get('review_evidence'));self.artifact(im.get('delivery_evidence'))
                        require(im.get('inserted' if mode=='auto' else 'included') is True,'生成图未插入或未收入手动包')
                    original_ids={im['id'] for im in d['originals']['images'] if im.get('usable')}
                    coverage=v.get('coverage',[])
                    require(coverage,'没有逐节配图覆盖表')
                    require(len({c.get('anchor') for c in coverage})==len(coverage),'配图覆盖锚点重复')
                    byanchor={c.get('anchor'):c for c in coverage}
                    for point in d['comprehension_points']:
                        require(point['anchor'] in byanchor,'理解点没有进入配图覆盖表：'+point['anchor'])
                        if point['required_visual']:
                            require(byanchor[point['anchor']].get('route')!='text' and byanchor[point['anchor']].get('image_ids'),'重要理解点缺图：'+point['anchor'])
                    for item in coverage:
                        route=item.get('route');refs=set(item.get('image_ids',[]))
                        require(item.get('anchor') and route in ('original','generated','text'),'覆盖表缺正文锚点或有效路径')
                        if item.get('required') is True:
                            require(route!='text' and refs,'重要理解点遗漏图片')
                        if route=='generated':require(refs and refs<=ids,'覆盖表引用不存在的生成图')
                        elif route=='original':require(refs and refs<=original_ids,'覆盖表引用不存在的原图')
                        else: require(item.get('reason'),'文字足够须说明内容判断依据')
                    referenced=set().union(*(set(c.get('image_ids',[])) for c in coverage))
                    require(ids<=referenced,'有生成图未对应正文理解点')
                    validate_design(images,v.get('group_review'),self.artifact,
                                    draft=(self.root/d['draft']).read_text(encoding='utf-8'),
                                    sole_human=json.loads((HERE/'references/runtime-profile.json').read_text()).get('visual_policy',{}).get('sole_human') is True and plan.get('audience')=='internal')
                    for im in images:
                        require(im['anchor'] in byanchor and im['id'] in byanchor[im['anchor']].get('image_ids',[]),'图片精确锚点与覆盖表不一致')
                    payload={'visual':v,'resolved':actual}
            else:
                q=d['qa'];require(q.get('passed') is True,'单篇尚未验收通过')
                require(all(q.get(k) is True for k in ('preservation_passed','presentation_clean','placement_review_passed')),'原资源保护、客户呈现或关键位置尚未验收')
                require(isinstance(q.get('scope'),str) and q['scope'].strip(),'须记录实际预览方式/范围及未实测项')
                self.artifact(q.get('content_evidence'))
                if mode=='auto':
                    self.artifact(q.get('readback_evidence'));self.artifact(q.get('preview_evidence'))
                else:
                    self.artifact(q.get('package_evidence'))
                    if plan['deliverable']=='feishu-live':
                        self.artifact(q.get('readback_evidence'));self.artifact(q.get('preview_evidence'))
                payload=q
        else:
            f=self.run['final'];self.artifact(f.get('evidence'))
            require(f.get('passed') is True,'整库/本期内容包尚未通过验收')
            require(f.get('kind')==plan['deliverable'],'完成声明与确认交付目标不一致')
            if f['kind']=='feishu-live':
                require(isinstance(f.get('target_url'),str) and f['target_url'].startswith('https://'),'在线交付缺少真实目标链接')
                self.artifact(f.get('readback_evidence'));self.artifact(f.get('preview_evidence'))
            payload=f
        return canonical({'payload':payload,'files':sorted(self.files,key=lambda x:(x['path'],x['sha256']))})
    def verify(self,stage,doc=None):
        key=self.key(stage,doc);entry=self.state['checkpoints'].get(key)
        require(entry and entry.get('status')=='passed','前置关卡未通过：'+key)
        for prev,pdoc in self.predecessors(stage,doc):
            self.verify(prev,pdoc)
            require(entry.get('dependencies',{}).get(self.key(prev,pdoc))==self.state['checkpoints'][self.key(prev,pdoc)]['digest'],'前序证据已改变，重新验收：'+key)
        require(entry['digest']==self.definition(stage,doc),'产物/证据发生变化，关卡失效：'+key)
    def advance(self,stage,doc=None):
        deps={}
        for prev,pdoc in self.predecessors(stage,doc):
            self.verify(prev,pdoc);deps[self.key(prev,pdoc)]=self.state['checkpoints'][self.key(prev,pdoc)]['digest']
        digest=self.definition(stage,doc)
        key=self.key(stage,doc)
        self.state['checkpoints'][key]={'status':'passed','digest':digest,'dependencies':deps,'checked_at':datetime.now(timezone.utc).isoformat()}
        temp=self.state_path.with_suffix('.json.tmp');temp.write_text(json.dumps(self.state,ensure_ascii=False,indent=2)+'\n');temp.replace(self.state_path)
        return {'ok':True,'gate':key,'scope':'record-and-file-validation; does not prove visual/online truth'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['gate','audit']);p.add_argument('--run',required=True);p.add_argument('--stage',choices=ORDER);p.add_argument('--doc')
    a=p.parse_args()
    try:
        g=Guard(a.run)
        if a.command=='gate':
            require(a.stage,'缺少阶段');require(a.stage not in DOC_STAGES or a.doc,'当前阶段必须提供 --doc')
            result=g.advance(a.stage,a.doc)
        else:
            for key in list(g.state['checkpoints']):
                if key.startswith('doc:'):_,doc,stage=key.split(':',2);g.verify(stage,doc)
                else:g.verify(key)
            result={'ok':True,'checked_gates':len(g.state['checkpoints']),'complete':'final' in g.state['checkpoints']}
        print(json.dumps(result,ensure_ascii=False));return 0
    except (GateError,ContractError,ResolutionError,KeyError,ValueError,OSError,struct.error) as e:
        print(json.dumps({'ok':False,'next_action':str(e)},ensure_ascii=False));return 1
if __name__=='__main__':raise SystemExit(main())
