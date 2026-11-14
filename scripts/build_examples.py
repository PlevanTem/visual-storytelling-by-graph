"""Rebuild eight fixed, synthetic design examples (not a general chart engine).

Python standard library only. Inputs are preserved in evals/fixtures.
"""
import hashlib
import html
import json
import math
import textwrap
from datetime import datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'examples'
INK='#18312f'; MUTED='#576b68'; GRID='#d9e0d9'; PAPER='#fffdf8'
TEAL='#087f74'; ORANGE='#b34f2e'; OLD='#71838f'; FAINT='#bfcfc8'
def load(name):return json.loads((ROOT/'evals/fixtures'/f'{name}.json').read_text(encoding='utf-8'))
def esc(s):return html.escape(str(s),quote=True)
def quantile(xs,p):return sorted(xs)[math.ceil(p*len(xs))-1]
def fnum(n):return f'{n:g}'

class SVG:
    def __init__(self,case,title,subtitle,mobile=False,height=None):
        self.mobile=mobile;self.w=620 if mobile else 1000;self.h=height or (680 if mobile else 610)
        self.pad=38 if mobile else 58; self.font=22 if mobile else 16
        self.items=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" role="img" aria-labelledby="title desc" font-family="Segoe UI, Arial, sans-serif">',f'<title id="title">{esc(title)}</title>',f'<desc id="desc">{esc(subtitle)}. Synthetic demonstration data. {case}.</desc>',f'<rect width="{self.w}" height="{self.h}" fill="{PAPER}"/>']
        y=self.wrap(self.pad,46,title,29 if mobile else 33,self.w-2*self.pad,INK,weight=650)
        y=self.wrap(self.pad,y+12,subtitle,20 if mobile else 16,self.w-2*self.pad,MUTED)
        self.line(self.pad,y+12,self.w-self.pad,y+12,GRID)
        self.top=y+43;self.bottom=self.h-185
    def add(self,s):self.items.append(s)
    def text(self,x,y,s,size=None,fill=INK,anchor='start',weight=400,attrs=''):
        self.add(f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size or self.font}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" {attrs}>{esc(s)}</text>')
    def wrap(self,x,y,s,size,width,fill=INK,weight=400):
        lines=textwrap.wrap(s,width=max(12,int(width/(size*.51)))) or ['']
        for line in lines:self.text(x,y,line,size,fill,weight=weight);y+=size*1.3
        return y
    def line(self,x1,y1,x2,y2,stroke=GRID,width=1,attrs=''):
        self.add(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{stroke}" stroke-width="{width}" {attrs}/>')
    def rect(self,x,y,w,h,fill,attrs=''):
        self.add(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{fill}" {attrs}/>')
    def circle(self,x,y,r,fill,attrs=''):
        self.add(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{fill}" {attrs}/>')
    def path(self,d,stroke,width=2,attrs=''):
        self.add(f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{width}" stroke-linejoin="round" {attrs}/>')
    def footer(self,summary,note):
        y=self.h-106
        y=self.wrap(self.pad,y,summary,20 if self.mobile else 19,self.w-2*self.pad,INK,weight=600)
        self.wrap(self.pad,y+9,note,20 if self.mobile else 14,self.w-2*self.pad,MUTED)
    def finish(self):return '\n'.join(self.items+['</svg>'])

def revenue(m=False):
    d=load('revenue');s=SVG('C01','New business drives a $300k net increase','Q3 to Q4 revenue bridge / USD thousands',m)
    left=s.pad+35;right=s.w-s.pad;top=s.top;bottom=s.bottom;yw=lambda v:bottom-v/1800*(bottom-top)
    for tick in [0,600,1200,1800]:
        yy=yw(tick);s.line(left,yy,right,yy);s.text(left-12,yy+6,str(tick),s.font-1,MUTED,'end')
    values=[('Opening',0,d['opening'])];running=d['opening']
    for row in d['contributions']:values.append((row['label'],running,running+row['value']));running+=row['value']
    values.append(('Closing',0,d['closing']))
    step=(right-left)/6;bw=step*.65
    for i,(label,start,end) in enumerate(values):
        x=left+step*(i+.175);color=INK if i in [0,5] else TEAL if end>=start else ORANGE
        s.rect(x,yw(max(start,end)),bw,abs(yw(start)-yw(end)),color,f'data-mark="bridge" data-index="{i}" data-start="{start}" data-end="{end}"')
        val=end if i in [0,5] else end-start
        s.text(x+bw/2,yw(max(start,end))-12,('+' if 0<i<5 and val>0 else '')+str(val),s.font,color,'middle',600)
        if i<5:s.line(x+bw,yw(end),left+step*(i+1+.175),yw(end),MUTED,1,attrs='stroke-dasharray="3 4"')
        label={'New business':'New','Contraction':'Downsell'}.get(label,label)
        if m and label=='Expansion':label='Expand'
        s.text(x+bw/2,bottom+30,label,20 if m else 15,MUTED,'middle')
    s.footer('Net +$300k. Gross losses: $200k.','Synthetic data. Opening 1,200 + 320 + 180 - 90 - 110 = closing 1,500.')
    return s

def latency(m=False):
    d=load('latency');s=SVG('C02','Median improves. Tail latency worsens.','Independent request samples / latency in ms',m)
    left=s.pad+45;right=s.w-s.pad-10;top=s.top+13;bottom=s.bottom
    X=lambda v:left+v/1500*(right-left);Y=lambda v:bottom-v*(bottom-top)
    for f in [0,.5,1]:s.line(left,Y(f),right,Y(f));s.text(left-12,Y(f)+6,f'{f:.0%}',s.font-1,MUTED,'end')
    for v in [0,500,1000,1500]:s.text(X(v),bottom+28,str(v),s.font-1,MUTED,'middle')
    s.text(left,top-21,'Share at or below latency',s.font-1,MUTED)
    for key,color,dash in [('before',OLD,'stroke-dasharray="6 4"'),('after',TEAL,'')]:
        xs=sorted(d[key]);path=f'M {X(0):.2f} {Y(0):.2f}'
        for i,x in enumerate(xs):path+=f' H {X(x):.2f} V {Y((i+1)/len(xs)):.2f}'
        path+=f' H {X(1500):.2f}';s.path(path,color,3,f'data-mark="ecdf" data-series="{key}" {dash}')
    s.line(X(500),top,X(500),bottom,ORANGE,1.5,'stroke-dasharray="4 4"')
    s.text(X(500)+8,bottom-13,'500 ms',s.font-1,ORANGE)
    lx=right-210;s.line(lx,top-27,lx+25,top-27,OLD,3,'stroke-dasharray="6 4"');s.text(lx+34,top-21,'Before',s.font-1,OLD)
    lx=right-95;s.line(lx,top-27,lx+25,top-27,TEAL,3);s.text(lx+34,top-21,'After',s.font-1,TEAL)
    s.footer('p50: 200 → 150 ms  /  p95: 480 → 900 ms','Synthetic, n=20 per version; nearest-rank quantiles. Over 500 ms: 5% → 20%.')
    return s

def paired(m=False):
    d=load('paired');s=SVG('C03','11 of 12 participants finish faster','Same participants before and after / completion time in seconds',m)
    left=s.pad+55;right=s.w-s.pad-85;top=s.top;bottom=s.bottom
    X1=left+55;X2=right-45;Y=lambda v:bottom-(v-35)/45*(bottom-top)
    for v in [40,50,60,70,80]:s.line(left,Y(v),right,Y(v));s.text(left-12,Y(v)+6,str(v),s.font-1,MUTED,'end')
    for p in d['participants']:
        slow=p['after']>p['before'];color=ORANGE if slow else FAINT
        s.line(X1,Y(p['before']),X2,Y(p['after']),color,3 if slow else 2,attrs=f'data-mark="pair" data-id="{p["id"]}"')
        for key,x in [('before',X1),('after',X2)]:s.circle(x,Y(p[key]),5,color,f'data-mark="paired-point" data-id="{p["id"]}" data-period="{key}" data-value="{p[key]}"')
        if slow:s.text(X2+14,Y(p['after'])+6,p['id']+'  +2 s',s.font,ORANGE,weight=600)
    s.text(X1,bottom+32,'Before',s.font,MUTED,'middle');s.text(X2,bottom+32,'After',s.font,MUTED,'middle')
    s.footer('Median paired change: -6 seconds.','Synthetic complete pairs, n=12. Lower is faster; no control group or causal attribution.')
    return s

def conversion(m=False):
    d=load('conversion');s=SVG('C04','A pooled decline hides two source-level gains','Conversion rate / % of observations in each group',m,760 if m else 650)
    left=145 if m else 200;right=s.w-s.pad-25;top=s.top+40;bottom=s.bottom-12;X=lambda v:left+v*(right-left)
    for v in [0,.25,.5,.75,1]:s.line(X(v),top-30,X(v),bottom+8);s.text(X(v),bottom+36,f'{v:.0%}',s.font-1,MUTED,'middle')
    groups=['All','Organic','Paid']
    for i,group in enumerate(groups):
        y=top+i*(bottom-top-55)/2
        s.text(left-20,y+6,group,s.font,INK,'end',600)
        rates=[]
        for version,color in [('Old',OLD),('New',TEAL)]:
            rows=[r for r in d['rows'] if r['version']==version and (group=='All' or r['segment']==group)]
            n=sum(r['n'] for r in rows);k=sum(r['success'] for r in rows);rate=k/n;rates.append((version,color,rate,k,n))
        s.line(X(rates[0][2]),y,X(rates[1][2]),y,FAINT,5)
        for version,color,rate,k,n in rates:
            s.circle(X(rate),y,7,color,f'data-mark="rate" data-group="{group}" data-version="{version}" data-value="{rate}"')
            s.text(X(rate),y-18 if version=='Old' else y+32,f'{version} {rate:.1%}',s.font,color,'middle',600)
    s.footer('Pooled: 50.0% → 34.5%; both source rates rise.','Synthetic. All Old 100/200, New 69/200; Organic 80/100, 27/30; Paid 20/100, 42/170. Observational.')
    return s

def sensor_segments(d):
    segments=[];current=[];prev=None
    for r in d['readings']:
        t=datetime.fromisoformat(r['time'])
        if r['value'] is None:
            if current:segments.append(current)
            current=[];prev=None;continue
        if prev and (t-prev).total_seconds()>45*60:
            if current:segments.append(current)
            current=[]
        current.append(r);prev=t
    if current:segments.append(current)
    return segments

def sensor(m=False):
    d=load('sensor');s=SVG('C05','Keep missing coverage visible','Temperature in °C / local time UTC+08:00',m)
    left=s.pad+40;right=s.w-s.pad;top=s.top;bottom=s.bottom
    start=datetime.fromisoformat(d['readings'][0]['time']);end=datetime.fromisoformat(d['readings'][-1]['time'])
    X=lambda t:left+(datetime.fromisoformat(t)-start).total_seconds()/(end-start).total_seconds()*(right-left)
    Y=lambda v:bottom-(v-45)/40*(bottom-top)
    s.rect(left,top,right-left,Y(70)-top,'#faeee5')
    for a,b in [('09:30','11:00'),('13:00','14:30')]:
        x1=X('2026-11-12T'+a+':00+08:00');x2=X('2026-11-12T'+b+':00+08:00')
        s.rect(x1,top,x2-x1,bottom-top,'#e9ece7')
    for v in [50,60,70,80]:s.line(left,Y(v),right,Y(v));s.text(left-12,Y(v)+6,str(v),s.font-1,MUTED,'end')
    s.line(left,Y(70),right,Y(70),ORANGE,1.5,'stroke-dasharray="5 4"');s.text(right-3,Y(70)-10,'70°C threshold',s.font-1,ORANGE,'end')
    for segment in sensor_segments(d):
        path=' '.join(('M' if i==0 else 'L')+f' {X(r["time"]):.2f} {Y(r["value"]):.2f}' for i,r in enumerate(segment))
        s.path(path,TEAL,3,'data-mark="observed-segment"')
    for r in d['readings']:
        if r['value'] is not None:
            s.circle(X(r['time']),Y(r['value']),4.5,ORANGE if r['value']>70 else TEAL,f'data-mark="sensor" data-time="{r["time"]}" data-value="{r["value"]}"')
    for hour in [8,10,12,14,16]:s.text(X(f'2026-11-12T{hour:02}:00:00+08:00'),bottom+30,f'{hour:02}:00',s.font-1,MUTED,'middle')
    s.footer('13 observations. 2 samples exceed 70°C.','Synthetic. Gray bands mark gaps; 2 explicit missing readings. Continuous exceedance duration is unknown.')
    return s

def geography(m=False):
    d=load('geography');s=SVG('C06','Capacity and intensity answer different questions','Monthly service requests / totals and requests per 1,000 residents',m,850 if m else 610)
    if m:panels=[(s.pad+105,s.w-s.pad-25,s.top+40,'Requests',1000,'requests'),(s.pad+105,s.w-s.pad-25,s.top+300,'Per 1,000 residents',10,'rate')]
    else:panels=[(s.pad+110,450,s.top+42,'Requests',1000,'requests'),(650,940,s.top+42,'Per 1,000 residents',10,'rate')]
    for left,right,top,label,maxv,key in panels:
        s.text(left,top-23,label,s.font,INK,weight=600)
        for tick in [0,maxv/2,maxv]:
            x=left+tick/maxv*(right-left);s.line(x,top-3,x,top+153);s.text(x,top+184,fnum(tick),s.font-1,MUTED,'middle')
        for i,r in enumerate(d['rows']):
            y=top+12+i*43;v=r['requests'] if key=='requests' else r['requests']/r['population']*1000
            x=left+v/maxv*(right-left);color=TEAL if key=='requests' and r['region']=='North' else ORANGE if key=='rate' and r['region']=='South' else OLD
            s.text(left-13,y+6,r['region'],s.font-1,MUTED,'end');s.line(left,y,x,y,FAINT,3)
            s.circle(x,y,6,color,f'data-mark="geo" data-region="{r["region"]}" data-metric="{key}" data-value="{v}"')
            s.text(x+12,y+6,fnum(v),s.font-1,color,weight=600)
    s.footer('North: highest volume. South: highest intensity.','Synthetic. Population-normalized rates do not replace total demand when planning capacity.')
    return s

def uncertainty(m=False):
    d=load('uncertainty');s=SVG('C07',"A's interval is above zero. B is imprecise.",'Conversion-rate difference / percentage points vs control',m)
    left=s.pad+65;right=s.w-s.pad-30;top=s.top+25;bottom=s.bottom;X=lambda v:left+(v+2)/6*(right-left)
    for v in [-2,-1,0,1,2,3,4]:
        s.line(X(v),top-10,X(v),bottom+8,INK if v==0 else GRID,1.5 if v==0 else 1,'stroke-dasharray="4 4"' if v==0 else '')
        s.text(X(v),bottom+35,str(v),s.font-1,MUTED,'middle')
    for i,r in enumerate(d['rows']):
        y=top+25+i*(bottom-top-45)/2;color=TEAL if r['variant']=='A' else ORANGE if r['variant']=='B' else OLD
        s.text(left-22,y+6,r['variant'],s.font,INK,'end',600)
        s.line(X(r['low']),y,X(r['high']),y,color,4,f'data-mark="interval" data-variant="{r["variant"]}"')
        s.line(X(r['low']),y-8,X(r['low']),y+8,color,2);s.line(X(r['high']),y-8,X(r['high']),y+8,color,2)
        s.circle(X(r['estimate']),y,7,color,f'data-mark="estimate" data-variant="{r["variant"]}" data-value="{r["estimate"]}"')
        s.text(X(r['estimate']),y-23,f'{r["estimate"]:+.1f} [{r["low"]:+.1f}, {r["high"]:+.1f}]',s.font-1,color,'middle')
    s.footer('Intervals are supplied 95% confidence intervals.','Synthetic. Sample sizes A=400, B=100, C=380. Intervals were not re-estimated; containing zero does not prove no effect.')
    return s

def money(cents):return ('-' if cents<0 else '')+f'${abs(cents)/100:,.2f}'
def ledger(m=False):
    d=load('ledger');s=SVG('C08','A table keeps every cent traceable','Accounts payable / USD, credits retained',m)
    xs=[s.pad,s.w*.34,s.w*.57,s.w-s.pad];top=s.top+15;step=47 if m else 48
    for x,label in zip(xs,['Vendor','Invoice','Due','USD']):s.text(x,top,label,s.font-1,MUTED,'end' if x==xs[-1] else 'start',600)
    s.line(s.pad,top+15,s.w-s.pad,top+15)
    for i,r in enumerate(d['rows']):
        y=top+(i+1)*step+10;s.text(xs[0],y,r['vendor'],s.font-1);s.text(xs[1],y,r['invoice'],s.font-1)
        due='Nov '+r['due'][-2:] if m else r['due'];s.text(xs[2],y,due,s.font-1,MUTED)
        s.text(xs[3],y,money(r['amount_cents']),s.font-1,ORANGE if r['amount_cents']<0 else INK,'end',attrs=f'data-mark="amount" data-cents="{r["amount_cents"]}"')
        s.line(s.pad,y+16,s.w-s.pad,y+16)
    y=top+5*step+10;s.text(xs[0],y,'Net payable',s.font,INK,weight=650);s.text(xs[3],y,money(sum(r['amount_cents'] for r in d['rows'])),s.font,INK,'end',650,'data-mark="total"')
    s.footer('Net payable: $4,215.75.','Synthetic. All due dates in November 2026. Exact lookup is the task; a chart is optional.')
    return s

CHARTS=[('01-revenue',revenue),('02-latency',latency),('03-paired',paired),('04-conversion',conversion),('05-sensor',sensor),('06-geography',geography),('07-uncertainty',uncertainty),('08-ledger',ledger)]

CSS='''
:root{--paper:#f2f2e9;--ink:#18312f;--muted:#576b68;--accent:#087f74;--line:#ced8cf}*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:24px}body{margin:0;background:var(--paper);color:var(--ink);font-family:"Segoe UI","Microsoft YaHei",Arial,sans-serif}a{color:inherit;text-underline-offset:4px}a:hover{color:var(--accent)}button,select{font:inherit;color:inherit}button,select{background:#fffdf8;border:1px solid #9bada3;padding:10px 14px;border-radius:3px}button{cursor:pointer}button:disabled{opacity:.5;cursor:default}:focus-visible{outline:3px solid #b34f2e;outline-offset:4px}.shell{max-width:1240px;margin:auto;padding:0 44px}header{border-bottom:1px solid var(--line);padding:26px 0}.brand{font-weight:700;letter-spacing:-.5px;font-size:21px}.topline{display:flex;justify-content:space-between;align-items:center;gap:20px}.topline a{font-size:14px}.hero{padding:70px 0 50px;display:grid;grid-template-columns:1fr 240px;align-items:end;gap:40px}h1{font-size:clamp(44px,6vw,76px);line-height:1.03;letter-spacing:-3px;font-weight:600;margin:0 0 25px}.hero p{font-size:17px;line-height:1.8;max-width:690px;margin:0;color:var(--muted)}.hero-side{border-top:2px solid var(--ink);padding-top:18px}.hero-side b{font-weight:400;font-size:76px;line-height:1}.hero-side p{font-size:14px;line-height:1.6}.layout{display:grid;grid-template-columns:155px minmax(0,1fr);gap:34px;align-items:start}nav{position:sticky;top:24px;padding:10px 0}nav a{display:block;text-decoration:none;font-size:14px;padding:9px 0;color:var(--muted)}nav a:hover{color:var(--accent)}.case{margin-bottom:70px;min-width:0}.case-head{padding:21px 0 18px;border-top:1px solid var(--line)}.eyebrow{font-size:12px;letter-spacing:1.4px;text-transform:uppercase;color:var(--accent);font-weight:650}h2{font-size:27px;font-weight:600;letter-spacing:-.6px;margin:9px 0}.case-head p{font-size:15px;line-height:1.7;color:var(--muted);margin:0}figure{margin:0;border:1px solid var(--line);background:#fffdf8}picture,img{display:block;width:100%;height:auto}figcaption{font-size:13px;line-height:1.6;padding:13px 22px;border-top:1px solid var(--line);color:var(--muted)}details{font-size:14px;line-height:1.8;margin-top:16px}summary{cursor:pointer;color:var(--muted)}details p{margin:10px 0}.interactive{background:#fffdf8;border:1px solid var(--line);padding:22px;margin-top:16px}.controls{display:flex;align-items:center;gap:12px;flex-wrap:wrap}.controls label{font-size:14px;font-weight:600}.interactive h3{font-size:18px;font-weight:600;margin:25px 0 10px}.interactive output{display:block;font-size:14px;line-height:1.7;color:var(--muted);margin:14px 0}.interactive svg{display:block;width:100%;height:auto}.counts{border-collapse:collapse;width:100%;font-size:14px}.counts caption{text-align:left;font-size:13px;color:var(--muted);margin:12px 0}.counts th,.counts td{text-align:left;border-bottom:1px solid var(--line);padding:10px 8px}.counts th:last-child,.counts td:last-child{text-align:right}.empty{padding:30px 0;color:var(--muted)}footer{border-top:1px solid var(--line);padding:32px 0 46px;font-size:14px;color:var(--muted);line-height:1.8}.sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0)}
@media(max-width:760px){.shell{padding:0 20px}.hero{padding:43px 0 32px;display:block}.hero-side{display:none}h1{letter-spacing:-1.8px}.hero p{font-size:15px}.layout{display:block}nav{position:static;display:flex;gap:18px;overflow-x:auto;margin:0 0 25px;padding:0 0 10px}nav a{white-space:nowrap}.case{margin-bottom:45px}.case-head p{font-size:14px}.interactive{padding:14px}.controls{gap:9px}button,select{padding:9px 10px;font-size:14px}.counts{font-size:13px}.counts th,.counts td{padding:9px 3px}figcaption{padding:12px 16px}.topline a{font-size:12px}.brand{font-size:18px}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}@media print{body{background:white}.hero,nav,header,.interactive,details{display:none}.layout{display:block}.shell{padding:0}.case{break-inside:avoid}figure{border:0}a{color:inherit}}
'''

JS='''
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
'''

def gallery():
    cases=json.loads((ROOT/'evals/cases.json').read_text(encoding='utf-8'))
    names=['Explain the change','Keep the tail','Preserve the pairs','Check the denominator','Show the gaps','Choose the right measure','Keep uncertainty visible','Let a table do the work']
    nav=['Revenue','Latency','Paired','Conversion','Coverage','Geography','Uncertainty','Exact lookup']
    reasons=[
      '选瀑布图保留起点、带符号变动与终点。堆叠构成不能直接解释负贡献。',
      '选 ECDF 保留分布交叉和尾部，补充分位数与阈值样本比例。没有把独立请求伪配对。',
      '连接相同参与者，保留唯一变慢者。观察到前后变化不等于识别培训因果效果。',
      '共同位置轴比较总体与各来源，保留分子分母。交互再验证筛选、空状态与复位。',
      '真实时间坐标，明确缺测和长间隙。只报告观测超阈样本，不编造持续超温时长。',
      '两个度量分开轴与单位，共同地区顺序便于对照。没有必要用地图引入面积干扰。',
      '点区间保留估计与区间宽度。使用输入给定的95%置信区间，不重新估计或暗示含零证明无效。',
      '主要任务是精确查值与对账，保留贷项和合计。表格本身就是完整答案。'
    ]
    sections=[]
    for i,(stem,_) in enumerate(CHARTS):
        c=cases[i]
        part=f'<section class="case" id="case-{i+1:02}" aria-labelledby="heading-{i+1}"><div class="case-head"><span class="eyebrow">{i+1:02} / {nav[i]}</span><h2 id="heading-{i+1}">{names[i]}</h2><p>{esc(reasons[i])}</p></div><figure><picture><source media="(max-width: 600px)" srcset="charts/{stem}-mobile.svg"><img src="charts/{stem}.svg" alt="{esc(names[i])}: {esc(c["title"])}" loading="lazy"></picture><figcaption>合成数据 · <a href="../{c["fixture"]}">原始数据</a> · <a href="charts/{stem}.svg" download>下载 SVG</a></figcaption></figure>'
        if i==3:
            part+='''<div class="interactive" hidden><div class="controls"><label for="segment">来源 / Segment</label><select id="segment"><option value="All">All sources</option><option value="Organic">Organic</option><option value="Paid">Paid</option><option value="Partner">Partner (no observations)</option></select><button type="button" id="reset-filter">Reset</button><button type="button" id="export-current">Download current SVG</button></div><h3 id="current-title">All sources / conversion rate</h3><svg id="rate-chart" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 240" role="img" aria-labelledby="live-title live-desc" font-family="Segoe UI, Arial, sans-serif"></svg><p class="empty" id="empty-state" hidden></p><output id="current-summary" aria-live="polite"></output><table class="counts"><caption>Current counts and denominators</caption><thead><tr><th scope="col">Version</th><th scope="col">Converted</th><th scope="col">Observed</th><th scope="col">Rate</th></tr></thead><tbody id="current-counts"></tbody></table></div><noscript><p>交互需要 JavaScript；上方静态图保留总体与来源的完整比较。</p></noscript>'''
        part+=f'<details><summary>用户请求与验收问题</summary><p>{esc(cases[i]["title"])}</p><p>{esc(json.loads((OUT/"plans.json").read_text(encoding="utf-8"))[i]["question"])}</p><p>{esc("；".join(c["reader_questions"]))}</p></details></section>'
        sections.append(part)
    navhtml=''.join(f'<a href="#case-{i+1:02}">{i+1:02} {label}</a>' for i,label in enumerate(nav))
    data=json.dumps(load('conversion'),ensure_ascii=False).replace('</','<\\/')
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="Eight synthetic worked examples for intent-driven data visualization."><title>Visual Storytelling by Graph — Worked Examples</title><link rel="stylesheet" href="style.css"></head><body><header><div class="shell topline"><span class="brand">Visual Storytelling / by Graph</span><a href="../README.md">Skill & installation ↗</a></div></header><main class="shell"><div class="hero"><div><h1>Make the point.<br>Keep the evidence.</h1><p>从用户要回答的问题出发，选择图表、叙事与必要交互。这里展示 8 个可复现示例，覆盖 12 个模拟用户请求。全部为合成数据；这些示例不构成真实读者效果验证。</p></div><div class="hero-side"><b>08</b><p>worked examples<br>One question at a time.</p></div></div><div class="layout"><nav aria-label="案例导航">{navhtml}</nav><div>{''.join(sections)}</div></div></main><footer><div class="shell">Skill, reference rules, source data and evaluation cases are included locally.<br><a href="../verification/REPORT.md">查看验证状态</a> · <a href="../references/sources.md">来源与规则边界</a><br>模拟案例用于展示与复查，不代表真实业务发现、真实用户实验或已验证的性能提升。</div></footer><script id="conversion-data" type="application/json">{data}</script><script src="app.js"></script></body></html>'''

def main():
    (OUT/'charts').mkdir(parents=True,exist_ok=True)
    for stem,builder in CHARTS:
        for mobile in [False,True]:(OUT/'charts'/(stem+('-mobile' if mobile else '')+'.svg')).write_text(builder(mobile).finish(),encoding='utf-8')
    (OUT/'style.css').write_text(CSS,encoding='utf-8');(OUT/'app.js').write_text(JS,encoding='utf-8');(OUT/'index.html').write_text(gallery(),encoding='utf-8')
    calc={'revenue':{'net':load('revenue')['closing']-load('revenue')['opening']},'latency':{key:{'n':len(load('latency')[key]),'p50':quantile(load('latency')[key],.5),'p95':quantile(load('latency')[key],.95),'over_500':sum(v>500 for v in load('latency')[key])/len(load('latency')[key])} for key in ['before','after']},'sensor':{'segments':len(sensor_segments(load('sensor')))},'ledger':{'total_cents':sum(r['amount_cents'] for r in load('ledger')['rows'])}}
    (OUT/'calculations.json').write_text(json.dumps(calc,indent=2)+'\n',encoding='utf-8')
    manifest={'hash_scheme':'SHA256 UTF-8 text, CRLF normalized to LF','sha256':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest() for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='manifest.json'}}
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print('Built 16 SVGs (8 desktop + 8 mobile), offline gallery, interactive filter and export.')

if __name__=='__main__':main()
