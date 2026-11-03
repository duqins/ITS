// Use the bundled Node packages directory through DAWRA_NODE_MODULES.
const fs=require('fs'),path=require('path');
const packages=process.env.DAWRA_NODE_MODULES;
const {chromium}=require(packages?path.join(packages,'playwright'):'playwright');
const root=path.resolve(__dirname,'../..');
const qa=process.env.DAWRA_QA_DIR;
const screens=[['UI-03','figure-7-1-ui-03'],['UI-06','figure-7-2-ui-06'],['UI-07','figure-7-3-ui-07'],['UI-08','figure-7-4-ui-08'],['UI-09','figure-7-5-ui-09'],['UI-10','figure-7-6-ui-10'],['UI-13','figure-7-7-ui-13-dashboard','dashboard'],['UI-13','figure-7-8-ui-13-reports','report'],['UI-12','figure-7-9-ui-12']];
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true});
 const page=await browser.newPage({viewport:{width:1180,height:900},deviceScaleFactor:1.6});
 const errors=[],checks=[];page.on('pageerror',e=>errors.push(e.message));
 const requested=process.env.DAWRA_CAPTURE_SCREENS?.split(',');
 for(const [id,name,view] of screens.filter(([id])=>!requested||requested.includes(id))){
  const url='file:///'+path.join(__dirname,'index.html').replaceAll('\\','/')+'?screen='+id+(view?'&view='+view:'');
  await page.goto(url);await page.evaluate(()=>document.fonts.ready);
  if(qa){
   const bounds=await page.locator('#app').boundingBox();
   await page.setViewportSize({width:1180,height:Math.ceil(bounds.y+bounds.height+5)});
   await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
   await page.locator('#app').screenshot({path:path.join(qa,name+'-normal.png'),animations:'disabled'});
   await page.setViewportSize({width:1180,height:900});
  }
  const desktop=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth}));
  await page.selectOption('#mode','down');
  if(!await page.locator('.ai').innerText().then(t=>t.includes('unavailable')))throw Error('Missing fallback: '+id);
  if(view&&qa){await page.locator('#app').screenshot({path:path.join(qa,name+'-down.png')});}
  await page.selectOption('#mode','low');
  if(view&&qa){await page.locator('#app').screenshot({path:path.join(qa,name+'-low.png')});}
  await page.setViewportSize({width:390,height:844});await page.goto(url);await page.evaluate(()=>document.fonts.ready);
  const mobile=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth}));
  if(view&&qa)await page.screenshot({path:path.join(qa,name+'-mobile.png'),fullPage:true});
  if(desktop.width!==desktop.scroll||mobile.width!==mobile.scroll)throw Error('Page overflow: '+id+' '+view);
  await page.setViewportSize({width:1180,height:900});await page.goto(url);await page.evaluate(()=>document.fonts.ready);
  const print=await require('./print-capture.cjs')({page,root,name});
  checks.push({id,view,desktop,mobile,print});await page.setViewportSize({width:1180,height:900});
 }
 await browser.close();if(errors.length)throw Error(errors.join('\n'));
 if(qa){
  const file=path.join(qa,'browser-checks.json');
  const previous=requested&&fs.existsSync(file)?JSON.parse(fs.readFileSync(file,'utf8')).checks:[];
  const merged=previous.filter(old=>!checks.some(now=>now.id===old.id&&now.view===old.view)).concat(checks);
  fs.writeFileSync(file,JSON.stringify({errors,checks:merged},null,2));
 }
 console.log('Captured nine views and eighteen readable print halves. No browser errors or page overflow.');
})().catch(e=>{console.error(e);process.exit(1)});
