// Capture a narrow print layout in two readable, continuous page-width halves.
const fs=require('fs'),path=require('path');
module.exports=async function capturePrint({page,root,name}){
 await page.setViewportSize({width:1000,height:1000});
 await page.addStyleTag({content:fs.readFileSync(path.join(__dirname,'print-capture.css'),'utf8')+'\n.preview{display:none}'});
 await page.evaluate(()=>{
  const app=document.querySelector('#app');app.classList.add('print-capture');
  app.querySelectorAll('input:not([type=radio]),select,textarea').forEach(control=>{
   const value=document.createElement('div');value.className='capture-value';value.id=control.id;
   value.textContent=control.tagName==='SELECT'?control.selectedOptions[0]?.textContent:control.value;
   control.replaceWith(value);
  });
  app.querySelectorAll('*').forEach(el=>{
   const size=parseFloat(getComputedStyle(el).fontSize);
   if(size<15)el.style.setProperty('font-size','15px','important');
  });
  // Clear a common horizontal seam in the two columns without cutting a line.
  const originalBox=app.getBoundingClientRect(),seam=Math.round(originalBox.height/2);
  const moved=new Set();
  for(let pass=0;pass<3;pass++){
   const crossing=new Set(),walk=document.createTreeWalker(app,NodeFilter.SHOW_TEXT);
   for(let node;node=walk.nextNode();){
    if(!node.textContent.trim())continue;
    const range=document.createRange();range.selectNodeContents(node);
    if([...range.getClientRects()].some(r=>r.width&&r.top-originalBox.top<seam+3&&r.bottom-originalBox.top>seam-3)){
     // text in an AI-panel part moves the whole part, so its heading stays with it
     crossing.add(node.parentElement.closest('.reason,.human')||node.parentElement.closest('p,td,th,.readonly,.capture-value,label,.pending-note,.group-title,li')||node.parentElement);
    }
   }
   // a field that spans the seam, or a heading left just above it, moves below the seam with what follows
   for(const el of app.querySelectorAll('.field')){const r=el.getBoundingClientRect();if(!moved.has(el)&&r.top-originalBox.top<seam-3&&r.bottom-originalBox.top>seam+3)crossing.add(el);}
   for(const el of app.querySelectorAll('.group-title,.reason>strong,.human>strong')){const r=el.getBoundingClientRect();if(r.bottom-originalBox.top>seam-90&&r.top-originalBox.top<seam+3&&!moved.has(el.closest('.reason,.human')||el))crossing.add(el.closest('.reason,.human')||el);}
   if(!crossing.size)break;
   // a table cell that crosses the seam moves its whole row, so a label never splits from its value
   for(const cell of [...crossing])if(cell.tagName==='TD'||cell.tagName==='TH')for(const c of cell.parentElement.children)crossing.add(c);
   for(const block of crossing){
    if(moved.has(block))continue;moved.add(block);
    const top=block.getBoundingClientRect().top-originalBox.top;
    block.style.paddingTop=(parseFloat(getComputedStyle(block).paddingTop)+Math.max(8,seam+8-top))+'px';
   }
  }
  window.__printSeam=seam;
 });
 const metrics=await page.evaluate(()=>{
  const app=document.querySelector('#app'),box=app.getBoundingClientRect(),lines=[];
  const walk=document.createTreeWalker(app,NodeFilter.SHOW_TEXT);
  for(let node;node=walk.nextNode();){
   if(!node.textContent.trim())continue;
   const range=document.createRange();range.selectNodeContents(node);
   for(const r of range.getClientRects())if(r.width&&r.height)lines.push([r.top-box.top,r.bottom-box.top]);
  }
  const height=Math.ceil(box.height),middle=height/2;
  let cut=null,score=Infinity;
  if(!lines.some(([top,bottom])=>top<window.__printSeam+2&&bottom>window.__printSeam-2))cut=window.__printSeam;
  for(let y=Math.floor(middle-150);y<=Math.ceil(middle+150);y++){
   if(y<40||height-y<40)continue;
   if(lines.some(([top,bottom])=>top<y+2&&bottom>y-2))continue;
   if(cut===null&&Math.abs(y-middle)<score){cut=y;score=Math.abs(y-middle);}
  }
  if(cut===null)throw Error('No clear line boundary for '+document.title);
  const textNodes=[...app.querySelectorAll('*')].filter(el=>el.childNodes.length&&[...el.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())&&el.getBoundingClientRect().height);
  const minPx=Math.min(...textNodes.map(el=>parseFloat(getComputedStyle(el).fontSize)));
  return {x:box.x,y:box.y,width:box.width,height,cut,minPx,printedMinPt:minPx*465/box.width};
 });
 await page.setViewportSize({width:1000,height:metrics.height+2});
 const overlap=0;
 const halves=[['top',0,metrics.cut+overlap],['bottom',metrics.cut-overlap,metrics.height-metrics.cut+overlap]];
 for(const [half,y,height] of halves){
  if(height>1030)throw Error(name+' '+half+' is too tall for readable print: '+height+' CSS px');
  await page.screenshot({path:path.join(root,'images',name+'-'+half+'.png'),clip:{x:metrics.x,y:metrics.y+y,width:metrics.width,height},animations:'disabled'});
 }
 if(metrics.printedMinPt<9)throw Error('Print type below 9 pt: '+name);
 return metrics;
};
