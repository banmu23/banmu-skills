#!/usr/bin/env python3
"""Isolated regression tests. Synthetic images/evidence are tests, never delivery proof."""
import copy,hashlib,json,struct,tempfile,unittest,zlib
from pathlib import Path
from workflow_guard import Guard,GateError,WORKFLOW,DOC_STAGES
from resolve_visual_skill import resolve,ResolutionError

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def png(w=160,h=90):
 def chunk(t,b):return struct.pack('>I',len(b))+t+b+struct.pack('>I',zlib.crc32(t+b)&0xffffffff)
 return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,8,2,0,0,0))+chunk(b'IDAT',zlib.compress((b'\x00'+b'\xff\xff\xff'*w)*h))+chunk(b'IEND',b'')
class WorkflowTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);self.path=self.root/'run.json'
  for f in ['evidence.md','source.md','draft.md']:(self.root/f).write_text('TEST ONLY: # 步骤一\n# 步骤二\n',encoding='utf-8')
  (self.root/'original.png').write_bytes(png());(self.root/'generated.png').write_bytes(png())
  self.skill=self.root/'customer-visual';self.skill.mkdir()
  (self.skill/'SKILL.md').write_text('---\nname: customer-visual\nmetadata:\n  version: V1\n---\n# TEST ONLY\n')
  candidate={'path':str(self.skill),'owner_id':'test-customer','family':'test-family','approved':True}
  self.run={'workflow_version':'V2','workflow_sha256':digest(WORKFLOW),
   'plan':{'audience':'customer','owner_id':'test-customer','visual_family':'test-family','mode':'manual','deliverable':'content-package','confirmed':True,'evidence':'evidence.md','required_docs':['home','module','body'],'sources':[{'id':'s1','path':'source.md','sha256':digest(self.root/'source.md'),'read_confirmed':True}]},
   'access':{'mode':'manual','evidence':'evidence.md','nodes':[{'id':'home','kind':'home','level':1,'parent':None},{'id':'module','kind':'module','level':2,'parent':'home'},{'id':'body','kind':'body','level':3,'parent':'module'}]},
   'visual_candidates':[candidate],'documents':{},'final':{'kind':'content-package','passed':True,'evidence':'evidence.md'}}
  skill={**resolve(self.run),'actual_call_verified':True,'call_evidence':'evidence.md','owner_evidence':'evidence.md'}
  for did,kind in [('home','home'),('module','module'),('body','body')]:
   d={'kind':kind,'source_ids':['s1'],'draft':'draft.md','draft_sha256':digest(self.root/'draft.md'),'comprehension_points':[],
   'approval':{'confirmed':True,'content_sha256':digest(self.root/'draft.md'),'evidence':'evidence.md'},
   'beautify':{'method':'manual','passed':True,'copy_sha256':digest(self.root/'draft.md'),'evidence':'evidence.md'},
   'originals':{'source_total':0,'evidence':'evidence.md','images':[]},
   'visual':{'images':[],'navigation_only':True,'not_applicable_reason':'TEST ONLY pure navigation','coverage_evidence':'evidence.md'},
   'qa':{'passed':True,'content_evidence':'evidence.md','package_evidence':'evidence.md'}}
   if kind=='body':
    d['comprehension_points']=[{'anchor':'步骤一','required_visual':True},{'anchor':'步骤二','required_visual':True}]
    d['originals']={'source_total':1,'evidence':'evidence.md','images':[{'id':'o1','usable':True,'path':'original.png','sha256':digest(self.root/'original.png'),'anchor':'步骤一','included':True}]}
    d['visual']={'skill':skill,'images':[{'id':'g1','path':'generated.png','sha256':digest(self.root/'generated.png'),'visual_pass':True,'review_evidence':'evidence.md','delivery_evidence':'evidence.md','included':True}],
    'coverage_review_passed':True,'coverage_evidence':'evidence.md','coverage':[{'anchor':'步骤一','route':'original','image_ids':['o1'],'required':True},{'anchor':'步骤二','route':'generated','image_ids':['g1'],'required':True}]}
   self.run['documents'][did]=d
  self.save()
 def tearDown(self):self.temp.cleanup()
 def save(self):self.path.write_text(json.dumps(self.run,ensure_ascii=False),encoding='utf-8')
 def gate(self,s,d=None):self.save();return Guard(self.path).advance(s,d)
 def prepare(self):
  self.gate('plan');self.gate('access')
  for did in ['home','module']:
   for s in DOC_STAGES:self.gate(s,did)
  for s in ['copy','beautify','originals']:self.gate(s,'body')
 def reject(self,s,d=None):
  with self.assertRaises((GateError,ResolutionError)):self.gate(s,d)
 def test_full_manual_package_and_audit(self):
  self.prepare();self.gate('visual','body');self.gate('page','body');self.gate('final')
  g=Guard(self.path);g.verify('final');self.assertEqual(len(g.state['checkpoints']),18)
 def test_unconfirmed_plan(self):self.run['plan']['confirmed']=False;self.reject('plan')
 def test_skip_gate(self):self.reject('access')
 def test_wrong_hierarchy(self):
  self.gate('plan');self.run['access']['nodes'][2]['parent']='home';self.reject('access')
 def test_next_doc_before_previous_finished(self):self.gate('plan');self.gate('access');self.reject('copy','module')
 def test_changed_confirmed_draft(self):
  self.prepare();(self.root/'draft.md').write_text('changed');self.reject('visual','body')
 def test_changed_source(self):self.prepare();(self.root/'source.md').write_text('changed');self.reject('visual','body')
 def test_missing_original(self):
  self.prepare();(self.root/'original.png').unlink();self.reject('visual','body')
 def test_original_inventory_mismatch(self):
  self.prepare();self.run['documents']['body']['originals']['source_total']=2;self.reject('originals','body')
 def test_no_customer_visual(self):self.prepare();self.run['visual_candidates']=[];self.reject('visual','body')
 def test_wrong_visual_owner(self):self.prepare();self.run['visual_candidates'][0]['owner_id']='other';self.reject('visual','body')
 def test_newer_visual_rejects_old_selection(self):
  self.prepare();(self.skill/'VERSION').write_text('V2');self.reject('visual','body')
 def test_latest_actual_visual_selected(self):
  newer=self.root/'newer';newer.mkdir();(newer/'SKILL.md').write_text('---\nname: newer\nmetadata:\n  version: V4\n---\n')
  self.run['visual_candidates'].append({**self.run['visual_candidates'][0],'path':str(newer)})
  self.assertEqual(resolve(self.run)['name'],'newer')
 def test_conflicting_same_version(self):
  other=self.root/'other';other.mkdir();(other/'SKILL.md').write_text('---\nname: other\nmetadata:\n  version: V1\n---\n')
  self.run['visual_candidates'].append({**self.run['visual_candidates'][0],'path':str(other)})
  with self.assertRaises(ResolutionError):resolve(self.run)
 def test_visual_reference_change_invalidates(self):
  self.prepare();(self.skill/'ref.txt').write_text('changed style');self.reject('visual','body')
 def test_uncovered_important_point(self):
  self.prepare();self.run['documents']['body']['visual']['coverage'].pop();self.reject('visual','body')
 def test_important_point_cannot_be_text(self):
  self.prepare();self.run['documents']['body']['visual']['coverage'][1]={'anchor':'步骤二','route':'text','reason':'trying to skip','required':False};self.reject('visual','body')
 def test_body_cannot_have_zero_generated_images(self):
  self.prepare();self.run['documents']['body']['visual']=copy.deepcopy(self.run['documents']['home']['visual']);self.reject('visual','body')
 def test_corrupt_png(self):
  self.prepare();p=self.root/'generated.png';p.write_bytes(png()[:-5]);self.run['documents']['body']['visual']['images'][0]['sha256']=digest(p);self.reject('visual','body')
 def test_square_png(self):
  self.prepare();p=self.root/'generated.png';p.write_bytes(png(90,90));self.run['documents']['body']['visual']['images'][0]['sha256']=digest(p);self.reject('visual','body')
 def test_missing_visual_review(self):
  self.prepare();self.run['documents']['body']['visual']['images'][0]['visual_pass']=False;self.reject('visual','body')
 def test_live_requires_readback_and_preview(self):
  self.run['plan']['deliverable']='feishu-live';self.run['final']['kind']='feishu-live'
  self.gate('plan');self.gate('access')
  for s in DOC_STAGES[:-1]:self.gate(s,'home')
  self.reject('page','home')
 def test_manual_package_cannot_claim_live(self):
  self.prepare();self.gate('visual','body');self.gate('page','body');self.run['final']['kind']='feishu-live';self.reject('final')
 def test_final_needs_all_pages(self):self.prepare();self.reject('final')
 def test_evidence_cannot_escape_directory(self):self.run['plan']['evidence']='../outside.txt';self.reject('plan')
 def test_wrong_flow_version(self):self.run['workflow_sha256']='obsolete';self.reject('plan')
if __name__=='__main__':unittest.main(verbosity=2)
