// Applied report scope is shared by the two UI-13 views and AI-state examples.
const snapshotScope={from:'2026-10-01',to:'2026-10-31',department:'both'};
const scopeUrl=new URL(location.href);
const dateValue=(key,fallback)=>/^\d{4}-\d{2}-\d{2}$/.test(scopeUrl.searchParams.get(key)||'')?scopeUrl.searchParams.get(key):fallback;
let appliedScope={from:dateValue('from',snapshotScope.from),to:dateValue('to',snapshotScope.to),department:['both','engineering','computing'].includes(scopeUrl.searchParams.get('department'))?scopeUrl.searchParams.get('department'):'both'};
if(appliedScope.from>appliedScope.to)appliedScope={...snapshotScope};
let draftScope={...appliedScope};
const hasSnapshot=()=>Object.keys(snapshotScope).every(k=>appliedScope[k]===snapshotScope[k]);
const departmentNames={both:'Engineering and Computing',engineering:'Engineering',computing:'Computing'};
function scopeControls(){
 return `<form class="report-filters" aria-label="Report filters"><div class="filter-type"><strong>Report type</strong><span>Sustainability and resource exchange</span></div><div class="filter-dates"><label for="report-from">From<input id="report-from" type="date" required value="${esc(draftScope.from)}"></label><label for="report-to">To<input id="report-to" type="date" required value="${esc(draftScope.to)}"></label></div><label for="report-department">Department<select id="report-department">${Object.entries(departmentNames).map(([v,n])=>`<option value="${v}" ${v===draftScope.department?'selected':''}>${n}</option>`).join('')}</select></label><div class="filter-buttons"><button type="submit" class="button primary">Apply filters</button><button type="button" class="button" id="reset-report">Reset to example</button></div><p class="filter-status" aria-live="polite">Applied: ${esc(appliedScope.from)} to ${esc(appliedScope.to)} · ${esc(departmentNames[appliedScope.department])}. ${hasSnapshot()?'Example snapshot S06.':'No example snapshot for this scope.'}</p><p class="filter-error" role="alert"></p></form>`;
}
const renderBeforeFilters=render;
render=function(){
 renderBeforeFilters();
 if(data[current].id!=='UI-13')return;
 const body=document.querySelector('.record-body');
 if(hasSnapshot())body.querySelector('.filter-row').outerHTML=scopeControls();
 else{
  body.innerHTML=scopeControls()+'<section class="report-empty"><h2>No example data for these filters</h2><p>This preview contains only October 2026 for Engineering and Computing together. Totals and AI text are unavailable for the applied scope. Reset to the example to review S06.</p></section>';
  document.querySelector('.ai').outerHTML=aiPanel({...ui13,confidence:null,ai:'No report draft for the applied scope.',low:'No report draft for the applied scope.',down:'AI unavailable. No conventional example snapshot exists for this scope.',reason:'No supporting source snapshot is included for these filters.',decision:'Change the filters or reset to the example before reviewing figures.'},mode.value);
  document.querySelector('.actions').hidden=true;
  document.querySelector('main > details').hidden=true;
  document.querySelector('.down').hidden=true;
  document.querySelector('.record').textContent='No example snapshot · UI-13';
  document.querySelector('.status').innerHTML='<i></i>No example data';
 }
 const form=body.querySelector('form');
 document.querySelector('.layout').before(form);
 const readDraft=()=>({from:form.querySelector('#report-from').value,to:form.querySelector('#report-to').value,department:form.querySelector('#report-department').value});
 form.oninput=()=>{draftScope=readDraft();};
 form.onsubmit=e=>{
  e.preventDefault();draftScope=readDraft();
  if(!draftScope.from||!draftScope.to||draftScope.from>draftScope.to){form.querySelector('.filter-error').textContent='Choose a start date on or before the end date, then apply again.';form.querySelector('#report-to').focus();return;}
  appliedScope={...draftScope};render();
 };
 form.querySelector('#reset-report').onclick=()=>{appliedScope={...snapshotScope};draftScope={...snapshotScope};render();};
 const url=new URL(location.href);
 for(const [k,v] of Object.entries(appliedScope))url.searchParams.set(k,v);
 history.replaceState(null,'',url);
 document.querySelectorAll('.report-view-tabs a').forEach(a=>{const next=new URL(a.href);for(const [k,v] of Object.entries(appliedScope))next.searchParams.set(k,v);a.href=next;});
};
select.onchange=render;mode.onchange=render;render();
