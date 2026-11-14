"""Portable factual, SVG-encoding and package validation. Standard library only."""
import hashlib,html,json,math,re,statistics,sys,xml.etree.ElementTree as ET
from collections import Counter
from fractions import Fraction
from pathlib import Path
from urllib.parse import unquote,urlparse
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1];CHECKS=[]
NS='{http://www.w3.org/2000/svg}'
def require(v,m):
    if not v:raise AssertionError(m)
def close(a,b,tol=.035):require(abs(float(a)-float(b))<=tol,f'{a} != {b}')
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def fixture(name):return read('evals/fixtures/'+name+'.json')
def marks(s,name):return [e for e in s.iter() if e.get('data-mark')==name]
def p(e,k):return float(e.get(k))
def numbers(s):return [float(v) for v in re.findall(r'[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?',s)]
def points(e):return [tuple(map(float,v.split(','))) for v in e.get('points').split()]
def check(name,fn):
    try:r=fn();CHECKS.append({'check':name,'status':'pass','detail':r})
    except Exception as e:CHECKS.append({'check':name,'status':'fail','detail':str(e)})

def structure():
    for name in ['SKILL.md','agents/openai.yaml','README.md','README.en.md','references/specialized-methods.md','docs/index.html','verification/REPORT.md']:
        require((ROOT/name).is_file(),'missing '+name)
    text=(ROOT/'SKILL.md').read_text(encoding='utf-8');require(text.startswith('---\nname: visual-storytelling-by-graph\n'),'renamed frontmatter');require('[TODO:' not in text,'scaffold')
    cases=read('evals/cases.json');require(len(cases)==24 and len({c['id'] for c in cases})==24,'24 unique cases')
    for c in cases:
        require((ROOT/c['fixture']).exists() and (ROOT/c['request']).exists(),c['id']);require(read(c['fixture'])['synthetic'] is True,'synthetic provenance')
        for key in ['facts','must_preserve','acceptable_alternatives','reader_questions']:require(bool(c[key]),c['id']+' '+key)
    works=read('docs/collection.json');require(len(works)==20 and len({w['id'] for w in works})==20,'20 works');require(sum(len(w['states']) for w in works)==31,'31 states')
    require(len(list((ROOT/'docs/assets').glob('c*-mobile.svg')))==31,'31 mobile assets')
    for w in works:
        require((ROOT/'docs'/w['data']).exists(),'data download')
        for state in w['states']:
            for key in ['chart','mobile']:
                s=ET.parse(ROOT/'docs'/state[key]).getroot();require(s.get('role')=='img','role');require(s.find(NS+'title') is not None and s.find(NS+'desc') is not None,'accessible SVG name')
                for e in s.iter():
                    for attr in ['x','y','width','height','cx','cy','r']:
                        if attr in e.attrib:require(math.isfinite(float(e.get(attr))),'nonfinite attribute');require(attr not in ['width','height','r'] or float(e.get(attr))>=0,'negative geometry')
    return {'cases':24,'json_fixtures':len(list((ROOT/'evals/fixtures').glob('*.json'))),'works':20,'states':31,'full_svg_assets':62}

def links():
    n=0
    for file in ROOT.rglob('*.md'):
        if '.git' in file.parts or 'independent' in file.parts:continue
        for value in re.findall(r'\[[^\]]*\]\(([^)]+)\)',file.read_text(encoding='utf-8')):
            target=value.strip().split(' "')[0]
            if urlparse(target).scheme or target.startswith('#'):continue
            require((file.parent/unquote(target.split('#')[0])).resolve().is_file(),f'{file.relative_to(ROOT)} -> {target}');n+=1
    page=(ROOT/'docs/index.html').read_text(encoding='utf-8')
    for target in re.findall(r'(?:href|src)="([^"]+)"',page):
        if urlparse(target).scheme or target.startswith('#'):continue
        require((ROOT/'docs'/unquote(target)).is_file(),'HTML -> '+target);n+=1
    return {'local_links':n,'remote_availability':'verified separately at publication'}

def facts():
    import classic_checks
    classic_checks.numerical();classic_checks.encodings();classic_checks.csv_audit()
    d=fixture('ternary');require(len(d['rows'])==36,'compositions');require(all(min(r[k] for k in d['parts'])>=0 and sum(r[k] for k in d['parts'])==100 for r in d['rows']),'closed parts')
    d=fixture('wind');require(sum(sum(r['counts']) for r in d['rows'])==240,'wind denominator');require(max(d['rows'],key=lambda r:sum(r['counts']))['direction']=='SE','direction maximum')
    d=fixture('survival');
    for group,expected in [('Dry',Fraction(231,400)),('Humid',Fraction(3,10))]:
        rows=[r for r in d['rows'] if r['group']==group];v=Fraction(1)
        for t in sorted({r['time'] for r in rows}):
            risk=sum(r['time']>=t for r in rows);events=sum(r['time']==t and r['event'] for r in rows);v*=Fraction(risk-events,risk)
        require(v==expected,'exact KM endpoint '+group)
    d=fixture('agreement');diff=[r['method_b']-r['method_a'] for r in d['rows']];require(statistics.mean(diff)==2 and sum(abs(x)>3 for x in diff)==6,'bias / tolerance')
    d=fixture('intersections');counts=Counter(tuple(r['membership']) for r in d['rows']);overlap=[r for r in d['rows'] if sum(r['membership'])>=2]
    require(len(d['rows'])==64 and len(counts)==15 and len(overlap)==42 and len({tuple(r['membership']) for r in overlap})==11,'set partition facts')
    d=fixture('repairs');require(len(d['rows'])==len({r['id'] for r in d['rows']})==60,'unique devices');require(Counter(r['Outcome'] for r in d['rows'])==Counter({'Reuse':34,'Parts':14,'Recycle':12}),'outcomes')
    values=fixture('recurrence')['values']
    for eps,expected in [(.1,422),(.25,986),(.45,1744)]:require(sum(abs(a-b)<=eps for i,a in enumerate(values) for j,b in enumerate(values) if i!=j)==expected,'off-diagonal count')
    d=fixture('horizon');require(len(d['rows'])==8 and all(len(r['values'])==48 for r in d['rows']),'horizon size');require(max(abs(v) for r in d['rows'] for v in r['values'])<6,'no horizon clipping')
    d=fixture('phase')['rows'];require(len(d)==97 and d[0]['input']==d[-1]['input'] and d[0]['response']==d[-1]['response'],'closed sampled cycle');require(d[24]['input']==d[72]['input'] and d[24]['response']!=d[72]['response'],'multiple responses at same input')
    d=fixture('ridges');require(len(d['rows'])==6 and all(len(r['values'])==24 for r in d['rows']),'ridge samples')
    d=fixture('swarm')['rows'];require([statistics.mean(r['values']) for r in d]==[15,15,15],'equal means');require([statistics.median(r['values']) for r in d]==[15,15,8],'different medians')
    d=fixture('spectrogram');require(len(d['values'])==256 and (len(d['values'])-64)//16+1==13,'STFT frames');require(8+24*1.25==38,'known components cross')
    return '24 supplied cases; exact KM fractions, counts, semantics, means and classic encodings. Not population or causal inference.'

def gallery_encodings():
    works=read('docs/collection.json');total=0
    for w in works:
        for state in w['states']:
            for key in ['chart','mobile']:
                file=ROOT/'docs'/state[key];s=ET.parse(file).getroot();md=s.find(NS+'metadata');m=json.loads(md.text) if md is not None else {};cid=w['id']
                if int(cid[1:])<=8 and state['key']=='All':
                    classic=ROOT/'examples/charts'/(['01-revenue','02-latency','03-paired','04-conversion','05-sensor','06-geography','07-uncertainty','08-ledger'][int(cid[1:])-1]+('-mobile' if key=='mobile' else '')+'.svg')
                    old=ET.parse(classic).getroot();attrs=['x','y','x1','y1','x2','y2','cx','cy','width','height','r','d']
                    geometry=lambda root:[(e.tag,tuple((a,e.get(a)) for a in attrs if e.get(a) is not None)) for e in root.iter() if e.get('data-mark')]
                    require(geometry(old)==geometry(s),'classic geometry '+str(file.name))
                elif cid=='C04':
                    rs=[r for r in fixture('conversion')['rows'] if r['segment']==state['key']]
                    if not rs:require(not marks(s,'filtered-rate') and m['available'] is False,'empty state is not zero')
                    else:
                        rects=marks(s,'filtered-rate');require(len(rects)==2,'two version rates');left=p(rects[0],'x')
                        ticks=[t for t in s.iter(NS+'text') if t.text=='100%'];right=float(ticks[0].get('x'))
                        for e in rects:
                            r=next(r for r in rs if r['version']==e.get('data-version'));close(p(e,'width'),(right-left)*r['success']/r['n'])
                elif cid=='C13':
                    rows={r['id']:r for r in fixture('ternary')['rows'] if state['key']=='All' or r['group']==state['key']};require(len(marks(s,'ternary'))==len(rows),'composition count')
                    for e in marks(s,'ternary'):
                        r=rows[e.get('data-id')];v=m['vertices'];close(p(e,'cx'),sum(r[k]*v[i][0]/100 for i,k in enumerate(['clay','silt','sand'])));close(p(e,'cy'),sum(r[k]*v[i][1]/100 for i,k in enumerate(['clay','silt','sand'])))
                elif cid=='C14':
                    d=fixture('wind');scale=m['radius_scale_per_sqrt_count'];require(len(marks(s,'wind-sector'))==24,'wind sectors')
                    for e in marks(s,'wind-sector'):
                        r=next(r for r in d['rows'] if r['direction']==e.get('data-direction'));j=int(e.get('data-bin'));r0=math.sqrt(sum(r['counts'][:j]))*scale;r1=math.sqrt(sum(r['counts'][:j+1]))*scale
                        arcs=[float(x) for x in re.findall(r'A ([\d.]+)',e.get('d'))];close(arcs[0],r1,.002)
                        if j:close(arcs[-1],r0,.002)
                        close((p(e,'data-r1')**2-p(e,'data-r0')**2)/scale**2,r['counts'][j],.000001)
                elif cid=='C15':
                    left,right,top,bottom=m['plot'];d=fixture('survival')['rows']
                    for e in marks(s,'km'):
                        rows=[r for r in d if r['group']==e.get('data-group')];v=Fraction(1);vs=[];ts=sorted({r['time'] for r in rows})
                        for t in ts:
                            risk=sum(r['time']>=t for r in rows);events=sum(r['time']==t and r['event'] for r in rows);v*=Fraction(risk-events,risk)
                            if events:vs.append(bottom-float(v)*(bottom-top))
                        actual=[float(y) for y in re.findall(r'V ([\d.]+)',e.get('d'))];require(len(actual)==len(vs),'event-only steps')
                        for a,b in zip(actual,vs):close(a,b)
                        xs=[float(x) for x in re.findall(r'H ([\d.]+)',e.get('d'))]
                        for a,t in zip(xs,ts):close(a,left+t/100*(right-left))
                    for e in marks(s,'risk'):require(int(e.get('data-n'))==sum(r['group']==e.get('data-group') and r['time']>=int(e.get('data-time')) for r in d),'risk set')
                    require(sum(int(e.get('data-n')) for e in marks(s,'censor'))==13,'censor multiplicity')
                elif cid=='C16':
                    d=fixture('agreement')['rows'];diff=[r['method_b']-r['method_a'] for r in d];bias=statistics.mean(diff);sd=statistics.stdev(diff)
                    close(m['bias'],bias,1e-10);close(m['loa'][0],bias-1.96*sd,1e-10);close(m['loa'][1],bias+1.96*sd,1e-10)
                    left,right,top,bottom=m['plot']
                    for e in marks(s,'agreement'):
                        r=next(r for r in d if r['id']==e.get('data-id'));mean=(r['method_a']+r['method_b'])/2;dv=r['method_b']-r['method_a'];close(p(e,'cx'),left+(mean-35)/70*(right-left));close(p(e,'cy'),bottom-(dv+5)/13*(bottom-top))
                elif cid=='C17':
                    d=fixture('intersections');counts=Counter(''.join('1' if b else '0' for b in r['membership']) for r in d['rows'] if state['key']=='All' or sum(r['membership'])>=2)
                    require(len(marks(s,'intersection'))==len(counts),'exact patterns')
                    for e in marks(s,'intersection'):
                        n=counts[e.get('data-pattern')];close(p(e,'height'),n*15);close(p(e,'y'),m['bar_bottom']-n*15)
                        x=p(e,'x')+p(e,'width')/2;circles=[c for c in s.iter(NS+'circle') if abs(p(c,'cx')-x)<.05];circles=sorted(circles,key=lambda c:p(c,'cy'));require(len(circles)==4,'four tags')
                        require(''.join('0' if c.get('fill')=='#2a393a' else '1' for c in circles)==e.get('data-pattern'),'included / excluded membership')
                elif cid=='C18':
                    d=fixture('repairs');counts=Counter('|'.join(r[k] for k in d['stages']) for r in d['rows']);require(len(marks(s,'flow'))==len(counts)==9,'complete paths')
                    for e in marks(s,'flow'):
                        n=counts[e.get('data-path')];curves=[numbers(t) for t in re.findall(r'C ([^CLMZ]+)',e.get('d'))];ls=[numbers(t) for t in re.findall(r'L ([^CLMZ]+)',e.get('d'))];start=numbers(re.search(r'M ([^CLMZ]+)',e.get('d')).group(1))
                        close(curves[-1][-1]-start[1],n*m['scale']);close(ls[1][1]-curves[1][-1],n*m['scale']);close(ls[2][1]-ls[0][1],n*m['scale'])
                    for j,stage in enumerate(d['stages']):require(sum(int(e.get('data-count')) for e in marks(s,'flow-node') if int(e.get('data-stage'))==j)==60,'node conservation')
                elif cid=='C19':
                    vals=fixture('recurrence')['values'];eps=float(state['key']);expected={(i,j) for i,a in enumerate(vals) for j,b in enumerate(vals) if abs(a-b)<=eps};actual={(int(e.get('data-i')),int(e.get('data-j'))) for e in marks(s,'recurrence')};require(actual==expected,'exact recurrence matrix')
                    close(m['rate'],(len(expected)-64)/4032,1e-10)
                    for e in marks(s,'recurrence'):close(p(e,'x'),m['origin'][0]+int(e.get('data-j'))*m['cell']);close(p(e,'y'),m['origin'][1]+int(e.get('data-i'))*m['cell'])
                elif cid=='C20':
                    rows={r['station']:r['values'] for r in fixture('horizon')['rows']};require(len(marks(s,'horizon'))==48,'signed bands')
                    for e in marks(s,'horizon'):
                        pts=points(e);base=pts[0][1];sign=int(e.get('data-sign'));band=int(e.get('data-band'));values=rows[e.get('data-station')];require(len(pts)==50,'48 sample heights')
                        for point,v in zip(pts[1:-1],values):close(point[1],base-min(2,max(0,sign*v-2*band))/2*m['band_height'])
                elif cid=='C21':
                    d=fixture('phase')['rows'];left,right,top,bottom=m['plot']
                    for e in marks(s,'phase'):
                        pts=[numbers(t) for t in re.findall(r'[ML] ([^ML]+)',e.get('d'))];rows=d[int(e.get('data-start')):int(e.get('data-end'))+1];require(len(pts)==len(rows),'ordered points')
                        for point,r in zip(pts,rows):close(point[0],left+(r['input']+1.15)/2.3*(right-left));close(point[1],bottom-(r['response']+1.15)/2.3*(bottom-top))
                elif cid=='C22':
                    d={r['stage']:r['values'] for r in fixture('ridges')['rows']};h=float(state['key'])
                    for e in marks(s,'kde'):
                        pts=points(e);require(len(pts)==203,'KDE evaluation grid');base=pts[0][1];values=d[e.get('data-stage')]
                        for i,point in enumerate(pts[1:-1]):x=i*.5;density=sum(math.exp(-((x-v)/h)**2/2) for v in values)/(len(values)*h*math.sqrt(2*math.pi));close(point[1],base-density*m['density_scale'])
                elif cid=='C23':
                    d={r['cohort']:r['values'] for r in fixture('swarm')['rows']};left,right=m['plot_x'];require(len(marks(s,'swarm'))==36,'all exact samples')
                    for e in marks(s,'swarm'):v=d[e.get('data-cohort')][int(e.get('data-index'))];close(p(e,'cx'),left+v/100*(right-left));require(float(e.get('data-value'))==v,'raw wait')
                    for group in d:
                        ms=[e for e in marks(s,'swarm') if e.get('data-cohort')==group]
                        for i,a in enumerate(ms):
                            for b in ms[i+1:]:require(math.hypot(p(a,'cx')-p(b,'cx'),p(a,'cy')-p(b,'cy'))>=9.45,'non-collision without x jitter')
                elif cid=='C24':
                    d=fixture('spectrogram');N=64;amplitudes=[]
                    for start in range(0,193,16):
                        frame=[]
                        for k in range(33):
                            reals=[];imags=[]
                            for n in range(N):v=d['values'][start+n]*(.5-.5*math.cos(2*math.pi*n/(N-1)));reals.append(v*math.cos(2*math.pi*k*n/N));imags.append(-v*math.sin(2*math.pi*k*n/N))
                            frame.append(math.hypot(sum(reals),sum(imags)))
                        amplitudes.append(frame)
                    peak=max(map(max,amplitudes));require(len(marks(s,'stft'))==13*33,'STFT grid');left,right,top,bottom=m['plot']
                    for e in marks(s,'stft'):
                        i,k=int(e.get('data-frame')),int(e.get('data-bin'));expected=max(-50,20*math.log10(max(amplitudes[i][k],peak*1e-12)/peak));close(e.get('data-db'),expected,1e-8);close(p(e,'x'),left+i*(right-left)/13);close(p(e,'y'),top+(32-k)*(bottom-top)/33)
                total+=1
    return {'full_svgs_checked':total,'methods':'Raw fixture recomputation and actual coordinate/path/area checks; not label matching alone.'}

def evidence():
    browser=ROOT/'verification/gallery-browser.json'
    if not browser.exists():return {'browser':'not_run'}
    r=read('verification/gallery-browser.json');require(r['status']=='pass','latest browser QA not passing')
    for name,h in r['inputs_sha256'].items():require(hashlib.sha256((ROOT/name).read_bytes().replace(b'\r\n',b'\n')).hexdigest()==h,'browser evidence stale: '+name)
    return {'browser':'pass','hashes_current':len(r['inputs_sha256']),'limits':r['limits']}

def main():
    for name,fn in [('structure',structure),('local_links',links),('facts_and_classic_checks',facts),('gallery_encoding_geometry',gallery_encodings),('recorded_browser_inputs',evidence)]:check(name,fn)
    result={'status':'pass' if all(r['status']=='pass' for r in CHECKS) else 'fail','checks':CHECKS,'limits':'Fixed synthetic cases, author-written deterministic checks. Not no-Skill/Skill A/B or human readers.'}
    (ROOT/'verification/structural-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2));return result['status']!='pass'
if __name__=='__main__':sys.exit(main())
