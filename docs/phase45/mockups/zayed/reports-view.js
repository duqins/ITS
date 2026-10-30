// UI-13 has dashboard and report views; both use the same synthetic S06 records.
const reportView=new URL(location.href).searchParams.get('view')==='report';
const ui13=data.find(s=>s.id==='UI-13');
if(reportView){
 ui13.title='Review report draft';
 ui13.actions=['Open source records','Return draft with comments','Approve sustainability figures'];
 const originalContent=content;
 content=function(s){
  if(s.id!=='UI-13')return originalContent(s);
  return `<div class="filter-row">${[0,1,2].map(i=>`<div class="filter-item"><strong>${esc(s.fields[i][0])}</strong>${esc(s.fields[i][1])}</div>`).join('')}</div>
  <div class="pending-note">${icon('clock')}Draft S06. Sustainability, Finance and Business administration reviews are pending.</div>
  <section class="group"><div class="group-title">${icon('file')}<h2>AI-generated report draft</h2></div>
  <p class="view-description">Synthetic October 2026 example. Verify each statement against the source totals.</p>
  <p>Two fulfilled requests avoided an estimated AED 900 in purchases. After AED 180 in related costs, estimated net savings are AED 720.</p>
  <p>Three distinct items were diverted from waste: two through reuse and one through repair. The reuse rate is 50% (2 of 4 listed items). One of one closed repairs succeeded.</p>
  <p>Carbon reduction and asset-life extension are N/A because emission factors and retirement dates are missing.</p></section>
  <div class="group-title">${icon('check')}<h2>Source and review evidence</h2></div>
  <div class="table-wrap"><table class="data-table"><thead><tr><th>Claim</th><th>Source / basis</th><th>Data owner</th></tr></thead><tbody>
  <tr><td>Two fulfilled requests</td><td>TRF-0007, TRF-0008; reviewer confirmations</td><td>Business administration</td></tr>
  <tr><td>AED 720 estimated savings</td><td>AED 900 avoided purchases less AED 180 related costs; S06</td><td>Finance</td></tr>
  <tr><td>3 items; 50% reuse; 100% repair</td><td>Distinct items; 2 of 4 listed items; MWO-0012</td><td>Sustainability</td></tr>
  <tr><td>Carbon and life extension N/A</td><td>Required inputs missing; no AI estimate used</td><td>Sustainability</td></tr>
  </tbody></table></div>
  `;
 };
 subtitles['UI-13']='Check the written draft against its sources. Approve only your assigned area.';
}else{
 ui13.title='Sustainability dashboard';
 subtitles['UI-13']='Inspect period totals and missing inputs before reviewing the written report.';
}
const originalRender=render;
render=function(){
 originalRender();
 if(data[current].id!=='UI-13')return;
 const controls=document.createElement('nav');controls.className='report-view-tabs';controls.setAttribute('aria-label','Reports and sustainability views');
 controls.innerHTML=`<a href="?screen=UI-13&view=dashboard&state=${mode.value}" ${!reportView?'aria-current="page"':''}>Dashboard</a><a href="?screen=UI-13&view=report&state=${mode.value}" ${reportView?'aria-current="page"':''}>Report draft</a>`;
 document.querySelector('.lead').after(controls);
 if(reportView&&mode.value==='down'){
  document.querySelector('.record-body .group').innerHTML='<div class="group-title">'+icon('info')+'<h2>AI narrative unavailable</h2></div><p class="view-description">No new AI draft was generated. The source totals below remain available for conventional reporting and owner review.</p>';
 }
};
select.onchange=render;mode.onchange=render;render();
