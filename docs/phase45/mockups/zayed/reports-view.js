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
  <p>Two fulfilled requests each received one 24-inch Dell P2422H monitor. Avoided purchases are an estimated AED 690 (2 x AED 345). After AED 180 related costs, estimated net savings are AED 510.</p>
  <p>Three distinct items were diverted from waste: two through reuse and one through repair. The reuse rate is 50% (2 of 4 listed items). One of one closed repairs succeeded.</p>
  <p>Estimated carbon reduction is about 253.5 to 651.5 kg CO2e. The gross range is 256 to 654, less about 2.49 for the new fan. Same-building collection uses no van trip. Asset-life extension remains N/A because retirement dates are missing.</p></section>
  <div class="group-title">${icon('check')}<h2>Source and review evidence</h2></div>
  <div class="table-wrap"><table class="data-table"><thead><tr><th>Claim</th><th>Source / basis</th><th>Data owner</th></tr></thead><tbody>
  <tr><td>Two monitors in two fulfilled requests</td><td>TRF-0007 / REQ-0014 and TRF-0008 / REQ-0016. Reviewer confirmations</td><td>Business administration</td></tr>
  <tr><td>AED 510 estimated savings</td><td>AED 690 avoided purchases minus AED 180 related costs. S06</td><td>Finance</td></tr>
  <tr><td>3 items; 50% reuse; 100% repair</td><td>Distinct items; 2 of 4 listed items; MWO-0012</td><td>Sustainability</td></tr>
  <tr><td>About 253.5 to 651.5 kg CO2e</td><td>Section 12: 2 x (128 to 327) minus 0.10 x 24.86548. Synthetic fan mass and IT-material proxy. Transport 0.</td><td>Sustainability</td></tr><tr><td>Life extension N/A</td><td>Retirement dates missing.</td><td>Sustainability</td></tr>
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
