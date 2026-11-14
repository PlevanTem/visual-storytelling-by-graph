"""Independent forward test. Reads only named raw fixtures; no package implementation."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
from decimal import Decimal
from statistics import mean, median, stdev
from html import escape
import json, math, xml.etree.ElementTree as ET

HERE=Path(__file__).resolve().parent
PKG=HERE.parents[1]
def read(name): return json.loads((PKG/'evals'/'fixtures'/name).read_text(encoding='utf-8'))
def save(name,s): (HERE/name).write_text(s,encoding='utf-8')
def txt(x,y,s,**attrs):
    a=' '.join(f'{k.replace("_","-")}="{v}"' for k,v in attrs.items())
    return f'<text x="{x}" y="{y}" {a}>{escape(str(s))}</text>'
def line(x1,y1,x2,y2,**attrs):
    a=' '.join(f'{k.replace("_","-")}="{v}"' for k,v in attrs.items())
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" {a}/>'
def svg(title,body,w=1040,h=680):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}"><style>text{{font:14px Arial,sans-serif}} text:not([fill]){{fill:#1b2730}} .small{{font-size:12px}} .title{{font-size:22px;font-weight:bold}} line:not([stroke]){{stroke:#bdc7ce}} .axis{{stroke:#273c4b}}</style><rect width="{w}" height="{h}" fill="#fff"/>{txt(35,38,title,class_="title").replace("class-=", "class=")}{body}</svg>'
results={}
checks=[]
def check(name, condition):
    assert condition,name
    checks.append({'check':name,'status':'pass'})

# C15: exact product-limit computation, treating each event time as a risk-set query.
surv=read('survival.json'); groups=sorted({r['group'] for r in surv['rows']})
km={}
for group in groups:
    rows=[r for r in surv['rows'] if r['group']==group]
    s=Fraction(1); table=[]
    for t in sorted({r['time'] for r in rows}):
        n=sum(r['time']>=t for r in rows)
        d=sum(r['time']==t and r['event']==1 for r in rows)
        c=sum(r['time']==t and r['event']==0 for r in rows)
        s*=Fraction(n-d,n)
        table.append({'time':t,'risk':n,'events':d,'censored':c,'survival':float(s),'fraction':str(s)})
    med=next((r['time'] for r in table if r['survival']<=.5),None)
    km[group]={'n':len(rows),'events':sum(r['event'] for r in rows),'censored':sum(not r['event'] for r in rows),'last_observation':max(r['time'] for r in rows),'median_cycles':med,'steps':table}
results['C15']={'method':'Kaplan-Meier; time>=t risk set; events at ties processed before censor removal','groups':km,'assumptions':[surv['assumptions'],'No confidence interval or group significance test computed; observational group differences do not identify a causal environment effect.']}
body=txt(35,67,'Synthetic durability trial | unreadability is an event; + marks right censoring')
x=lambda v:100+8*v; y=lambda v:380-270*v
for v in [0,.25,.5,.75,1]:
    body+=line(100,y(v),900,y(v))+txt(75,y(v)+4,f'{v:.0%}',text_anchor='end')
for t in range(0,101,20): body+=line(x(t),110,x(t),380)+txt(x(t),407,t,text_anchor='middle')
body+=txt(500,432,'Accelerated aging cycles',text_anchor='middle')
for gi,group in enumerate(groups):
    color=['#156a9c','#c56822'][gi]; pts=[(x(0),y(1))]; prev=1
    for r in km[group]['steps']:
        pts.append((x(r['time']),y(prev)))
        if r['events']: pts.append((x(r['time']),y(r['survival'])))
        prev=r['survival']
        if r['censored']:
            body+=f'<g data-censor-group="{group}" data-time="{r["time"]}" data-count="{r["censored"]}">'
            body+=line(x(r['time'])-4,y(prev),x(r['time'])+4,y(prev),stroke=color,stroke_width=2)+line(x(r['time']),y(prev)-5,x(r['time']),y(prev)+5,stroke=color,stroke_width=2)
            if r['censored']>1: body+=txt(x(r['time']),y(prev)-11,f'x{r["censored"]}',text_anchor='middle')
            body+='</g>'
    body+=f'<polyline data-km="{group}" points="'+ ' '.join(f'{a},{b}' for a,b in pts)+f'" fill="none" stroke="{color}" stroke-width="3"/>'
    body+=txt(670,72+gi*22,f'{group}: n={km[group]["n"]}; {km[group]["events"]} events',fill=color)
    body+=txt(35,492+gi*28,group)
    for t in range(0,101,20):
        n=sum(r['group']==group and r['time']>=t for r in surv['rows'])
        body+=txt(x(t),492+gi*28,n,text_anchor='middle')
body+=txt(35,464,'At risk just before cycle (includes observations at that cycle)')
body+=txt(35,566,'Dry median: not reached within observed follow-up. Humid median: '+str(km['Humid']['median_cycles'])+' cycles.')
body+=txt(35,593,'Independent, non-informative censoring assumed. No confidence bands or causal claims.')
body+=txt(35,620,'Curves stop at each group\'s last observation; no extrapolation. All inputs are synthetic.')
save('C15-kaplan-meier.svg',svg('Readable survival with right censoring',body))

# C17: exact membership, with and without singleton patterns. Keep every observed pattern.
inter=read('intersections.json'); members=Counter(''.join('1' if b else '0' for b in r['membership']) for r in inter['rows'])
check('C17 unique raw object IDs',len({r['id'] for r in inter['rows']})==len(inter['rows']))
check('C17 declared universe has no 0000',members['0000']==0)
states=[]
for minimum in [1,2]:
    counts=sorted(((p,n) for p,n in members.items() if p.count('1')>=minimum),key=lambda kv:(-kv[1],kv[0]))
    total=sum(n for p,n in counts); states.append((minimum,total,len(counts)))
    body=txt(35,68,f'Synthetic archive | at least {minimum} tag(s) | {total} objects | {len(counts)} exact patterns')
    body+=txt(35,91,'Filled dots: included. Hollow dots: excluded. Each column is mutually exclusive.')
    bw=720/len(counts); base=345; unit=22
    for idx,(p,n) in enumerate(counts):
        cx=220+(idx+.5)*bw
        body+=f'<rect data-pattern="{p}" data-count="{n}" x="{cx-13}" y="{base-n*unit}" width="26" height="{n*unit}" fill="#156a9c"/>'
        body+=txt(cx,base-n*unit-9,n,text_anchor='middle')
        active=[i for i,b in enumerate(p) if b=='1']
        if len(active)>1: body+=line(cx,390+active[0]*37,cx,390+active[-1]*37,stroke='#273c4b',stroke_width=2)
        for k,b in enumerate(p): body+=f'<circle data-pattern="{p}" data-set="{k}" data-member="{b}" cx="{cx}" cy="{390+k*37}" r="5" stroke="#273c4b" fill="'+('#273c4b' if b=='1' else '#fff')+'"/>'
    for k,label in enumerate(inter['sets']): body+=txt(192,395+k*37,label,text_anchor='end')
    for v in range(0,10,3): body+=txt(205,base-v*unit+5,v,text_anchor='end')
    body+=line(220,base,940,base)+txt(35,565,'Counts refer to exact membership; an object with extra tags belongs to a different column.')
    body+=txt(35,595,'Universe excludes untagged objects. No observed intersection is omitted from the selected state.')
    save(f'C17-exact-{minimum}.svg',svg(f'Exact archive tag intersections: at least {minimum} tag(s)',body))
results['C17']={'method':'UpSet-style exact intersection bars and membership matrix; common 22 SVG units per object','patterns':dict(sorted(members.items())),'states':[{'minimum_tags':a,'objects':b,'patterns':c} for a,b,c in states]}

# C19: Decimal comparisons use the supplied decimal values exactly.
rec=read('recurrence.json'); values=[Decimal(str(v)) for v in rec['values']]; N=len(values)
rec_stats=[]
for eps in rec['epsilons']:
    E=Decimal(str(eps)); cells=[(i,j) for i in range(N) for j in range(N) if abs(values[i]-values[j])<=E]
    off=sum(i!=j for i,j in cells); denominator=N*(N-1)
    rec_stats.append({'epsilon':eps,'n':N,'off_diagonal_recurrent_cells':off,'denominator':denominator,'rate':off/denominator,'all_cells':len(cells)})
    body=txt(35,69,f'Synthetic scalar signal | epsilon={eps} amplitude units | n={N}')
    body+=txt(35,93,f'Off-diagonal recurrence: {off}/{denominator} = {100*off/denominator:.2f}%')
    for i,j in cells: body+=f'<rect data-i="{i}" data-j="{j}" x="{125+7*j}" y="{125+7*i}" width="7" height="7" fill="#156a9c"/>'
    for v in [0,16,32,48,63]:
        body+=txt(125+7*(v+.5),599,v,text_anchor='middle')+txt(112,125+7*(v+.5)+5,v,text_anchor='end')
    body+=txt(350,625,'Sample index j',text_anchor='middle')+txt(35,118,'Index i')
    body+=txt(620,165,'R(i,j) = 1 iff |x(i)-x(j)| <= epsilon')
    body+=txt(620,195,'Rate excludes the diagonal i=j.')
    body+=txt(620,225,'The diagonal is shown in the matrix.')
    body+=txt(620,270,'Fixed scale; no renormalization on toggle.')
    body+=txt(620,300,'Embedding dimension 1; scalar amplitude.')
    body+=txt(620,345,'Pattern depends on threshold and sampling.')
    body+=txt(620,375,'No claim about chaos or hidden mechanism.')
    save(f'C19-recurrence-{eps}.svg',svg(f'Recurrence at epsilon {eps}',body))
results['C19']={'method':'Scalar absolute distance; exact decimal comparisons; diagonal excluded only from rate','states':rec_stats,'sample_index_assumption':'Uniform sampling interval not supplied; axes show sample index, not physical time.'}

# C23: place exact x first, then resolve collisions vertically with deterministic candidates.
swarm=read('swarm.json'); swarm_stats=[]; body=txt(35,68,'Synthetic waiting times | each dot is one observation; horizontal position is exact')
for t in [0,15,30,45,60,75,90,100]:
    body+=line(140+8*t,110,140+8*t,565,stroke='#e3e7ea')+txt(140+8*t,590,t,text_anchor='middle')
for gi,row in enumerate(swarm['rows']):
    vals=row['values']; baseline=170+gi*160; placed=[]
    for idx,v in enumerate(vals):
        px=140+8*v
        for oy in [0]+[v for k in range(1,20) for v in (k*11,-k*11)]:
            py=baseline+oy
            if all(math.hypot(px-a,py-b)>=10.5 for a,b in placed): break
        else: raise AssertionError('unplaced swarm observation')
        placed.append((px,py))
        body+=f'<circle data-cohort="{row["cohort"]}" data-index="{idx}" data-value="{v}" cx="{px}" cy="{py}" r="4.5" fill="#156a9c"/>'
    summary={'cohort':row['cohort'],'n':len(vals),'mean':mean(vals),'median':median(vals),'min':min(vals),'max':max(vals),'sample_sd':stdev(vals),'frequencies':dict(sorted(Counter(vals).items()))}
    swarm_stats.append(summary)
    body+=txt(35,baseline-65,row['cohort'])+txt(140,baseline-65,f'n={len(vals)}; mean={mean(vals):g}; median={median(vals):g}; range={min(vals)}-{max(vals)} min')
body+=txt(535,620,'Wait time (minutes)',text_anchor='middle')+txt(35,655,'Vertical displacement only avoids overlap. These distributions do not identify the cause of complaints.')
save('C23-exact-x-swarm.svg',svg('Same mean, different observed waiting-time distributions',body,h=710))
results['C23']={'method':'Deterministic vertical-only collision avoidance; exact x; no jitter in wait values','groups':swarm_stats,'finding':'Compact values cluster around 15; Split has observations at 0 and 30; Tail has eleven 8-minute values and one 92-minute value. Complaint cause is not established.'}

# Parse the generated marks, then compare encodings against raw data or independently computed values.
ns={'s':'http://www.w3.org/2000/svg'}
for group in groups:
    root=ET.parse(HERE/'C15-kaplan-meier.svg').getroot(); mark=root.find(f'.//s:polyline[@data-km="{group}"]',ns)
    points=[tuple(map(float,p.split(','))) for p in mark.attrib['points'].split()]
    rows=[r for r in surv['rows'] if r['group']==group]
    check(f'C15 {group} curve ends at last observation',points[-1][0]==100+8*max(r['time'] for r in rows))
    observed_events=Counter(r['time'] for r in rows if r['event'])
    drops=[a[0] for a,b in zip(points,points[1:]) if b[1]>a[1]]
    check(f'C15 {group} SVG descends only at all event times',drops==[100+8*t for t in sorted(observed_events)])
    check(f'C15 {group} censor multiplicity retained',sum(int(e.attrib['data-count']) for e in root.findall(f'.//s:g[@data-censor-group="{group}"]',ns))==sum(not r['event'] for r in rows))
    for px,py in points:
        t=(px-100)/8
        factors=[1-count/sum(r['time']>=event_t for r in rows) for event_t,count in observed_events.items() if event_t<=t]
        post=math.prod(factors)
        # A horizontal segment arriving at an event may still show the pre-event value.
        pre=math.prod([1-count/sum(r['time']>=event_t for r in rows) for event_t,count in observed_events.items() if event_t<t])
        check(f'C15 {group} survival coordinate {px}:{py}',min(abs((380-py)/270-post),abs((380-py)/270-pre))<1e-12)
    # Independent life-table bookkeeping versus direct >= risk queries.
    at_risk=len(rows)
    for step in km[group]['steps']:
        check(f'C15 {group} time {step["time"]} life table risk',at_risk==step['risk'])
        at_risk-=step['events']+step['censored']
for minimum,total,_ in states:
    root=ET.parse(HERE/f'C17-exact-{minimum}.svg').getroot(); bars=root.findall('.//s:rect[@data-pattern]',ns)
    check(f'C17 state {minimum} conservation',sum(int(b.attrib['data-count']) for b in bars)==sum(sum(r['membership'])>=minimum for r in inter['rows']))
    for b in bars:
        p=b.attrib['data-pattern']; actual=sum(''.join(str(int(v)) for v in r['membership'])==p for r in inter['rows'])
        check(f'C17 {minimum} pattern {p} SVG height and baseline',float(b.attrib['height'])==22*actual and float(b.attrib['y'])+float(b.attrib['height'])==345)
    dots=root.findall('.//s:circle[@data-member]',ns)
    check(f'C17 state {minimum} exact membership encoding',all(d.attrib['data-member']==d.attrib['data-pattern'][int(d.attrib['data-set'])] and d.attrib['fill']==('#273c4b' if d.attrib['data-member']=='1' else '#fff') for d in dots))
previous=set()
for state in rec_stats:
    eps=state['epsilon']; root=ET.parse(HERE/f'C19-recurrence-{eps}.svg').getroot(); marks=root.findall('.//s:rect[@data-i]',ns)
    cells={(int(e.attrib['data-i']),int(e.attrib['data-j'])) for e in marks}
    check(f'C19 {eps} SVG cell coordinates',all(float(e.attrib['x'])==125+7*int(e.attrib['data-j']) and float(e.attrib['y'])==125+7*int(e.attrib['data-i']) for e in marks))
    check(f'C19 {eps} SVG full rule equivalence',all(((i,j) in cells)==(abs(values[i]-values[j])<=Decimal(str(eps))) for i in range(N) for j in range(N)))
    check(f'C19 {eps} symmetry and diagonal',all((j,i) in cells for i,j in cells) and all((i,i) in cells for i in range(N)))
    check(f'C19 {eps} threshold monotonicity',previous<=cells); previous=cells
    unordered=sum(abs(values[i]-values[j])<=Decimal(str(eps)) for i in range(N) for j in range(i+1,N))
    check(f'C19 {eps} rate from unordered-pair cross-check',unordered*2==state['off_diagonal_recurrent_cells'])
root=ET.parse(HERE/'C23-exact-x-swarm.svg').getroot()
for row in swarm['rows']:
    marks=root.findall(f'.//s:circle[@data-cohort="{row["cohort"]}"]',ns)
    check(f'C23 {row["cohort"]} every observation at exact x',len(marks)==len(row['values']) and all(float(e.attrib['cx'])==140+8*row['values'][int(e.attrib['data-index'])] for e in marks))
    check(f'C23 {row["cohort"]} no dot collisions',all(math.hypot(float(a.attrib['cx'])-float(b.attrib['cx']),float(a.attrib['cy'])-float(b.attrib['cy']))>=10.5 for i,a in enumerate(marks) for b in marks[i+1:]))

# No external scripts: all selectable states exist as inline SVG and remain readable without JS.
def panel(case,title,files,labels):
    buttons=''.join(f'<button type="button" data-select="{case}-{i}" aria-pressed="{str(i==0).lower()}">{escape(label)}</button>' for i,label in enumerate(labels))
    views=''.join(f'<div id="{case}-{i}" class="view"'+(' hidden' if i else '')+'>'+ (HERE/f).read_text(encoding='utf-8')+'</div>' for i,f in enumerate(files))
    return f'<section data-case="{case}"><h2>{title}</h2>{buttons}<button type="button" data-reset="{case}-0">Reset</button>{views}</section>'
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Independent specialist forward test</title><style>body{font:16px Arial;margin:24px auto;max-width:1080px;padding:0 12px;color:#1b2730;background:#f2f4f6}section{background:white;padding:16px;margin:20px 0}button{padding:10px;margin:4px;cursor:pointer}button[aria-pressed=true]{background:#156a9c;color:white}svg{width:100%;height:auto}h1{font-size:25px}h2{font-size:19px}.view[hidden]{display:none}</style><h1>Independent specialist forward test</h1><p>All four fixtures are synthetic. Each graphic retains its units, counts and limits. Controls use native keyboard-accessible buttons.</p>'''
html+=panel('C15','C15 - Censored durability',['C15-kaplan-meier.svg'],['Full observation'])
html+=panel('C17','C17 - Exact intersections',['C17-exact-1.svg','C17-exact-2.svg'],['All tagged objects','At least two tags'])
html+=panel('C19','C19 - Scalar recurrence',[f'C19-recurrence-{e}.svg' for e in rec['epsilons']],[f'Epsilon {e}' for e in rec['epsilons']])
html+=panel('C23','C23 - Exact waiting times',['C23-exact-x-swarm.svg'],['All samples'])
html+='''<noscript><style>.view[hidden]{display:block}</style>JavaScript is disabled; all parameter states are shown.</noscript><script>function select(id){const el=document.getElementById(id),s=el.closest('section');s.querySelectorAll('.view').forEach(v=>v.hidden=v.id!==id);s.querySelectorAll('[data-select]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.select===id));}document.addEventListener('click',e=>{const b=e.target.closest('button');if(b)select(b.dataset.select||b.dataset.reset);});</script></html>'''
save('index.html',html)
results['verification']={'checks':checks,'data_and_svg':'pass','render':'not_run','interaction':'not_run','reader_comprehension':'not_run','aesthetic_effectiveness':'not_tested'}
save('results.json',json.dumps(results,indent=2))
print(json.dumps({'outputs':sorted(p.name for p in HERE.iterdir()),'checks_passed':len(checks),'C15':{g:{k:v for k,v in d.items() if k!='steps'} for g,d in km.items()},'C17':results['C17']['states'],'C19':rec_stats,'C23':swarm_stats},indent=2))
