import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { Presentation, PresentationFile } from '@oai/artifact-tool';

const [input,out]=process.argv.slice(2);
const data=JSON.parse(await fs.readFile(input,'utf8'));
const skill='/root/.codex/skills/builtins/presentations';
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
function textbox(slide,text,y,height,size=28){
  const box=slide.shapes.add({geometry:'textbox',position:{left:70,top:y,width:1140,height},fill:'none',line:{style:'solid',fill:'none',width:0}});
  box.text=text;
  box.text.style={fontSize:size,color:'#111111',wrap:'word',typeface:'DejaVu Sans'};
  return box;
}
for(const role of ['student','classroom']){
  const p=Presentation.create({slideSize:{width:1280,height:720}});
  const renderDir=path.join(out,'INSTRUCTOR ONLY/renders',role);await fs.mkdir(renderDir,{recursive:true});
  for(const item of data.slides){
    if(item.title.length>100||item.text.length>1400)throw Error('Slide content exceeds default layout; split content in master: '+item.id);
    const visibleText=item.text.replace(/^#{1,6}\s+/gm,'').replace(/\*\*([^*]+)\*\*/g,'$1').replace(/\[([^\]]+)\]\([^)]+\)/g,'$1');
    const s=p.slides.add();s.background.fill='#ffffff';textbox(s,item.title,45,90,44);textbox(s,visibleText,155,item.equations?.length||item.figures?.length?240:470,28);textbox(s,data.meta.course+' - '+item.id,660,30,16);
    const pictures=[...(item.equations||[]),...(item.figures||[])];
    if(pictures.length>2)throw Error('Split slide with more than two image/equation assets: '+item.id);
    for(const [j,imagePath] of pictures.entries()){
      const bytes=await fs.readFile(imagePath);s.images.add({blob:bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),contentType:'image/png',alt:item.id+' equation or figure '+(j+1),fit:'contain',position:{left:70+j*570,top:420,width:pictures.length===1?1140:540,height:200}});
    }
    if(role==='classroom'&&item.notes){s.speakerNotes.text=item.notes;s.speakerNotes.setVisible(true);}
    if(role==='classroom')for(const r of item.reveals){
      const reveal=p.slides.add();reveal.background.fill='#ffffff';textbox(reveal,r.id+' discussion',45,90,44);textbox(reveal,r.text,155,470,28);textbox(reveal,data.meta.course,660,30,16);
    }
  }
  for(const [i,s] of p.slides.items.entries()){
    const png=await p.export({slide:s,format:'png',scale:1.5});await fs.writeFile(path.join(renderDir,`${String(i+1).padStart(3,'0')}.png`),new Uint8Array(await png.arrayBuffer()));
  }
  const candidate=path.join(out,`INSTRUCTOR ONLY/${role}-candidate.pptx`);await(await PresentationFile.exportPptx(p)).save(candidate);
  const final=path.join(out,role==='student'?'STUDENT FILES/student-deck.pptx':'INSTRUCTOR ONLY/classroom-deck.pptx');
  await fs.mkdir(path.join(out,'_validation'),{recursive:true});
  await finalizePresentation({workspaceDir:out,candidatePath:candidate,finalPath:final,pythonExecutable:process.env.CODEX_PRIMARY_RUNTIME_PYTHON,integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit'],fontPolicy:{basis:'design',families:['DejaVu Sans']},verifyArtifactToolImport:true,receiptPath:path.join(out,`_validation/${role}-validation.json`)});
  await fs.unlink(candidate);
}
// PDF contains exactly the student-visible slides rendered from the same presentation model.
const {spawnSync}=await import('node:child_process');
const python=process.env.CODEX_PRIMARY_RUNTIME_PYTHON;
const result=spawnSync(python,['-c',`from PIL import Image\nfrom pathlib import Path\np=Path(${JSON.stringify(out)})\nimgs=[Image.open(f).convert('RGB') for f in sorted((p/'INSTRUCTOR ONLY/renders/student').glob('*.png'))]\nimgs[0].save(p/'STUDENT FILES/student-deck.pdf',save_all=True,append_images=imgs[1:],resolution=144)\n`],{encoding:'utf8'});
if(result.status!==0)throw Error(result.stderr);
