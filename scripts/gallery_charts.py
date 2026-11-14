"""SVG exhibit renderers. Theme changes do not change analytical transformations."""
import html,json,math,statistics
from collections import Counter,defaultdict
from pathlib import Path
import build_examples as legacy
from gallery_math import km,exact_intersections,recurrence,kde,stft,swarm

ROOT=Path(__file__).resolve().parents[1]
BG='#101719';INK='#e9e9df';MUTED='#98a8a5';GRID='#2a393a';ACCENT='#c3d8c7';AMBER='#dda96f';BLUE='#8fb8ce';RUST='#c77d63';FAINT='#476563'
COLORS=[ACCENT,AMBER,BLUE,RUST]
legacy.INK=INK;legacy.MUTED=MUTED;legacy.GRID=GRID;legacy.PAPER=BG;legacy.TEAL=ACCENT;legacy.ORANGE=AMBER;legacy.OLD=BLUE;legacy.FAINT=FAINT

def load(name):return json.loads((ROOT/'evals/fixtures'/f'{name}.json').read_text(encoding='utf-8'))
def esc(x):return html.escape(str(x),quote=True)
def fnum(x):return f'{x:g}'

class Canvas(legacy.SVG):
    def __init__(self,case,title,subtitle,mobile=False,height=None):
        super().__init__(case,title,subtitle,mobile,height or (790 if mobile else 730))
        self.case=case
    def polygon(self,points,fill,attrs=''):
        self.add(f'<polygon points="'+ ' '.join(f'{x:.3f},{y:.3f}' for x,y in points)+f'" fill="{fill}" {attrs}/>')
    def metadata(self,data):self.add('<metadata>'+esc(json.dumps(data,ensure_ascii=False))+'</metadata>')
    def footer(self,summary,note):
        super().footer(summary,note)
    def result(self):return self.finish()

def ternary(m=False,state='All'):
    d=load('ternary');rows=[r for r in d['rows'] if state=='All' or r['group']==state]
    s=Canvas('C13','Three parts. One closed whole.',f'Clay / silt / sand, mass % · {state} · n={len(rows)}',m,830 if m else 780)
    top=s.top+25;bottom=s.bottom-10;height=bottom-top;side=min(s.w-170,height*2/math.sqrt(3));height=side*math.sqrt(3)/2
    A=(s.w/2,bottom-height);B=(s.w/2-side/2,bottom);C=(s.w/2+side/2,bottom)
    pos=lambda a,b,c:(a*A[0]+b*B[0]+c*C[0],a*A[1]+b*B[1]+c*C[1])
    for t in [.2,.4,.6,.8]:
        for p,q in [(pos(t,1-t,0),pos(t,0,1-t)),(pos(1-t,t,0),pos(0,t,1-t)),(pos(1-t,0,t),pos(0,1-t,t))]:s.line(*p,*q,GRID)
        p=pos(t,1-t,0);s.text(p[0]-12,p[1]+5,str(round(t*100)),17 if m else 14,MUTED,'end')
        p=pos(0,t,1-t);s.text(p[0],p[1]+25,str(round(t*100)),17 if m else 14,MUTED,'middle')
        p=pos(1-t,0,t);s.text(p[0]+12,p[1]+5,str(round(t*100)),17 if m else 14,MUTED)
    s.polygon([A,B,C],'none',f'stroke="{MUTED}" stroke-width="1.2"')
    s.text(A[0],A[1]-19,'Clay 100%',s.font,INK,'middle');s.text(B[0]-8,B[1]+40,'Silt 100%',s.font,INK,'middle');s.text(C[0]+8,C[1]+40,'Sand 100%',s.font,INK,'middle')
    for r in rows:
        x,y=pos(r['clay']/100,r['silt']/100,r['sand']/100);color=COLORS[['Estuary','Dune','Loess'].index(r['group'])]
        s.circle(x,y,5.5 if m else 6,color,f'data-mark="ternary" data-id="{r["id"]}" data-clay="{r["clay"]}" data-silt="{r["silt"]}" data-sand="{r["sand"]}" fill-opacity=".8"')
    # Legend stays in the plot's unused top margin, outside the triangle.
    ly=s.top-4
    for i,g in enumerate(['Estuary','Dune','Loess']):
        x=s.pad+i*((s.w-2*s.pad)/3);s.circle(x+5,ly-5,4,COLORS[i]);s.text(x+18,ly,g,s.font-2,MUTED)
    s.footer('Composition closes to 100% for every sample.','Synthetic. Grid steps: 20 percentage points. No geological classification boundaries inferred.')
    s.metadata({'case':'C13','state':state,'n':len(rows),'vertices':[A,B,C]});return s

def arc_path(cx,cy,r0,r1,a0,a1):
    def p(r,a):return (cx+r*math.sin(a),cy-r*math.cos(a))
    a,b=p(r1,a0),p(r1,a1);c,e=p(r0,a1),p(r0,a0)
    if r0==0:return f'M {cx:.3f} {cy:.3f} L {a[0]:.3f} {a[1]:.3f} A {r1:.3f} {r1:.3f} 0 0 1 {b[0]:.3f} {b[1]:.3f} Z'
    return f'M {a[0]:.3f} {a[1]:.3f} A {r1:.3f} {r1:.3f} 0 0 1 {b[0]:.3f} {b[1]:.3f} L {c[0]:.3f} {c[1]:.3f} A {r0:.3f} {r0:.3f} 0 0 0 {e[0]:.3f} {e[1]:.3f} Z'

def wind(m=False,state='All'):
    d=load('wind');s=Canvas('C14','The wind has an address.','Direction FROM / area encodes observation frequency',m,840 if m else 790)
    cx=s.w/2;cy=(s.top+s.bottom)/2+22;rmax=min((s.w-190)/2,(s.bottom-s.top-45)/2)-10;scale=rmax/math.sqrt(60)
    for row in d['rows']:
        a=math.radians(row['bearing']);cum=0
        for j,n in enumerate(row['counts']):
            r0=math.sqrt(cum)*scale;cum+=n;r1=math.sqrt(cum)*scale
            s.add(f'<path d="{arc_path(cx,cy,r0,r1,a-math.radians(19),a+math.radians(19))}" fill="{["#36555d",BLUE,AMBER][j]}" stroke="{BG}" stroke-width="1" data-mark="wind-sector" data-direction="{row["direction"]}" data-bin="{j}" data-count="{n}" data-r0="{r0}" data-r1="{r1}"/>')
        lx=cx+(rmax+29)*math.sin(a);ly=cy-(rmax+29)*math.cos(a)
        s.text(lx,ly+6,row['direction'],s.font,MUTED,'middle')
    for n in [15,30,60]:
        r=math.sqrt(n)*scale;s.circle(cx,cy,r,'none',f'stroke="{MUTED}" stroke-opacity=".35" stroke-width="1"')
        s.text(cx+9,cy-r+18,f'{n/240:.2%}',s.font-3,INK,attrs=f'paint-order="stroke" stroke="{BG}" stroke-width="4"')
    for i,label in enumerate(['2–4 m/s','4–8 m/s','8+ m/s']):
        x=s.pad+i*(s.w-2*s.pad)/3;s.rect(x,s.top-15,13,13,['#36555d',BLUE,AMBER][i]);s.text(x+20,s.top-3,label,s.font-2,MUTED)
    s.footer('SE contributes 25% of all 240 observations.','Synthetic non-calm observations. Radius follows sqrt(count); clockwise from north. Ring labels are frequencies.')
    s.metadata({'case':'C14','n':240,'radius_scale_per_sqrt_count':scale});return s

def survival(m=False,state='All'):
    d=load('survival');s=Canvas('C15','Still readable. Not observed forever.','Readability / accelerated aging cycles',m,860 if m else 790)
    left=s.pad+48;right=s.w-s.pad-15;top=s.top+25;bottom=s.bottom-85;X=lambda t:left+t/100*(right-left);Y=lambda v:bottom-v*(bottom-top)
    for v in [0,.25,.5,.75,1]:s.line(left,Y(v),right,Y(v));s.text(left-12,Y(v)+6,f'{v:.0%}',s.font-2,MUTED,'end')
    for t in [0,20,40,60,80,100]:s.text(X(t),bottom+28,str(t),s.font-2,MUTED,'middle')
    risks={};endpoints={}
    for gi,g in enumerate(['Dry','Humid']):
        rows=[r for r in d['rows'] if r['group']==g];trace=km(rows);color=[ACCENT,AMBER][gi];path=f'M {X(0):.3f} {Y(1):.3f}'
        for r in trace:
            path+=f' H {X(r["time"]):.3f}'
            if r['events']:path+=f' V {Y(r["survival"]):.3f}'
            if r['censored']:
                x,y=X(r['time']),Y(r['survival']);s.line(x-4,y,x+4,y,color,2);s.line(x,y-6,x,y+6,color,2,f'data-mark="censor" data-group="{g}" data-time="{r["time"]}" data-n="{r["censored"]}"')
        s.path(path,color,3,f'data-mark="km" data-group="{g}"');last=trace[-1];endpoints[g]=last['survival']
        risks[g]=[sum(r['time']>=t for r in rows) for t in [0,20,40,60,80,100]]
        s.text(left-27,bottom+67+gi*27,g,s.font-2,color,'end')
        for t,n in zip([0,20,40,60,80,100],risks[g]):s.text(X(t),bottom+67+gi*27,n,s.font-2,color,'middle',attrs=f'data-mark="risk" data-group="{g}" data-time="{t}" data-n="{n}"')
        s.line(right-200+gi*105,top-14,right-177+gi*105,top-14,color,3);s.text(right-170+gi*105,top-8,g,s.font-2,color)
    s.footer('Risk counts below. Crosses mark censoring.','Synthetic, n=12/group. Curves stop at last observation. Non-informative censoring assumed; no confidence bands.')
    s.metadata({'case':'C15','risks':risks,'end_survival':endpoints,'plot':[left,right,top,bottom]});return s

def agreement(m=False,state='All'):
    d=load('agreement');diff=[r['method_b']-r['method_a'] for r in d['rows']];bias=statistics.mean(diff);sd=statistics.stdev(diff);lo,hi=bias-1.96*sd,bias+1.96*sd
    s=Canvas('C16','Correlation leaves agreement unanswered.','Bland–Altman / pair mean (x), B - A (y), dB',m,790 if m else 730)
    left=s.pad+55;right=s.w-s.pad-20;top=s.top+30;bottom=s.bottom;X=lambda v:left+(v-35)/70*(right-left);Y=lambda v:bottom-(v+5)/13*(bottom-top)
    s.rect(left,Y(3),right-left,Y(-3)-Y(3),'#1d2c2c')
    for v in [-4,-2,0,2,4,6,8]:s.line(left,Y(v),right,Y(v));s.text(left-12,Y(v)+6,str(v),s.font-2,MUTED,'end')
    for v in [40,60,80,100]:s.text(X(v),bottom+30,str(v),s.font-2,MUTED,'middle')
    for val,label,color in [(bias,'Bias',ACCENT),(lo,'Lower LoA',AMBER),(hi,'Upper LoA',AMBER)]:
        s.line(left,Y(val),right,Y(val),color,1.4,'stroke-dasharray="5 5"');s.text(left+8,Y(val)-8,f'{label} {val:+.2f}',s.font-3,color)
    for r in d['rows']:
        mean=(r['method_a']+r['method_b'])/2;v=r['method_b']-r['method_a'];s.circle(X(mean),Y(v),5,ACCENT if abs(v)<=3 else AMBER,f'data-mark="agreement" data-id="{r["id"]}" data-mean="{mean}" data-difference="{v}"')
    s.footer(f'Mean bias {bias:+.2f} dB. Tolerance band: ±3 dB.','Synthetic pairs. LoA = mean ±1.96 sample SD, not a mean CI. Distributional assumptions are not established.')
    s.metadata({'case':'C16','bias':bias,'sd':sd,'loa':[lo,hi],'domain_x':[35,105],'domain_y':[-5,8],'plot':[left,right,top,bottom]});return s

def upset(m=False,state='All'):
    d=load('intersections');min_degree=2 if state=='Overlaps' else 1;cols=exact_intersections(d['rows'],min_degree);n=sum(c['count'] for c in cols)
    s=Canvas('C17','Every overlap has a precise meaning.',f'Exact membership intersections / {state} / n={n} objects',m,840 if m else 770)
    left=118 if m else 165;right=s.w-s.pad-15;top=s.top+20;barbottom=top+155;matrix_top=barbottom+50;rowstep=38 if m else 35;step=(right-left)/len(cols)
    for value in [0,5,10]:y=barbottom-value/10*150;s.line(left,y,right,y);s.text(left-12,y+6,value,s.font-2,MUTED,'end')
    for j,c in enumerate(cols):
        x=left+step*(j+.5);h=c['count']/10*150;color=COLORS[min(c['degree']-1,3)]
        s.rect(x-step*.29,barbottom-h,step*.58,h,color,f'data-mark="intersection" data-pattern="'+''.join('1' if b else '0' for b in c['membership'])+f'" data-count="{c["count"]}"')
        s.text(x,barbottom-h-9,c['count'],17 if m else 15,color,'middle')
        active=[i for i,b in enumerate(c['membership']) if b]
        if len(active)>1:s.line(x,matrix_top+active[0]*rowstep,x,matrix_top+active[-1]*rowstep,color,2)
        for i,b in enumerate(c['membership']):s.circle(x,matrix_top+i*rowstep,4.5 if m else 5.5,color if b else GRID)
    for i,label in enumerate(d['sets']):s.text(left-18,matrix_top+i*rowstep+6,label,s.font-2,MUTED,'end')
    s.footer(f'{len(cols)} exclusive patterns. {n} unique objects.','Synthetic. Filled dots are included; unfilled tags are excluded. Universe: objects with at least one tag.')
    s.metadata({'case':'C17','state':state,'n':n,'patterns':len(cols),'left':left,'right':right,'bar_bottom':barbottom,'bar_scale':15});return s

def alluvial(m=False,state='All'):
    d=load('repairs');s=Canvas('C18','A second life has more than one route.','60 unique devices / observed three-stage paths',m,870 if m else 790)
    stages=d['stages'];orders=[['Audio','Optical','Mechanical'],['Repairable','Intermittent','Failed'],['Reuse','Parts','Recycle']]
    counts=Counter(tuple(r[k] for k in stages) for r in d['rows']);totals=[Counter(r[k] for r in d['rows']) for k in stages]
    left=s.pad+55;right=s.w-s.pad-55;xs=[left,(left+right)/2,right];top=s.top+48;gap=28;scale=(s.bottom-top-2*gap)/60;nw=12;nodes={};slots={}
    for j,order in enumerate(orders):
        y=top
        for label in order:nodes[j,label]=(y,totals[j][label]*scale);slots[j,label]=y;y+=totals[j][label]*scale+gap
    flows=[]
    for path,n in sorted(counts.items()):
        ys=[slots[j,label] for j,label in enumerate(path)];h=n*scale
        for j,label in enumerate(path):slots[j,label]+=h
        x0,x1,x2=xs;c0=(x0+x1)/2;c1=(x1+x2)/2;a,b,c=ys
        shape=f'M {x0+nw:.3f} {a:.3f} C {c0:.3f} {a:.3f} {c0:.3f} {b:.3f} {x1:.3f} {b:.3f} L {x1+nw:.3f} {b:.3f} C {c1:.3f} {b:.3f} {c1:.3f} {c:.3f} {x2:.3f} {c:.3f} L {x2:.3f} {c+h:.3f} C {c1:.3f} {c+h:.3f} {c1:.3f} {b+h:.3f} {x1+nw:.3f} {b+h:.3f} L {x1:.3f} {b+h:.3f} C {c0:.3f} {b+h:.3f} {c0:.3f} {a+h:.3f} {x0+nw:.3f} {a+h:.3f} Z'
        color=COLORS[orders[0].index(path[0])];s.add(f'<path d="{shape}" fill="{color}" fill-opacity=".43" data-mark="flow" data-path="{esc("|".join(path))}" data-count="{n}" data-width="{h}"/>');flows.append({'path':path,'count':n,'width':h})
    for j,order in enumerate(orders):
        s.text(xs[j]+nw/2,top-43,stages[j],s.font-1,MUTED,'middle')
        for label in order:
            y,h=nodes[j,label];s.rect(xs[j],y,nw,h,ACCENT,f'data-mark="flow-node" data-stage="{j}" data-label="{label}" data-count="{totals[j][label]}"')
            # Direct labels above each node avoid placing text across narrow ribbons.
            short={'Mechanical':'Mech.','Intermittent':'Intermit.','Repairable':'Repair'}.get(label,label) if m else label
            s.text(xs[j]+nw/2,y-8,f'{short} {totals[j][label]}',s.font-3,INK,'middle')
    s.footer('Reuse 34 / Parts 14 / Recycle 12.','Synthetic complete paths. Each device appears once; constant ribbon width follows its full path. Descriptive, not causal.')
    s.metadata({'case':'C18','n':60,'scale':scale,'flows':flows});return s

def recur(m=False,state='0.25'):
    d=load('recurrence');epsilon=float(state);matrix,rate=recurrence(d['values'],epsilon)
    s=Canvas('C19','A signal remembers its neighbours.',f'Scalar recurrence / epsilon {epsilon:g} amplitude units',m,840 if m else 810)
    size=min(s.w-175,s.bottom-s.top-25);left=(s.w-size)/2;top=s.top+8;cell=size/len(matrix)
    s.rect(left,top,size,size,'#182427')
    for i,row in enumerate(matrix):
        for j,v in enumerate(row):
            if v:s.rect(left+j*cell,top+i*cell,cell+.02,cell+.02,'#3c5854' if i==j else AMBER,f'data-mark="recurrence" data-i="{i}" data-j="{j}"')
    for value in [0,16,32,48,63]:
        x=left+(value+.5)*cell;y=top+(value+.5)*cell;s.text(x,top+size+27,value,s.font-2,MUTED,'middle');s.text(left-13,y+6,value,s.font-2,MUTED,'end')
    s.text(left,top-10,'Sample j →',s.font-2,MUTED)
    s.footer(f'Off-diagonal recurrence rate: {rate:.1%}.','Synthetic, 64 scalar states. Both axes are sample index. Main diagonal excluded from rate; no chaos inference.')
    s.metadata({'case':'C19','epsilon':epsilon,'rate':rate,'matrix_size':len(matrix),'origin':[left,top],'cell':cell});return s

def horizon(m=False,state='All'):
    d=load('horizon');s=Canvas('C20','Heat, folded into three bands.','8 stations × 48 days / temperature anomaly in °C',m,880 if m else 810)
    left=s.pad+55;right=s.w-s.pad-5;top=s.top+15;rowh=(s.bottom-top-20)/8;bandh=rowh*.73;X=lambda i:left+i/47*(right-left)
    palette={1:['#59462d','#9e7646',AMBER],-1:['#29475b','#507e99',BLUE]}
    for g,row in enumerate(d['rows']):
        base=top+(g+1)*rowh;s.line(left,base,right,base);s.text(left-12,base-8,row['station'],s.font-3,MUTED,'end')
        for sign in [-1,1]:
            for band in range(3):
                vals=[min(2,max(0,sign*v-band*2)) for v in row['values']]
                pts=[(left,base)]+[(X(i),base-v/2*bandh) for i,v in enumerate(vals)]+[(right,base)]
                s.polygon(pts,palette[sign][band],f'data-mark="horizon" data-station="{row["station"]}" data-sign="{sign}" data-band="{band}"')
    for day in [0,12,24,36,47]:s.text(X(day),s.bottom+25,day+1,s.font-2,MUTED,'middle')
    s.footer('2°C per band. Blue is negative; amber positive.','Synthetic. Negative values mirror upward; three common bands cover ±6°C. No sample exceeds the display range.')
    s.metadata({'case':'C20','band_width':2,'bands':3,'row_height':rowh,'band_height':bandh,'x_domain':[1,48]});return s

def phase(m=False,state='All'):
    d=load('phase');s=Canvas('C21','One input. Two histories.','Ordered input / response trajectory, normalized units',m,800 if m else 750)
    left=s.pad+55;right=s.w-s.pad-20;top=s.top+25;bottom=s.bottom;X=lambda v:left+(v+1.15)/2.3*(right-left);Y=lambda v:bottom-(v+1.15)/2.3*(bottom-top)
    for v in [-1,0,1]:s.line(left,Y(v),right,Y(v),GRID);s.text(left-10,Y(v)+6,str(v),s.font-2,MUTED,'end');s.line(X(v),top,X(v),bottom);s.text(X(v),bottom+29,str(v),s.font-2,MUTED,'middle')
    rows=d['rows'];mid=48
    for a,b,color in [(0,mid,ACCENT),(mid,96,AMBER)]:
        pts=[(X(r['input']),Y(r['response'])) for r in rows[a:b+1]];s.path(' '.join(('M' if i==0 else 'L')+f' {x:.3f} {y:.3f}' for i,(x,y) in enumerate(pts)),color,3,f'data-mark="phase" data-start="{a}" data-end="{b}"')
    for index in [16,64]:
        p,q=rows[index],rows[index+2];x,y=X(p['input']),Y(p['response']);dx,dy=X(q['input'])-x,Y(q['response'])-y;mag=math.hypot(dx,dy);ux,uy=dx/mag,dy/mag
        s.polygon([(x+ux*8,y+uy*8),(x-ux*5-uy*5,y-uy*5+ux*5),(x-ux*5+uy*5,y-uy*5-ux*5)],ACCENT if index<48 else AMBER)
    s.text(left+8,top+15,'Response ↑',s.font-2,MUTED);s.text(right,bottom+57,'Input →',s.font-2,MUTED,'end')
    s.footer('Direction is part of the data.','Synthetic lagged nonlinear response. Colours separate the two half-cycles; no physical mechanism is identified.')
    s.metadata({'case':'C21','rows':len(rows),'plot':[left,right,top,bottom],'domain':[-1.15,1.15]});return s

def ridges(m=False,state='5'):
    d=load('ridges');h=float(state);s=Canvas('C22','The tide changes shape, not just level.',f'Gaussian density / common scale / bandwidth {h:g} NTU',m,870 if m else 800)
    left=s.pad+88;right=s.w-s.pad-5;top=s.top+40;bottom=s.bottom;rowstep=(bottom-top-20)/6;X=lambda v:left+v/100*(right-left);grid=[i*.5 for i in range(201)]
    density_scale=650 if not m else 700
    for g,row in enumerate(d['rows']):
        base=top+(g+1)*rowstep;s.line(left,base,right,base);s.text(left-15,base-4,row['stage'],s.font-3,MUTED,'end')
        ys=[kde(row['values'],x,h) for x in grid];pts=[(left,base)]+[(X(x),base-y*density_scale) for x,y in zip(grid,ys)]+[(right,base)]
        s.polygon(pts,COLORS[g%4],f'fill-opacity=".5" stroke="{COLORS[g%4]}" stroke-width="1" data-mark="kde" data-stage="{row["stage"]}"')
    for value in [0,25,50,75,100]:s.text(X(value),bottom+31,value,s.font-2,MUTED,'middle')
    s.footer('24 observations per tide. Density units: 1/NTU.','Synthetic. All ridges share one absolute density scale; changing bandwidth changes the estimate, not the samples.')
    s.metadata({'case':'C22','bandwidth':h,'density_scale':density_scale,'row_step':rowstep,'plot':[left,right,top,bottom]});return s

def beeswarm(m=False,state='All'):
    d=load('swarm');s=Canvas('C23','The same mean can hide different waits.','Individual waiting times / minutes / n=12 per cohort',m,850 if m else 790)
    left=s.pad+97;right=s.w-s.pad-12;top=s.top+62;bottom=s.bottom-55;X=lambda v:left+v/100*(right-left);ys=[top,top+(bottom-top)/2,bottom]
    for tick in [0,15,30,60,90]:s.line(X(tick),top-55,X(tick),bottom+48,ACCENT if tick==15 else GRID,1,'stroke-dasharray="4 4"' if tick==15 else '');s.text(X(tick),bottom+78,tick,s.font-2,MUTED,'middle')
    placed_all=[]
    for g,(row,y) in enumerate(zip(d['rows'],ys)):
        s.text(left-15,y+6,row['cohort'],s.font-2,MUTED,'end')
        for p in swarm(row['values'],X,4.5,.5):
            s.circle(p['x'],y+p['offset'],4.5,COLORS[g],f'data-mark="swarm" data-cohort="{row["cohort"]}" data-index="{p["index"]}" data-value="{p["value"]}"');placed_all.append({**p,'cohort':row['cohort'],'y':y+p['offset']})
    s.footer('Every cohort averages 15 min. Tail reaches 92 min.','Synthetic. Exact values set x; vertical displacement only separates points. All 36 observations are retained.')
    s.metadata({'case':'C23','plot_x':[left,right],'domain_x':[0,100],'placed':placed_all});return s

def spectrogram(m=False,state='All'):
    d=load('spectrogram');z=stft(d['values'],d['sample_rate'],d['window'],d['hop']);s=Canvas('C24','A rising tone crosses a fixed one.','Windowed DFT magnitude / relative dB, not power density',m,800 if m else 750)
    left=s.pad+45;right=s.w-s.pad-65;top=s.top+15;bottom=s.bottom;frames=z['frames'];freq=z['frequencies'];cw=(right-left)/len(frames);ch=(bottom-top)/len(freq)
    def color(value):
        # Monotone luminance ramp: deep blue -> pale gold.
        t=(value+50)/50;a=(22,38,48);b=(226,192,138);return '#'+''.join(f'{round(x+(y-x)*t):02x}' for x,y in zip(a,b))
    for i,f in enumerate(frames):
        for k,db in enumerate(f['db']):s.rect(left+i*cw,top+(len(freq)-1-k)*ch,cw+.03,ch+.03,color(db),f'data-mark="stft" data-frame="{i}" data-bin="{k}" data-db="{db}"')
    for hz in [0,16,32,48,64]:
        y=bottom-(hz/2+.5)*ch;s.text(left-12,y+6,hz,s.font-2,MUTED,'end')
    for i in [0,4,8,12]:s.text(left+(i+.5)*cw,bottom+29,f'{frames[i]["center"]:.2f}s',s.font-2,MUTED,'middle')
    for j in range(50):s.rect(right+21,top+j*(bottom-top)/50,12,(bottom-top)/50+.1,color(-j))
    s.text(right+40,top+7,'0',s.font-3,MUTED);s.text(right+40,bottom,'-50',s.font-3,MUTED)
    s.text(left,top-13,'Hz',s.font-2,MUTED)
    s.footer('64-point Hann / hop 16 / sample rate 128 Hz.','Synthetic. 20 log10 magnitude relative to the global peak; floor -50 dB. Window centres shown; no source identification.')
    s.metadata({'case':'C24','frames':len(frames),'bins':len(freq),'reference_peak':z['reference_peak'],'plot':[left,right,top,bottom]});return s

BUILDERS={'C13':ternary,'C14':wind,'C15':survival,'C16':agreement,'C17':upset,'C18':alluvial,'C19':recur,'C20':horizon,'C21':phase,'C22':ridges,'C23':beeswarm,'C24':spectrogram}
OLD_BUILDERS={f'C{i+1:02}':builder for i,(_,builder) in enumerate(legacy.CHARTS)}

def filtered_conversion(m,state):
    d=load('conversion');rows=[r for r in d['rows'] if r['segment']==state]
    s=Canvas('C04',state+' / conversion rate','Same source, explicit counts and denominators',m,750 if m else 650)
    if not rows:
        s.text(s.w/2,(s.top+s.bottom)/2,'No observations',s.font+5,MUTED,'middle')
        s.footer('A conversion rate cannot be computed.','Synthetic. Missing observations are not a 0% rate. Return to All to restore the comparison.')
        s.metadata({'case':'C04','state':state,'available':False});return s
    left=s.pad+60;right=s.w-s.pad-10;top=s.top+55;bottom=s.bottom;X=lambda r:left+r*(right-left)
    for v in [0,.25,.5,.75,1]:s.line(X(v),top-25,X(v),bottom+8);s.text(X(v),bottom+35,f'{v:.0%}',s.font-2,MUTED,'middle')
    for i,version in enumerate(['Old','New']):
        r=next(r for r in rows if r['version']==version);rate=r['success']/r['n'];y=top+i*90;color=BLUE if i==0 else ACCENT
        s.text(left-12,y+28,version,s.font-2,color,'end');s.rect(left,y,(right-left)*rate,38,color,f'data-mark="filtered-rate" data-version="{version}" data-value="{rate}"')
        s.text(X(rate),y-12,f'{rate:.1%} ({r["success"]}/{r["n"]})',s.font,color,'end' if rate>.6 else 'start')
    s.footer('Rates use only the selected source.','Synthetic observational groups. All shows the pooled and stratified comparison; no causal attribution.')
    s.metadata({'case':'C04','state':state,'available':True,'rows':rows});return s

def render(case,mobile=False,state='All'):
    if case=='C04' and state!='All':s=filtered_conversion(mobile,state)
    elif case in BUILDERS:s=BUILDERS[case](mobile,state)
    else:s=OLD_BUILDERS[case](mobile)
    text=s.finish().replace('#faeee5','#302722').replace('#e9ece7','#1b292a')
    return s,text
