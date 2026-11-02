// Regression checks for the approved review fixes; no backend actions are sent.
const path=require('path'),fs=require('fs');
const {chromium}=require(path.join(process.env.DAWRA_NODE_MODULES,'playwright'));
const base='file:///'+path.join(__dirname,'index.html').replaceAll('\\','/');
const check=(ok,message)=>{if(!ok)throw Error(message)};
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true});
 const page=await browser.newPage({viewport:{width:1180,height:900}});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base+'?screen=UI-07&state=down');
 await page.getByLabel('Choose alternative eligible asset AST-0071',{exact:true}).check();
 await page.locator('details').click();
 const text=await page.locator('main').innerText();
 check(!/83\s*\/\s*100|87\s*\/\s*100|compatibility 83|0\.82|27\s*\/\s*30/.test(text),'AI evidence leaked into classic fallback');
 if(process.env.DAWRA_QA_DIR)await page.screenshot({path:path.join(process.env.DAWRA_QA_DIR,'fallback-alternative-fixed.png'),fullPage:true});
 for(const view of ['dashboard','report']){
  await page.goto(base+'?screen=UI-13&view='+view);
  const normalText=await page.locator('main').innerText();
  check(['AED 690','AED 510','253.5','651.5'].every(value=>normalText.includes(value)),'Snapshot money/carbon values disagree');
  check(!/AED 900|AED 720|Carbon is N\/A|emission factors missing/.test(normalText),'Old sustainability example remains');
  check((await page.locator('.filter-status').innerText()).includes('S06'),'Initial snapshot missing');
  await page.locator('#report-from').fill('2026-11-01');await page.locator('#report-to').fill('2026-11-30');
  await page.locator('#report-department').selectOption('engineering');
  await page.getByRole('button',{name:'Apply filters',exact:true}).click();
  check(await page.getByRole('heading',{name:'No example data for these filters',exact:true}).count()===1,'Missing empty scope');
  check(!/AED 510|AED 690|253\.5|651\.5|50%|100%/.test(await page.locator('main').innerText()),'Stale S06 totals after filtering');
  await page.selectOption('#mode','down');check(await page.locator('#report-department').inputValue()==='engineering','Scope lost on AI-state change');
  const other=view==='dashboard'?'Report draft':'Dashboard';await page.getByRole('link',{name:other,exact:true}).click();
  check(await page.locator('#report-from').inputValue()==='2026-11-01','Scope lost across report views');
  check(await page.locator('.report-empty').count()===1,'Other view displayed an unrelated snapshot');
  await page.locator('#reset-report').click();
  check((await page.locator('.filter-status').innerText()).includes('S06'),'Reset did not restore snapshot');
  check((await page.locator('main').innerText()).includes('AED 510'),'Conventional totals missing with AI unavailable');
  await page.locator('#report-from').fill('2026-12-01');await page.getByRole('button',{name:'Apply filters',exact:true}).click();
  check((await page.locator('.filter-error').innerText()).includes('start date'),'Invalid date range accepted');
  check((await page.locator('.filter-status').innerText()).includes('2026-10-01'),'Invalid range changed applied scope');
 }
 check(errors.length===0,'Browser errors: '+errors.join('; '));
 for(const id of ['UI-03','UI-08']){
  await page.goto(base+'?screen='+id);
  const usedValue=await page.locator('.record-body').innerText()+' '+await page.locator('.record-body input').evaluateAll(inputs=>inputs.map(input=>input.value).join(' '));
  check(usedValue.includes('AED 250.00')&&!usedValue.includes('AED 450'),'Used monitor value mismatch: '+id);
 }
 await browser.close();console.log('Passed: updated prices/carbon, fallback score suppression, filters, empty states, persistence, reset and invalid date ranges.');
})().catch(e=>{console.error(e);process.exit(1)});
