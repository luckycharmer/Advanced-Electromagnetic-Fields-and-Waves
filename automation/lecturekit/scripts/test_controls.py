#!/usr/bin/env python3
"""Local synthetic regression tests. Never publish the fixtures as teaching evidence."""
import copy,importlib.util,json,tempfile,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('lk',Path(__file__).with_name('lecturekit.py'));lk=importlib.util.module_from_spec(spec);spec.loader.exec_module(lk)

def fixture(work):
    (work/'evidence').mkdir(exist_ok=True);(work/'evidence/context.txt').write_text('Synthetic test syllabus and supplied prerequisites, previous/next teaching, assessment and private destinations. Not an actual course.')
    m=lk.template('TEST101','L2','Linear calibration',60);m['meta']['level']='synthetic'
    for k in lk.CONTEXT:m['context'][k]={'verified':True,'fact':'Synthetic fixture '+k,'evidence_refs':['evidence/context.txt']}
    m['sources']=[{'id':'S1','title':'Synthetic calibration specification','uri':'fixture:test','edition':'test','status':'opened','accessed_at':lk.now(),'snapshot_path':'evidence/context.txt','sha256':lk.sha(work/'evidence/context.txt'),'core':True}]
    m['claims']=[{'id':'CL1','text':'y=a*x for the supplied linear model','source_ids':['S1'],'scope':'synthetic exact linear model','verification':'substitute x=2,a=3 gives y=6','evidence_refs':['evidence/context.txt']}]
    m['outcomes']=[{'id':'LO1','statement':'Calculate a response from a supplied linear slope.','syllabus_mapping':'Synthetic model'}]
    m['equations']=[{'id':'EQ1','latex':'y=ax','symbols':'a slope; x input; y response','assumptions':'Exact linear model, zero intercept','geometry':'No spatial geometry in this scalar calibration model.','steps':[{'explanation':'Multiply the input by the supplied slope.','latex':'y=3\\times 2=6'}],'units':'Dimensionless test quantities','verification':'Direct multiplication and repeated addition agree.','source_ids':['S1']}]
    m['blocks']=[{'id':'B1','kind':'explanation','markdown':'## Linear response\n\nUse the supplied slope to calculate the response. {{eq:EQ1}}','outcome_ids':['LO1'],'source_ids':['S1'],'claim_ids':['CL1']},{'id':'B2','kind':'worked_example','markdown':'## Distinct worked example\n\nFor a slope of four and input of three, the response is twelve.','outcome_ids':['LO1'],'source_ids':['S1'],'claim_ids':['CL1']},{'id':'B3','kind':'instructor','markdown':'Private instructor briefing sentinel for release-control testing.','outcome_ids':[],'source_ids':[],'claim_ids':[]}]
    m['questions']=[{'id':'Q'+str(i),'stage':stage,'prompt':'For slope two and input five calculate the response.','outcome_ids':['LO1'],'marks':1,'space_lines':2,'solution':('Active assessment sentinel answer is ten.' if stage in ['exit','assignment'] else 'The response is ten.'),'marking':['1 mark for ten using the supplied model.'],'common_slips':['Adding rather than multiplying.'],'active_assessment':True} for i,stage in enumerate(['diagnostic','worksheet','exit','followup','assignment'],1)]
    for doc in m['documents']:
        if doc['purpose'] in ['preview','reference']:doc['block_ids']=['B1','B2']
        elif doc['purpose']=='teaching_plan':doc['block_ids']=['B3']
    m['slides']=[{'id':'SL1','title':'Linear calibration','block_ids':['B1'],'question_ids':[],'reveal_question_ids':[],'instructor_notes':'Private instructor note sentinel.'},{'id':'SL2','title':'Response calculation','block_ids':['B2'],'question_ids':['Q2'],'reveal_question_ids':['Q2'],'instructor_notes':'Discuss the attempt before showing the next slide.'}]
    m['timeline']=[{'type':'diagnostic','minutes':5,'question_ids':['Q1'],'action':'Attempt diagnostic'}, {'type':'explanation','minutes':10,'slide_ids':['SL1'],'outcome_ids':['LO1'],'action':'Introduce the model'},{'type':'board','minutes':10,'action':'Board derivation'},{'type':'guided_calculation','minutes':10,'action':'Guided calculation'},{'type':'activity','minutes':10,'question_ids':['Q2'],'action':'Student attempt'},{'type':'explanation','minutes':5,'slide_ids':['SL2'],'action':'Discuss response'},{'type':'exit','minutes':5,'question_ids':['Q3'],'action':'Exit assessment'},{'type':'contingency','minutes':5,'action':'Contingency'}]
    m['interactive']['reason']='No tool needed to learn scalar multiplication.';m['policy']['student_access']='Synthetic isolated fixture; no external delivery.'
    lk.write(work/'master.json',m);return m

class Controls(unittest.TestCase):
    def setUp(self):self.temp=tempfile.TemporaryDirectory();self.work=Path(self.temp.name);self.m=fixture(self.work)
    def tearDown(self):self.temp.cleanup()
    def test_valid_fixture(self):self.assertEqual(lk.validate(self.m,self.work),[])
    def test_empty_context_blocked(self):self.m['context']['official_syllabus']['verified']=False;self.assertTrue(lk.validate(self.m,self.work))
    def test_duration_overrun(self):self.m['timeline'][0]['minutes']+=1;self.assertIn('Timeline must sum exactly to duration',lk.validate(self.m,self.work))
    def test_missing_outcome_coverage(self):self.m['outcomes'].append({'id':'LO2','statement':'Other task','syllabus_mapping':'test'});self.assertIn('Outcome lacks teaching or assessment LO2',lk.validate(self.m,self.work))
    def test_unknown_reference(self):self.m['slides'][0]['block_ids']=['unknown'];self.assertTrue(lk.validate(self.m,self.work))
    def test_private_student_block(self):self.m['documents'][0]['block_ids']=['B3'];self.assertIn('Private block in student document',lk.validate(self.m,self.work))
    def test_assessment_reveal(self):self.m['slides'][1]['reveal_question_ids']=['Q3'];self.assertIn('Active assessed answer in classroom Q3',lk.validate(self.m,self.work))
    def test_early_reveal(self):self.m['slides'][0]['reveal_question_ids']=['Q2'];self.assertIn('Reveal precedes attempt Q2',lk.validate(self.m,self.work))
    def test_source_hash(self):(self.work/'evidence/context.txt').write_text('changed');self.assertIn('Source snapshot hash mismatch S1',lk.validate(self.m,self.work))
    def test_path_escape(self):
        with self.assertRaises(lk.Blocked):lk.path(self.work,'../escape')
    def test_branding(self):self.m['blocks'][0]['markdown']='Generated by ChatGPT';self.assertTrue(lk.validate(self.m,self.work))
    def test_missing_solution(self):self.m['questions'][0]['solution']='';self.assertTrue(lk.validate(self.m,self.work))
    def test_inadequate_contingency(self):self.m['timeline'][-1]['minutes']=0;self.m['timeline'][0]['minutes']+=5;self.assertTrue(lk.validate(self.m,self.work))
    def test_stale_receipt(self):
        (self.work/'build').mkdir();lk.write(self.work/'build/manifest.json',{'master_sha256':lk.masterhash(self.work),'files':[]})
        r={'master_sha256':lk.masterhash(self.work),'manifest_sha256':lk.buildhash(self.work),'evidence':lk.evidence(self.work,['evidence/context.txt'])};self.assertTrue(lk.receiptvalid(self.work,r));self.m['meta']['topic']='Changed';lk.write(self.work/'master.json',self.m);self.assertFalse(lk.receiptvalid(self.work,r))
    def test_evidence_mutation(self):
        (self.work/'build').mkdir();lk.write(self.work/'build/manifest.json',{'master_sha256':lk.masterhash(self.work),'files':[]});r={'master_sha256':lk.masterhash(self.work),'manifest_sha256':lk.buildhash(self.work),'evidence':lk.evidence(self.work,['evidence/context.txt'])};(self.work/'evidence/context.txt').write_text('altered');self.assertFalse(lk.receiptvalid(self.work,r))
    def test_unreviewed_release_blocked(self):
        (self.work/'build').mkdir();lk.write(self.work/'build/manifest.json',{'master_sha256':lk.masterhash(self.work),'files':[]})
        with self.assertRaises(lk.Blocked):lk.release(self.work,'content')
    def test_export_mutation(self):
        (self.work/'build').mkdir();(self.work/'build/test.pdf').write_text('original');lk.write(self.work/'build/manifest.json',{'master_sha256':lk.masterhash(self.work),'files':[{'path':'test.pdf','sha256':lk.sha(self.work/'build/test.pdf')}]});(self.work/'build/test.pdf').write_text('changed')
        with self.assertRaises(lk.Blocked):lk.current(self.work)

if __name__=='__main__':unittest.main()
