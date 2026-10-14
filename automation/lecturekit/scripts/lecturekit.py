#!/usr/bin/env python3
"""Deterministic build/control layer. Scientific and visual review are evidence gates."""
import argparse, copy, csv, fcntl, hashlib, importlib.util, json, math, os, re, shutil, subprocess, sys, tempfile, time, zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
GATES=['syllabus_alignment','continuity','prerequisites','outcomes','content_correctness','derivations','units_numerics','sources','assessment','timing','rendering','functionality','delivery_public_safety']
PURPOSES=['preview','reference','worksheet','exit','followup','derivations','teaching_plan','solutions']
STUDENT=set(PURPOSES[:6]); PRIVATE=set(PURPOSES[6:])
CONTEXT=['official_syllabus','prerequisites','textbook_edition','previous_teaching','next_plan','assessment_coverage','destinations']
BRANDING=re.compile(r'(?i)(generated (?:by|with) (?:ai|chatgpt|claude)|as an ai|chatgpt|claude\.ai/artifact|powered by (?:openai|anthropic)|\[TODO\]|PLACEHOLDER|reviewer note:)')
IDENT=re.compile(r'^[A-Za-z0-9_-]+$')
class Blocked(Exception): pass
def digest(b): return hashlib.sha256(b).hexdigest()
def sha(p): return digest(Path(p).read_bytes())
def canonical(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def load(p): return json.loads(Path(p).read_text())
def write(p,x):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    data=json.dumps(x,indent=2,ensure_ascii=False)+'\n'
    tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_text(data);os.replace(tmp,p)
def now():return datetime.now(timezone.utc).isoformat()
def path(base,relative):
    if not isinstance(relative,str) or not relative:raise Blocked('Missing relative evidence/asset path')
    candidate=(base/relative).resolve()
    if not candidate.is_relative_to(base.resolve()):raise Blocked('Path escapes private work directory: '+relative)
    return candidate
def run(args,**kw):
    r=subprocess.run(args,text=True,capture_output=True,**kw)
    if r.returncode:raise Blocked('Command failed: '+args[0]+'\n'+(r.stderr+'\n'+r.stdout)[-3500:])
    return r.stdout
def master(work):return load(work/'master.json')
def masterhash(work):return digest(canonical(master(work)))
def manifest(work):return load(work/'build/manifest.json')
def buildhash(work):return digest(canonical(manifest(work)))
def template(course,session,topic,duration):
    return {'meta':{'schema_version':1,'course':course,'session':session,'topic':topic,'date':None,'duration_minutes':duration,'timezone':'Asia/Karachi','level':'','handwriting_font':'Caveat'},
    'context':{k:{'verified':False,'fact':'','evidence_refs':[]} for k in CONTEXT},
    'sources':[],'claims':[],'outcomes':[],'constants':[],'equations':[],'figures':[],'blocks':[],'questions':[],
    'documents':[{'purpose':p,'title':p.replace('_',' ').title(),'block_ids':[],'question_ids':[],'public':p in ['reference','derivations']} for p in PURPOSES],
    'slides':[],'timeline':[],'interactive':{'enabled':False,'reason':'','benefit':'','html_path':'','fallback_block_ids':[],'test_evidence_refs':[]},
    'policy':{'public_document_purposes':['reference','derivations'],'required_disclosure':'','student_access':'','instructor_access':'private','publish_github':False}}

def validate(m,work):
    errors=[]
    def need(test,msg):
        if not test:errors.append(msg)
    need(m.get('meta',{}).get('schema_version')==1,'Unsupported schema version')
    meta=m.get('meta',{});d=meta.get('duration_minutes')
    need(isinstance(d,(int,float)) and not isinstance(d,bool) and d>0,'Actual positive duration required')
    for key in ['course','session','topic','level']:need(bool(meta.get(key)),f'Missing meta.{key}')
    for key in ['course','session']:need(bool(IDENT.fullmatch(str(meta.get(key,'')))),'Unsafe identifier '+key)
    indexes={}
    for collection in ['sources','claims','outcomes','constants','equations','figures','blocks','questions','slides']:
        values=m.get(collection,[]);need(isinstance(values,list),collection+' must be an array')
        ix={}
        for obj in values:
            ident=obj.get('id','');need(bool(IDENT.fullmatch(ident)),collection+' unsafe/missing ID')
            need(ident not in ix,'Duplicate '+collection+' ID '+ident);ix[ident]=obj
        indexes[collection]=ix
    def refs(obj,field,target):
        for r in obj.get(field,[]):need(r in indexes[target],f'Unknown {target} ID {r}')
    for key in CONTEXT:
        c=m.get('context',{}).get(key,{})
        need(c.get('verified') is True and c.get('fact') and c.get('evidence_refs'),'Unresolved core context: '+key)
        for ep in c.get('evidence_refs',[]):need(path(work,ep).is_file(),'Missing context evidence '+ep)
    need(1<=len(m.get('outcomes',[]))<=10,'Measurable lecture outcomes required')
    for o in m.get('outcomes',[]):need(o.get('statement') and o.get('syllabus_mapping'),'Outcome statement/mapping missing')
    for s in m.get('sources',[]):
        need(s.get('title') and s.get('uri'),'Source title/URI required')
        need(s.get('status') in ['opened','not_opened'],'Source access status required')
        if s.get('core',False):need(s.get('status')=='opened','Unopened core source '+s['id'])
        if s.get('status')=='opened':
            need(bool(s.get('accessed_at')),'Source access time missing '+s['id'])
            p=path(work,s.get('snapshot_path',''));need(p.is_file(),'Source snapshot missing '+s['id'])
            if p.is_file():need(s.get('sha256')==sha(p),'Source snapshot hash mismatch '+s['id'])
    need(any(s.get('core') and s.get('status')=='opened' for s in m.get('sources',[])),'At least one opened core source required')
    for c in m.get('claims',[]):
        refs(c,'source_ids','sources');need(c.get('text') and c.get('scope') and c.get('verification'),'Claim traceability missing '+c['id'])
        need(bool(c.get('source_ids')),'Claim sources missing '+c['id'])
        for ep in c.get('evidence_refs',[]):need(path(work,ep).is_file(),'Missing claim evidence')
    for c in m.get('constants',[]):
        need(isinstance(c.get('value'),(int,float)) and math.isfinite(c['value']),'Invalid constant '+c['id'])
        need(c.get('source_id') in indexes['sources'] and c.get('unit') and c.get('tolerance'),'Constant source/unit/tolerance missing '+c['id'])
    for eq in m.get('equations',[]):
        refs(eq,'source_ids','sources')
        for k in ['latex','symbols','assumptions','geometry','steps','units','verification']:need(bool(eq.get(k)),'Equation '+eq['id']+' missing '+k)
        need(bool(eq.get('source_ids')),'Equation source missing '+eq['id'])
    need(bool(m.get('equations')),'Derivation equations required')
    for f in m.get('figures',[]):
        for k in ['path','editable_source_path']:need(path(work,f.get(k,'')).is_file(),'Figure/editable source missing '+f['id'])
        need(f.get('alt') and f.get('attribution') and f.get('licence'),'Figure provenance missing '+f['id'])
    for b in m.get('blocks',[]):
        need(b.get('markdown'),'Empty block '+b['id']);refs(b,'outcome_ids','outcomes');refs(b,'source_ids','sources');refs(b,'figure_ids','figures');refs(b,'claim_ids','claims')
        if b.get('kind') in ['explanation','worked_example']:need(bool(b.get('claim_ids')),'Scientific block lacks claim mapping '+b['id'])
        need(not BRANDING.search(b.get('markdown','').replace(m.get('policy',{}).get('required_disclosure','') or '\x00','')),'Unsolicited branding/draft residue '+b['id'])
        for typ,ident in re.findall(r'\{\{(eq|const):([^}]+)\}\}',b.get('markdown','')):need(ident in indexes['equations' if typ=='eq' else 'constants'],'Unresolved central token '+ident)
    for q in m.get('questions',[]):
        need(q.get('stage') in ['diagnostic','worksheet','exit','followup','assignment'],'Question stage missing '+q['id'])
        refs(q,'outcome_ids','outcomes');need(q.get('outcome_ids') and q.get('prompt') and q.get('solution') and q.get('marking'),'Question prompt/solution/marking/outcome missing '+q['id'])
        need(isinstance(q.get('marks'),(int,float)) and q['marks']>=0,'Question marks invalid '+q['id'])
        need(0<=q.get('space_lines',3)<=30,'Writing space invalid '+q['id'])
    for stage in ['diagnostic','worksheet','exit','followup','assignment']:need(any(q.get('stage')==stage for q in m.get('questions',[])),'Missing '+stage+' questions')
    taught=set();assessed=set()
    for b in m.get('blocks',[]):taught.update(b.get('outcome_ids',[]))
    for q in m.get('questions',[]):
        if q.get('stage')!='diagnostic':assessed.update(q.get('outcome_ids',[]))
    for o in indexes['outcomes']:need(o in taught and o in assessed,'Outcome lacks teaching or assessment '+o)
    docs=m.get('documents',[]);need(sorted(x.get('purpose','') for x in docs)==sorted(PURPOSES),'Required document purposes missing/duplicated')
    for doc in docs:
        refs(doc,'block_ids','blocks');refs(doc,'question_ids','questions')
        if doc.get('purpose') in STUDENT:need(all(indexes['blocks'][b].get('kind') not in ['instructor','logistics'] for b in doc.get('block_ids',[]) if b in indexes['blocks']),'Private block in student document')
        if doc.get('purpose') in ['preview','reference','teaching_plan']:need(bool(doc.get('block_ids')),'Empty required document '+doc['purpose'])
        expected={'preview':['diagnostic'],'worksheet':['worksheet'],'exit':['exit'],'followup':['followup','assignment']}.get(doc.get('purpose'))
        if expected and doc.get('question_ids'):
            needed={q['id'] for q in m['questions'] if q['stage'] in expected}
            need(set(doc['question_ids'])==needed,'Question-stage coverage differs from required purpose '+doc['purpose'])
    timeline=m.get('timeline',[])
    need(all(isinstance(t.get('minutes'),(int,float)) and t['minutes']>=0 for t in timeline),'Invalid timeline duration')
    if isinstance(d,(int,float)):
        need(abs(sum(t.get('minutes',0) for t in timeline)-d)<.001,'Timeline must sum exactly to duration')
        need(sum(t.get('minutes',0) for t in timeline if t.get('type')=='contingency')>=.05*d,'Reserve at least 5% contingency')
    for typ in ['diagnostic','explanation','board','guided_calculation','activity','exit','contingency']:need(any(t.get('type')==typ for t in timeline),'Missing teaching block '+typ)
    seen=set();attempted_before={}
    for t in timeline:
        refs(t,'slide_ids','slides');refs(t,'question_ids','questions');refs(t,'outcome_ids','outcomes')
        for sid in t.get('slide_ids',[]):attempted_before[sid]=set(seen)
        seen.update(t.get('question_ids',[]))
    need(bool(m.get('slides')),'Deck content missing')
    for s in m.get('slides',[]):
        refs(s,'block_ids','blocks');refs(s,'question_ids','questions');refs(s,'reveal_question_ids','questions');refs(s,'equation_ids','equations');refs(s,'figure_ids','figures')
        need(s.get('title') and (s.get('block_ids') or s.get('question_ids')),'Empty slide '+s['id'])
        need(s['id'] in attempted_before,'Slide not in run sheet '+s['id'])
        for qid in s.get('reveal_question_ids',[]):
            q=indexes['questions'].get(qid,{})
            need(not(q.get('active_assessment') and q.get('stage') in ['exit','assignment']),'Active assessed answer in classroom '+qid)
            need(qid in attempted_before.get(s['id'],set()),'Reveal precedes attempt '+qid)
        need(all(indexes['blocks'].get(b,{}).get('kind') not in ['instructor','logistics'] for b in s.get('block_ids',[])),'Private block on visible slide')
    it=m.get('interactive',{})
    if it.get('enabled'):
        need(it.get('benefit') and it.get('fallback_block_ids') and it.get('test_evidence_refs'),'Interactive benefit/fallback/test missing')
        refs(it,'fallback_block_ids','blocks');need(path(work,it.get('html_path','')).is_file(),'Interactive HTML missing')
        htmlpath=path(work,it.get('html_path',''))
        if htmlpath.is_file():need(not re.search(r'<(?:script|img|link)[^>]+(?:src|href)=[\"\x27](?:https?:|//)',htmlpath.read_text(),re.I),'Interactive external dependencies prevent offline self-contained delivery')
    else:need(it.get('reason'),'Explain why no interactive is needed')
    need(bool(m.get('policy',{}).get('student_access')),'Intended student access policy missing')
    return errors

def expand(text,m,work,latex=False):
    eq={e['id']:e for e in m['equations']};cs={c['id']:c for c in m['constants']}
    def sub(match):
        typ,ident=match.groups()
        if typ=='eq':return '$$\n'+eq[ident]['latex']+'\n$$\n\n('+ident+')'
        c=cs[ident];return f"{c.get('symbol',ident)} = {c['value']} {c['unit']}"
    return re.sub(r'\{\{(eq|const):([^}]+)\}\}',sub,text)
def qtext(q,solutions=False):
    s=f"### {q['id']} ({q['marks']} marks; {', '.join(q['outcome_ids'])})\n\n{q['prompt']}\n\n"
    if solutions:s+='**Solution**\n\n'+q['solution']+'\n\n**Marking**\n\n'+'\n'.join('- '+x for x in q['marking'])+'\n\n**Common slips**\n\n'+'\n'.join('- '+x for x in q.get('common_slips',[]))+'\n\n'
    else:s+='\n\n'.join('________________________________________________________________' for _ in range(q.get('space_lines',3)))+'\n\n'
    return s
def docmarkdown(doc,m,work):
    blocks={b['id']:b for b in m['blocks']};questions={q['id']:q for q in m['questions']};purpose=doc['purpose']
    s=f"# {doc['title']}\n\n{m['meta']['course']} - {m['meta']['session']} - {m['meta']['topic']}\n\n"
    if purpose not in ['solutions','teaching_plan']:s+='## Learning outcomes\n\n'+'\n'.join(f"- {o['id']}: {o['statement']}" for o in m['outcomes'])+'\n\n'
    for bid in doc.get('block_ids',[]):
        b=blocks[bid];s+=expand(b['markdown'],m,work)+'\n\n'
        for fid in b.get('figure_ids',[]):
            f=next(f for f in m['figures'] if f['id']==fid);s+=f"![{f['alt']}]({path(work,f['path'])})\n\n{f['attribution']}\n\n"
    automatic={'preview':['diagnostic'],'worksheet':['worksheet'],'exit':['exit'],'followup':['followup','assignment']}
    qids=doc.get('question_ids') or [q['id'] for q in m['questions'] if q['stage'] in automatic.get(purpose,[])]
    if purpose=='solutions':qids=[q['id'] for q in m['questions']]
    for qid in qids:s+=expand(qtext(questions[qid],purpose=='solutions'),m,work)+'\n\n'
    if purpose=='derivations':
        for e in m['equations']:
            s+=f"## {e['id']}\n\n**Assumptions:** {e['assumptions']}\n\n**Geometry:** {e['geometry']}\n\n**Symbols:** {e['symbols']}\n\n"
            for i,step in enumerate(e['steps'],1):s+=f"{i}. {step['explanation']}\n\n$$\n{step['latex']}\n$$\n\n"
            s+='**Final result**\n\n$$\n'+e['latex']+'\n$$\n\n**Units:** '+e['units']+'\n\n**Verification:** '+e['verification']+'\n\n'
    if purpose=='teaching_plan':
        s+='## Run sheet\n\n| Elapsed minutes | Type | Action | Slides | Cut priority |\n|---|---|---|---|---|\n';clock=0
        for t in m['timeline']:
            s+=f"| {clock:g}-{clock+t['minutes']:g} | {t['type']} | {t.get('action','')} | {', '.join(t.get('slide_ids',[]))} | {t.get('cut_priority','core')} |\n";clock+=t['minutes']
        s+='\n## Outcome evidence\n\n'
        for o in m['outcomes']:s+=f"- {o['id']}: "+', '.join(q['id'] for q in m['questions'] if o['id'] in q['outcome_ids'])+'\n'
    if m['policy'].get('required_disclosure'):s+='\n'+m['policy']['required_disclosure']+'\n'
    return s
def pdf(md,pdf,font='DejaVu Sans',pagestyle='plain'):
    if font=='Caveat':
        bundled=ROOT/'assets/Caveat.ttf'
        if not bundled.is_file():raise Blocked('Bundled handwriting font missing')
        fontdir=Path.home()/'.local/share/fonts/lecturekit';fontdir.mkdir(parents=True,exist_ok=True)
        installed=fontdir/'Caveat.ttf'
        if not installed.exists() or sha(installed)!=sha(bundled):
            shutil.copy2(bundled,installed);run(['fc-cache','-f',str(fontdir)],timeout=30)
        if 'Caveat' not in run(['fc-match','-f','%{family}',font]):raise Blocked('Handwriting font installation could not be verified')
    run(['pandoc',str(md),'-o',str(pdf),'--pdf-engine=xelatex','-V','papersize:a4','-V','geometry:margin=18mm','-V','mainfont='+font,'-V','fontsize=11pt','-V','pagestyle='+pagestyle],timeout=180)
    from pypdf import PdfReader,PdfWriter
    reader=PdfReader(pdf);writer=PdfWriter();writer.append_pages_from_reader(reader);writer.add_metadata({'/Title':md.stem,'/Author':'','/Creator':'','/Producer':''})
    with open(pdf,'wb') as f:writer.write(f)
def scrub_pptx(p,student):
    ns={'r':'http://schemas.openxmlformats.org/package/2006/relationships','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
    temp=p.with_suffix('.clean.pptx')
    with zipfile.ZipFile(p) as zin,zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            name=item.filename
            if student and any(x in name for x in ['notesSlides/','notesMasters/','comments/','commentAuthors']):continue
            data=zin.read(name)
            if name.endswith('.xml') or name.endswith('.rels'):
                root=ET.fromstring(data)
                if name=='[Content_Types].xml':ET.register_namespace('','http://schemas.openxmlformats.org/package/2006/content-types')
                if student:
                    for parent in root.iter():
                        for child in list(parent):
                            tag=child.tag.rsplit('}',1)[-1]
                            if tag in ['notesMasterIdLst','notesMasterId'] or any(x in child.attrib.get('Type','')+child.attrib.get('Target','')+child.attrib.get('PartName','') for x in ['notesSlide','notesMaster','comment']):parent.remove(child)
                if name=='docProps/core.xml':
                    for child in root:
                        if child.tag.rsplit('}',1)[-1] in ['creator','lastModifiedBy']:child.text=''
                if name=='docProps/app.xml':
                    for child in root:
                        if child.tag.rsplit('}',1)[-1] in ['Application','Company','Manager']:child.text=''
                if '/theme' in name:
                    for child in root.iter():
                        if child.attrib.get('name') in ['ChatGPT','OpenAI','Artifact Tool']:child.set('name','Lecture')
                data=ET.tostring(root,encoding='utf-8',xml_declaration=True)
            zout.writestr(item,data)
    os.replace(temp,p)
def build(work):
    m=master(work);errors=validate(m,work)
    if errors:raise Blocked('\n'.join(errors))
    if (work/'build/manifest.json').exists():
        try:
            old=current(work)
            if old.get('engine_sha256')==sha(__file__) and old.get('deck_builder_sha256')==sha(ROOT/'scripts/decks.mjs'):return {'state':'DRAFT_BUILT','resumed_unchanged':True,'manifest_sha256':buildhash(work),'files':len(old['files'])}
        except Blocked:pass
    build=work/'build';tmp=work/'_staging';shutil.rmtree(tmp,ignore_errors=True);tmp.mkdir()
    for folder in ['STUDENT FILES','INSTRUCTOR ONLY','INSTRUCTOR ONLY/sources','INSTRUCTOR ONLY/renders']: (tmp/folder).mkdir(parents=True,exist_ok=True)
    source=tmp/'INSTRUCTOR ONLY/sources';files=[]
    def add(p,role,purpose):files.append({'path':str(p.relative_to(tmp)),'sha256':sha(p),'size':p.stat().st_size,'role':role,'purpose':purpose})
    for doc in m['documents']:
        role='student' if doc['purpose'] in STUDENT else 'instructor';folder=tmp/('STUDENT FILES' if role=='student' else 'INSTRUCTOR ONLY')
        md=source/(doc['purpose']+'.md');md.write_text(docmarkdown(doc,m,work));f=folder/(doc['purpose']+'.pdf')
        font=m['meta'].get('handwriting_font','Caveat') if doc['purpose']=='derivations' else 'DejaVu Sans'
        pdf(md,f,font);add(f,role,doc['purpose']);add(md,'instructor','editable_source')
    for eq in m['equations']:
        (source/(eq['id']+'.tex')).write_text(eq['latex']+'\n')
        add(source/(eq['id']+'.tex'),'instructor','equation_source')
        # Typeset exact equation from the central source for mathematical slides.
        eqmd=source/(eq['id']+'-render.md');eqmd.write_text('$$\n'+eq['latex']+'\n$$\n')
        eqpdf=source/(eq['id']+'-render.pdf');pdf(eqmd,eqpdf,pagestyle='empty')
        run(['pdftoppm','-singlefile','-r','600','-png',str(eqpdf),str(source/eq['id'])],timeout=45)
        from PIL import Image,ImageChops
        im=Image.open(source/(eq['id']+'.png')).convert('RGB');bounds=ImageChops.difference(im,Image.new('RGB',im.size,'white')).getbbox()
        if bounds:im.crop((max(0,bounds[0]-15),max(0,bounds[1]-15),min(im.width,bounds[2]+15),min(im.height,bounds[3]+15))).save(source/(eq['id']+'.png'))
        eqmd.unlink();eqpdf.unlink();add(source/(eq['id']+'.png'),'instructor','equation_render')
    for fig in m['figures']:
        for key in ['path','editable_source_path']:
            original=path(work,fig[key]);dest=source/fig[key];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(original,dest)
            if not any(item['path']==str(dest.relative_to(tmp)) for item in files):add(dest,'instructor','figure_source')
    shutil.copy2(work/'master.json',source/'master.json');add(source/'master.json','instructor','master')
    for s in m['sources']:
        if s.get('status')=='opened':
            snapshot=path(work,s['snapshot_path']);dest=source/s['snapshot_path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(snapshot,dest);add(dest,'instructor','source_snapshot')
    for script in ['lecturekit.py','decks.mjs']:
        dest=source/'runtime/scripts'/script;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/'scripts'/script,dest);add(dest,'instructor','build_source')
    for asset in ['Caveat.ttf','Caveat-OFL.txt','master.schema.json']:
        dest=source/'runtime/assets'/asset;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/'assets'/asset,dest);add(dest,'instructor','runtime_asset')
    with (tmp/'INSTRUCTOR ONLY/source-register.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['id','title','uri','edition','status','accessed_at','sha256']);w.writerows([[s.get(k,'') for k in ['id','title','uri','edition','status','accessed_at','sha256']] for s in m['sources']])
    add(tmp/'INSTRUCTOR ONLY/source-register.csv','instructor','register')
    if m['interactive']['enabled']:
        shutil.copy2(path(work,m['interactive']['html_path']),tmp/'STUDENT FILES/exercise.html');add(tmp/'STUDENT FILES/exercise.html','student','interactive')
        original=path(work,m['interactive']['html_path']);dest=source/m['interactive']['html_path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(original,dest);add(dest,'instructor','interactive_source')
        doc={'purpose':'fallback','title':'Static exercise','block_ids':m['interactive']['fallback_block_ids']};md=source/'static-fallback.md';md.write_text(docmarkdown(doc,m,work));f=tmp/'STUDENT FILES/static-fallback.pdf';pdf(md,f);add(f,'student','fallback')
    # Export supported editable slides. Deck script emits role-separated PPTX and PNG previews.
    deckdata={'meta':m['meta'],'slides':[], 'private_solution_strings':[]}
    blocks={b['id']:b for b in m['blocks']};qs={q['id']:q for q in m['questions']}
    for s in m['slides']:
        eqids=list(s.get('equation_ids',[]))
        raw='\n\n'.join(blocks[x]['markdown'] for x in s.get('block_ids',[]))
        for ident in re.findall(r'\{\{eq:([^}]+)\}\}',raw):
            if ident not in eqids:eqids.append(ident)
        raw=re.sub(r'\{\{eq:([^}]+)\}\}',lambda r:'Equation '+r.group(1),raw)
        visible=expand(raw,m,work)
        visible+='\n\n'+'\n\n'.join(qs[x]['id']+': '+qs[x]['prompt'] for x in s.get('question_ids',[]))
        if '$' in visible or '{{' in visible:raise Blocked('Deck formula rendering required: supply slide image assets or plain Unicode math in blocks; unresolved raw LaTeX cannot be released')
        if len(eqids)>2:raise Blocked('Split slide with more than two equations: '+s['id'])
        deckdata['slides'].append({'id':s['id'],'title':s['title'],'text':visible.strip(),'notes':s.get('instructor_notes',''),'equations':[str(source/(ident+'.png')) for ident in eqids],'figures':[str(path(work,next(f for f in m['figures'] if f['id']==ident)['path'])) for ident in s.get('figure_ids',[])],'reveals':[{'id':qid,'text':qs[qid]['solution']} for qid in s.get('reveal_question_ids',[])]})
    write(source/'deck-data.json',deckdata)
    node=os.environ.get('CODEX_PRIMARY_RUNTIME_NODE');modules=os.environ.get('CODEX_PRIMARY_RUNTIME_NODE_MODULES')
    if not node or not modules:raise Blocked('Supported presentation runtime environment missing')
    runner=source/'runtime/scripts/decks.mjs';os.symlink(modules,runner.parent/'node_modules')
    run([node,str(runner),str(source/'deck-data.json'),str(tmp)],timeout=240)
    (runner.parent/'node_modules').unlink()
    scrub_pptx(tmp/'STUDENT FILES/student-deck.pptx',True);scrub_pptx(tmp/'INSTRUCTOR ONLY/classroom-deck.pptx',False)
    inspector='/root/.codex/skills/builtins/presentations/container_tools/inspect_presentation_package_integrity.py'
    for deck in [tmp/'STUDENT FILES/student-deck.pptx',tmp/'INSTRUCTOR ONLY/classroom-deck.pptx']:
        run([sys.executable,inspector,str(deck),'--fail-on-findings'],timeout=30)
    for f,role,purpose in [(tmp/'STUDENT FILES/student-deck.pptx','student','student_deck'),(tmp/'STUDENT FILES/student-deck.pdf','student','student_deck_pdf'),(tmp/'INSTRUCTOR ONLY/classroom-deck.pptx','instructor','classroom_deck')]:add(f,role,purpose)
    # Re-run leakage and package checks before committing a staging build.
    scan(m,tmp,files)
    # Asset ingestion/finalization can normalize image bytes. Hash only final bytes.
    for item in files:
        finalfile=tmp/item['path'];item['sha256']=sha(finalfile);item['size']=finalfile.stat().st_size
    result={'schema_version':1,'engine_sha256':sha(__file__),'deck_builder_sha256':sha(ROOT/'scripts/decks.mjs'),'master_sha256':masterhash(work),'files':sorted(files,key=lambda f:f['path']),'dependencies':{'python':sys.version.split()[0],'pandoc':run(['pandoc','--version']).splitlines()[0],'node':run([node,'--version']).strip(),'artifact_tool_version':load(Path(modules)/'@oai/artifact-tool/package.json').get('version'),'font':m['meta'].get('handwriting_font','Caveat'),'font_sha256':sha(ROOT/'assets/Caveat.ttf')}}
    write(tmp/'manifest.json',result)
    if build.exists():
        old=work/'_previous-build';shutil.rmtree(old,ignore_errors=True);os.replace(build,old)
    os.replace(tmp,build)
    return {'state':'DRAFT_BUILT','manifest_sha256':buildhash(work),'files':len(files)}

def scan(m,base,files):
    disclosure=m.get('policy',{}).get('required_disclosure','') or '\x00'
    private=[q['solution'] for q in m['questions'] if q.get('active_assessment') and q.get('stage') in ['exit','assignment']]
    private += [b['markdown'] for b in m['blocks'] if b.get('kind')=='instructor']
    for f in files:
        p=base/f['path']
        if f['role']!='student':continue
        text=''
        if p.suffix=='.pdf':
            from pypdf import PdfReader
            text='\n'.join(page.extract_text() or '' for page in PdfReader(p).pages)
        elif p.suffix=='.html':text=p.read_text()
        elif p.suffix=='.pptx':
            with zipfile.ZipFile(p) as z:
                for name in z.namelist():
                    if 'comments/' in name or 'notesSlides/notesSlide' in name:raise Blocked('Student deck contains notes/comments')
                    if name.startswith('ppt/slides/slide') and name.endswith('.xml'):
                        root=ET.fromstring(z.read(name));
                        if root.attrib.get('show')=='0':raise Blocked('Student hidden slide')
                    if name.endswith('.xml'):text+=' '+z.read(name).decode(errors='replace')
        if BRANDING.search(text.replace(disclosure,'')):raise Blocked('Branding or drafting residue in '+f['path'])
        normalized=lambda x:re.sub(r'\s+',' ',x).strip()
        for s in private:
            if len(normalized(s))>=15 and normalized(s) in normalized(text):raise Blocked('Private assessment/notes leakage in '+f['path'])

def current(work):
    mf=manifest(work)
    if mf['master_sha256']!=masterhash(work):raise Blocked('Master changed; rebuild before review/release')
    required={('STUDENT FILES/' if p in STUDENT else 'INSTRUCTOR ONLY/')+p+'.pdf' for p in PURPOSES}
    required.update(['STUDENT FILES/student-deck.pptx','STUDENT FILES/student-deck.pdf','INSTRUCTOR ONLY/classroom-deck.pptx','INSTRUCTOR ONLY/source-register.csv','INSTRUCTOR ONLY/sources/master.json'])
    if not required.issubset({f['path'] for f in mf['files']}):raise Blocked('Manifest omits required output files')
    for f in mf['files']:
        p=path(work/'build',f['path'])
        if not p.is_file() or sha(p)!=f['sha256']:raise Blocked('Missing/changed export: '+f['path'])
    errors=validate(master(work),work)
    if errors:raise Blocked('Source/context validation changed: '+'; '.join(errors))
    return mf
def evidence(work,refs):
    if not refs:raise Blocked('Actual evidence files required')
    return [{'path':r,'sha256':sha(path(work,r))} for r in refs]
def receiptvalid(work,r):
    if r.get('master_sha256')!=masterhash(work) or r.get('manifest_sha256')!=buildhash(work):return False
    return all(path(work,e['path']).is_file() and sha(path(work,e['path']))==e['sha256'] for e in r.get('evidence',[])) and bool(r.get('evidence'))
def release(work,phase):
    current(work);reviews=load(work/'reviews.json') if (work/'reviews.json').exists() else {}
    required=range(1,14 if phase=='delivered' else 13);blocked=[]
    for n in required:
        r=reviews.get(str(n),{})
        if not receiptvalid(work,r) or r.get('status') not in (['pass','not_applicable'] if n==12 else ['pass']):blocked.append(f'{n}: {GATES[n-1]}')
    if phase=='delivered':
        receipts=load(work/'delivery.json') if (work/'delivery.json').exists() else {}
        for f in manifest(work)['files']:
            r=receipts.get(f['path'],{})
            if r.get('sha256')!=f['sha256'] or not r.get('verified') or not r.get('remote_id') or not r.get('parent_id') or not r.get('evidence') or any(not path(work,e['path']).is_file() or sha(path(work,e['path']))!=e['sha256'] for e in r.get('evidence',[])):blocked.append('Delivery: '+f['path'])
    state={'state':'BLOCKED' if blocked else ('DELIVERY_VERIFIED' if phase=='delivered' else 'CONTENT_VERIFIED'),'blocked':blocked,'master_sha256':masterhash(work),'manifest_sha256':buildhash(work),'at':now()}
    write(work/'release.json',state)
    if blocked:raise Blocked('; '.join(blocked))
    return state
def public(work):
    release(work,'content');m=master(work);allowed=set(m['policy'].get('public_document_purposes',[]))
    if not allowed.issubset({'preview','reference','worksheet','followup','derivations'}):raise Blocked('Unsafe public purpose in allowlist')
    dest=work/'GITHUB READY';shutil.rmtree(dest,ignore_errors=True);dest.mkdir()
    pub=[]
    for doc in m['documents']:
        if doc['purpose'] not in allowed or not doc.get('public'):continue
        blockmap={b['id']:b for b in m['blocks']};figmap={f['id']:f for f in m['figures']}
        for bid in doc.get('block_ids',[]):
            for fid in blockmap[bid].get('figure_ids',[]):
                if not figmap[fid].get('public'):raise Blocked('Figure not approved for public sharing: '+fid)
        if any(q['active_assessment'] for q in m['questions'] if q['id'] in doc.get('question_ids',[]) or q['stage'] in {'preview':['diagnostic'],'worksheet':['worksheet'],'followup':['followup','assignment']}.get(doc['purpose'],[])):raise Blocked('Active assessment in public document')
        p=dest/(doc['purpose']+'.pdf');shutil.copy2(work/'build/STUDENT FILES'/p.name,p);pub.append(p)
    if m['interactive'].get('enabled') and m['interactive'].get('public'):
        for name in ['exercise.html','static-fallback.pdf']:
            p=dest/name;shutil.copy2(work/'build/STUDENT FILES'/name,p);pub.append(p)
    (dest/'README.md').write_text(f"# {m['meta']['course']}\n\n{m['meta']['topic']}\n\n"+'\n'.join('- ['+p.name+']('+p.name+')' for p in pub)+'\n')
    scan(m,dest,[{'path':p.name,'role':'student'} for p in pub])
    return {'state':'STAGED_NOT_PUBLISHED','files':[p.name for p in pub]}
def doctor():
    return {'commands':{k:shutil.which(k) for k in ['pandoc','xelatex','pdftoppm','fc-match']},'python_packages':{k:bool(importlib.util.find_spec(k)) for k in ['pypdf','PIL']},'node':os.environ.get('CODEX_PRIMARY_RUNTIME_NODE'),'modules':os.environ.get('CODEX_PRIMARY_RUNTIME_NODE_MODULES'),'bundled_handwriting_font':(ROOT/'assets/Caveat.ttf').is_file(),'scientific_review':'requires evidence; cannot be certified by this script'}
def main():
    p=argparse.ArgumentParser(description=__doc__);sp=p.add_subparsers(dest='cmd',required=True)
    sp.add_parser('doctor')
    a=sp.add_parser('init');a.add_argument('--course',required=True);a.add_argument('--session',required=True);a.add_argument('--topic',required=True);a.add_argument('--duration',type=float,required=True);a.add_argument('--out',type=Path,required=True)
    for cmd in ['validate','build','status','stage-public','delivery-plan']:
        a=sp.add_parser(cmd);a.add_argument('work',type=Path)
    a=sp.add_parser('record-gate');a.add_argument('work',type=Path);a.add_argument('--number',type=int,required=True,choices=range(1,14));a.add_argument('--status',required=True,choices=['pass','fail','unverified','not_applicable']);a.add_argument('--reviewer',required=True);a.add_argument('--note',required=True);a.add_argument('--evidence',nargs='+',required=True)
    a=sp.add_parser('record-delivery');a.add_argument('work',type=Path);a.add_argument('--file',required=True);a.add_argument('--remote-id',required=True);a.add_argument('--parent-id',required=True);a.add_argument('--readback-sha256',required=True);a.add_argument('--evidence',nargs='+',required=True)
    a=sp.add_parser('release');a.add_argument('work',type=Path);a.add_argument('--phase',choices=['content','delivered'],required=True)
    a=p.parse_args()
    try:
        if a.cmd=='doctor':result=doctor()
        elif a.cmd=='init':
            if a.out.exists() and any(a.out.iterdir()):raise Blocked('Refusing to overwrite existing work; use status/resume')
            a.out.mkdir(parents=True,exist_ok=True);(a.out/'evidence').mkdir();(a.out/'assets').mkdir();write(a.out/'master.json',template(a.course,a.session,a.topic,a.duration));result={'state':'CONTEXT_REQUIRED','master':str(a.out/'master.json')}
        elif a.cmd=='validate':
            errors=validate(master(a.work),a.work);result={'valid':not errors,'errors':errors}
            if errors:print(json.dumps(result,indent=2));return 2
        elif a.cmd=='build':
            with (a.work/'build.lock').open('w') as lock:
                try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
                except BlockingIOError:raise Blocked('Another build owns this work directory; retry after it completes')
                result=build(a.work)
        elif a.cmd=='release':result=release(a.work,a.phase)
        elif a.cmd=='stage-public':result=public(a.work)
        elif a.cmd=='record-gate':
            if a.status in ['pass','not_applicable']:current(a.work)
            if a.status=='not_applicable' and a.number!=12:raise Blocked('Only functionality may be not_applicable')
            r=load(a.work/'reviews.json') if (a.work/'reviews.json').exists() else {};r[str(a.number)]={'status':a.status,'reviewer':a.reviewer,'note':a.note,'evidence':evidence(a.work,a.evidence),'master_sha256':masterhash(a.work),'manifest_sha256':buildhash(a.work) if (a.work/'build/manifest.json').exists() else None,'at':now()};write(a.work/'reviews.json',r);result=r[str(a.number)]
        elif a.cmd=='record-delivery':
            release(a.work,'content')
            mf=current(a.work);f=next((f for f in mf['files'] if f['path']==a.file),None)
            if not f or a.readback_sha256!=f['sha256']:raise Blocked('Readback hash differs from current approved output')
            r=load(a.work/'delivery.json') if (a.work/'delivery.json').exists() else {};r[a.file]={'remote_id':a.remote_id,'parent_id':a.parent_id,'sha256':f['sha256'],'verified':True,'evidence':evidence(a.work,a.evidence),'at':now()};write(a.work/'delivery.json',r);result=r[a.file]
        elif a.cmd=='delivery-plan':
            mf=current(a.work);r=load(a.work/'delivery.json') if (a.work/'delivery.json').exists() else {}
            result={'operations':[dict(f,remote_id=r.get(f['path'],{}).get('remote_id'),operation='reconcile_or_skip' if r.get(f['path'],{}).get('sha256')==f['sha256'] else ('update' if r.get(f['path'],{}).get('remote_id') else 'create_after_reconciliation')) for f in mf['files']]}
        elif a.cmd=='status':
            result={'master_sha256':masterhash(a.work),'build_exists':(a.work/'build/manifest.json').exists()}
            try:current(a.work);result['build_current']=True
            except (Blocked,FileNotFoundError):result['build_current']=False
            result['last_release']=load(a.work/'release.json') if (a.work/'release.json').exists() else None
            result['last_blocker']=load(a.work/'last-blocker.json') if (a.work/'last-blocker.json').exists() else None
            if result['build_current']:
                r=load(a.work/'reviews.json') if (a.work/'reviews.json').exists() else {};result['gates']={str(n):r.get(str(n),{}).get('status','unverified') if receiptvalid(a.work,r.get(str(n),{})) else 'stale_or_unverified' for n in range(1,14)}
        print(json.dumps(result,indent=2));return 0
    except (Blocked,FileNotFoundError,KeyError,ValueError,TypeError) as e:
        result={'state':'BLOCKED','command':a.cmd,'reason':str(e),'at':now()}
        if getattr(a,'work',None) and a.work.is_dir():write(a.work/'last-blocker.json',result)
        print(json.dumps(result,indent=2));return 2
if __name__=='__main__':sys.exit(main())
