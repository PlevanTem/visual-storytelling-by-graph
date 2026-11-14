
const data=JSON.parse(document.getElementById('conversion-data').textContent);
const select=document.getElementById('segment');
const chart=document.getElementById('rate-chart');
const title=document.getElementById('current-title');
const summary=document.getElementById('current-summary');
const tbody=document.getElementById('current-counts');
const empty=document.getElementById('empty-state');
const exportButton=document.getElementById('export-current');
document.querySelector('.interactive').hidden=false;
const fmt=v=>(v*100).toFixed(1)+'%';
const xml=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
function update(){
 const seg=select.value; const label=seg==='All'?'All sources':seg;
 const groups=['Old','New'].map(version=>{const rows=data.rows.filter(r=>r.version===version&&(seg==='All'||r.segment===seg));const n=rows.reduce((s,r)=>s+r.n,0),k=rows.reduce((s,r)=>s+r.success,0);return{version,n,k,rate:n?k/n:null}});
 title.textContent=label+' / conversion rate';
 const has=groups.every(r=>r.n>0);chart.hidden=!has;chart.style.display=has?'block':'none';empty.hidden=has;exportButton.disabled=!has;
 empty.textContent=has?'':'No observations for '+label+'. A conversion rate cannot be computed.';
 tbody.replaceChildren();
 for(const r of groups){const tr=document.createElement('tr');tr.dataset.version=r.version;for(const value of [r.version,r.n?r.k:'—',r.n||'—',r.rate===null?'Not available':fmt(r.rate)]){const td=document.createElement('td');td.textContent=value;tr.append(td)}tbody.append(tr)}
 if(!has){summary.textContent='No data for '+label+'. Missing observations are not a 0% rate.';chart.innerHTML='<title>No observations</title>';return}
 const delta=(groups[1].rate-groups[0].rate)*100;
 summary.textContent=label+': Old '+fmt(groups[0].rate)+' ('+groups[0].k+'/'+groups[0].n+'); New '+fmt(groups[1].rate)+' ('+groups[1].k+'/'+groups[1].n+'). New − Old: '+(delta>=0?'+':'−')+Math.abs(delta).toFixed(1)+' pp.';
 let svg='<title id="live-title">'+xml(title.textContent)+'</title><desc id="live-desc">'+xml(summary.textContent)+' Synthetic data, observational groups.</desc><rect width="640" height="240" fill="#fffdf8"/>';
 for(const tick of [0,.25,.5,.75,1]){const x=85+tick*430;svg+='<line x1="'+x+'" x2="'+x+'" y1="30" y2="174" stroke="#d9e0d9"/><text x="'+x+'" y="200" text-anchor="middle" font-size="16" fill="#576b68">'+fmt(tick)+'</text>'}
 groups.forEach((r,i)=>{const y=56+i*70,color=i?'#087f74':'#71838f';svg+='<text x="12" y="'+(y+23)+'" font-size="20" fill="#18312f">'+r.version+'</text><rect data-version="'+r.version+'" data-rate="'+r.rate+'" x="85" y="'+y+'" width="'+(r.rate*430)+'" height="30" fill="'+color+'"/><text x="'+(95+r.rate*430)+'" y="'+(y+23)+'" font-size="19" fill="'+color+'">'+fmt(r.rate)+'</text>'});
 svg+='<text x="12" y="229" font-size="14" fill="#576b68">Synthetic data · '+xml(label)+' · counts and denominators in accessible table</text>';chart.innerHTML=svg;
}
select.addEventListener('change',update);
document.getElementById('reset-filter').addEventListener('click',()=>{select.value='All';update()});
exportButton.addEventListener('click',()=>{if(exportButton.disabled)return;const clone=chart.cloneNode(true);clone.setAttribute('xmlns','http://www.w3.org/2000/svg');const blob=new Blob([new XMLSerializer().serializeToString(clone)],{type:'image/svg+xml'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download='conversion-'+select.value.toLowerCase()+'.svg';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)});
update();
