// Generates the submission from the team's Markdown sections. Run npm run build:phase1.
// Open rebuilt files in Word and update the contents and page fields before submission.
const fs=require('fs'),path=require('path');
const {Document,Packer,Paragraph,TextRun,HeadingLevel,AlignmentType,Table,TableRow,TableCell,WidthType,ShadingType,LevelFormat,PageBreak,TableOfContents,PageNumber,Footer,Header,BorderStyle,VerticalAlign,TableLayoutType,ExternalHyperlink}=require('docx');
const FONT='Calibri',WIDTH=9746,NAVY='243746',OUT='Phase1_Initial_Plan_and_Requirements.docx';
const border={style:BorderStyle.SINGLE,size:4,color:'D9D9D9'};
function inline(text,base={}){
  const result=[],re=/(https?:\/\/[^\s|]+|\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)/g;
  let last=0,m;
  const run=(s,x={})=>new TextRun({text:s,font:FONT,size:22,color:'000000',...base,...x});
  while((m=re.exec(text))){
    if(m.index>last)result.push(run(text.slice(last,m.index)));
    const t=m[0];
    if(t.startsWith('http'))result.push(new ExternalHyperlink({link:t,children:[run(t,{color:NAVY})]}));
    else if(t.startsWith('**'))result.push(run(t.slice(2,-2),{bold:true}));
    else if(t.startsWith('`'))result.push(run(t.slice(1,-1),{font:'Consolas'}));
    else result.push(run(t.slice(1,-1),{italics:true}));
    last=m.index+t.length;
  }
  if(last<text.length)result.push(run(text.slice(last)));
  return result;
}
const p=(text,options={})=>new Paragraph({spacing:{after:110,line:260},widowControl:true,children:inline(text),...options});
const space=()=>new Paragraph({spacing:{after:60,before:0,line:80},children:[]});
const pageBreak=()=>new Paragraph({children:[new PageBreak()],spacing:{after:0,before:0}});
function cleanHeading(t){return t.replace(/^(\d+)\.\s/,'$1 ').replace(/(\d)[–-](\d)/g,'$1 to $2').replace(/\(Initial Reflection\)/,'Initial Reflection').replace(/\(As-Is\)/,'As Is').replace(/vs\./g,'and').replace(/\s[–—]\s/g,' ').replace(/[-–]/g,' ').replace(/[():]/g,'').replace(/\s+/g,' ').trim();}
function heading(level,text){return new Paragraph({heading:[HeadingLevel.HEADING_1,HeadingLevel.HEADING_2,HeadingLevel.HEADING_3][level-1],keepNext:true,pageBreakBefore:level===1&&/^1\.\s/.test(text),children:inline(cleanHeading(text),{size:[30,25,23][level-1],bold:true})});}
function table(headers,rows,rawWidths){
  const raw=rawWidths&&rawWidths.length===headers.length?rawWidths:headers.map(()=>1),sum=raw.reduce((a,b)=>a+b,0);
  const widths=raw.map(x=>Math.round(x/sum*WIDTH));widths[widths.length-1]+=WIDTH-widths.reduce((a,b)=>a+b,0);
  const cell=(text,i,head,n)=>new TableCell({width:{size:widths[i],type:WidthType.DXA},verticalAlign:VerticalAlign.CENTER,margins:{top:80,bottom:80,left:100,right:100},
    shading:{type:ShadingType.CLEAR,fill:head?NAVY:(n%2?'F2F4F5':'FFFFFF'),color:'auto'},
    children:[new Paragraph({alignment:/^(#|ID|Pri\.|Phase|Weight|Likelihood|Impact)$/.test(headers[i])?AlignmentType.CENTER:AlignmentType.LEFT,spacing:{after:0,before:0,line:235},widowControl:true,children:inline(text,{size:20,bold:head,color:head?'FFFFFF':'000000'})})]});
  return new Table({width:{size:WIDTH,type:WidthType.DXA},columnWidths:widths,layout:TableLayoutType.FIXED,borders:{top:border,bottom:border,left:border,right:border,insideHorizontal:border,insideVertical:border},
    rows:[new TableRow({tableHeader:true,cantSplit:true,children:headers.map((x,i)=>cell(x,i,true,0))}),...rows.map((r,n)=>new TableRow({cantSplit:true,children:headers.map((_,i)=>cell(r[i]||'',i,false,n))}))]});
}
const splitRow=line=>line.trim().replace(/^\|/,'').replace(/\|$/,'').split('|').map(x=>x.trim());
function parse(md){
  const lines=md.split(/\r?\n/),out=[];let i=0,widths=null;
  while(i<lines.length){
    const t=lines[i].trim(),wm=t.match(/^<!--\s*widths:\s*([\d,\s]+)\s*-->$/);
    if(wm){widths=wm[1].split(',').map(Number);i++;continue;}
    if(t.startsWith('<!--')){while(i<lines.length&&!lines[i].includes('-->'))i++;i++;continue;}
    if(!t){i++;continue;}
    if(t.startsWith('|')){const rows=[];while(i<lines.length&&lines[i].trim().startsWith('|'))rows.push(splitRow(lines[i++]));out.push(table(rows[0],rows.slice(1).filter(r=>!r.every(c=>/^:?-{2,}:?$/.test(c))),widths));out.push(space());widths=null;continue;}
    const hm=t.match(/^(#{1,4})\s+(.*)$/);
    if(hm){out.push(heading(Math.min(hm[1].length,3),hm[2]));i++;continue;}
    if(t.startsWith('- ')){out.push(p(t.slice(2),{numbering:{reference:'bullets',level:0},spacing:{after:75,line:260}}));i++;continue;}
    if(t.startsWith('> ')){out.push(p(t.slice(2)));i++;continue;}
    const buf=[t];i++;while(i<lines.length&&lines[i].trim()&&!/^(#|-|>|\||<!--)/.test(lines[i].trim()))buf.push(lines[i++].trim());out.push(p(buf.join(' ')));
  }
  return out;
}
const dir=path.join(__dirname,'sections'),files=fs.readdirSync(dir).filter(x=>x.endsWith('.md')).sort(),meta={};
for(const line of fs.readFileSync(path.join(dir,'00-title.md'),'utf8').split(/\r?\n/).filter(x=>x.startsWith('|'))){const r=splitRow(line);meta[r[0]]=r[1];}
const centered=(text,size,bold=false,after=180,extra={})=>new Paragraph({alignment:AlignmentType.CENTER,spacing:{after},children:inline(text,{size,bold}),...extra});
const cover=[centered('Khalifa University',32,true,120,{spacing:{before:500,after:120}}),centered('Department of Computer Science',24,false,180),centered('COSC 336  Introduction to Software Engineering',23,false,80),centered('Fall 2026',23,false,720),centered('Phase 1',28,true,140),centered('Initial Plan and Requirement Gathering Document',42,true,450,{style:'Title'}),centered(meta['Title of the project'],29,true,640),centered(meta['Prepared by'],24,false,240),centered(meta['Date of the document']+'  |  Version 1.0',22,false,400),centered('Prepared for',22,true,100),centered("Ala' Alsamarneh",22,false,70),centered('Hamdan Abdulla Naser Salem Alshkeili',22,false,200),centered('COSC 336 lab instructors and project clients',21,false,380),centered(meta['GitHub repository'],22,false,0)];
const children=[...cover,pageBreak(),new Paragraph({style:'ContentsTitle',children:inline('Contents',{size:32,bold:true}),spacing:{after:220}}),new TableOfContents('Contents',{hyperlink:true,headingStyleRange:'1-2'})];
for(const file of files.filter(x=>x!=='00-title.md'))children.push(...parse(fs.readFileSync(path.join(dir,file),'utf8')));
const style=(id,name,size,before,after,level)=>({id,name,basedOn:'Normal',next:'Normal',quickFormat:true,run:{font:FONT,size,bold:true,color:'000000'},paragraph:{spacing:{before,after},keepNext:true,...(level===undefined?{}:{outlineLevel:level})}});
const doc=new Document({creator:'COSC 336 Group 4',lastModifiedBy:'COSC 336 Group 4',title:'Initial Plan and Requirement Gathering Document',subject:meta['Title of the project'],description:'Phase 1 submission for COSC 336 Group 4',
  styles:{default:{document:{run:{font:FONT,size:22,color:'000000'},paragraph:{spacing:{after:110,line:260}}}},paragraphStyles:[style('Title','Title',42,0,450),style('ContentsTitle','Contents Title',32,0,220),style('Heading1','Heading 1',30,240,150,0),style('Heading2','Heading 2',25,210,110,1),style('Heading3','Heading 3',23,170,90,2),{id:'TOC1',name:'toc 1',basedOn:'Normal',next:'Normal',run:{font:FONT,size:22,bold:true,color:'000000'},paragraph:{spacing:{after:80,line:245}}},{id:'TOC2',name:'toc 2',basedOn:'Normal',next:'Normal',run:{font:FONT,size:21,color:'000000'},paragraph:{indent:{left:220},spacing:{after:50,line:240}}}]},
  numbering:{config:[{reference:'bullets',levels:[{level:0,format:LevelFormat.BULLET,text:'•',alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:300,hanging:180}}}}]}]},
  sections:[{properties:{titlePage:true,page:{size:{width:11906,height:16838},margin:{top:1080,bottom:1080,left:1080,right:1080,header:500,footer:500}}},headers:{default:new Header({children:[new Paragraph({alignment:AlignmentType.RIGHT,spacing:{after:0},children:inline('COSC 336  |  Group 4  |  Phase 1',{size:17})})]})},footers:{default:new Footer({children:[new Paragraph({alignment:AlignmentType.CENTER,spacing:{after:0},children:[new TextRun({text:'Page ',font:FONT,size:18,color:'000000'}),new TextRun({children:[PageNumber.CURRENT],font:FONT,size:18,color:'000000'})]})]})},children}]});
Packer.toBuffer(doc).then(buf=>{const output=path.join(__dirname,OUT);fs.writeFileSync(output,buf);console.log(`Built ${output} from ${files.length} section files.`);}).catch(e=>{console.error(e);process.exitCode=1;});
