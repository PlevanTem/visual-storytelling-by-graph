"""Small, explicit calculations for fixed synthetic exhibits; standard library only."""
import cmath
import math
from collections import Counter

def km(rows):
    survival=1.0;out=[]
    for t in sorted({r['time'] for r in rows}):
        risk=sum(r['time']>=t for r in rows)
        events=sum(r['time']==t and r['event']==1 for r in rows)
        censored=sum(r['time']==t and r['event']==0 for r in rows)
        survival*=1-events/risk
        out.append({'time':t,'risk':risk,'events':events,'censored':censored,'survival':survival})
    return out

def exact_intersections(rows,min_degree=1):
    counts=Counter(tuple(r['membership']) for r in rows if sum(r['membership'])>=min_degree)
    return [{'membership':list(pattern),'count':n,'degree':sum(pattern)} for pattern,n in sorted(counts.items(),key=lambda p:(-p[1],p[0]))]

def recurrence(values,epsilon):
    matrix=[[int(abs(a-b)<=epsilon) for b in values] for a in values]
    n=len(values);rate=(sum(map(sum,matrix))-n)/(n*(n-1))
    return matrix,rate

def kde(values,x,bandwidth):
    return sum(math.exp(-.5*((x-v)/bandwidth)**2) for v in values)/(len(values)*bandwidth*math.sqrt(2*math.pi))

def stft(values,sample_rate,window,hop):
    weights=[.5-.5*math.cos(2*math.pi*i/(window-1)) for i in range(window)]
    frames=[]
    for start in range(0,len(values)-window+1,hop):
        amplitudes=[abs(sum(values[start+n]*weights[n]*cmath.exp(-2j*math.pi*k*n/window) for n in range(window))) for k in range(window//2+1)]
        frames.append({'center':(start+(window-1)/2)/sample_rate,'amplitudes':amplitudes})
    peak=max(max(f['amplitudes']) for f in frames)
    for f in frames:f['db']=[max(-50,20*math.log10(max(a,peak*1e-12)/peak)) for a in f['amplitudes']]
    return {'frames':frames,'frequencies':[k*sample_rate/window for k in range(window//2+1)],'reference_peak':peak}

def swarm(values,map_x,radius=5,padding=1):
    placed=[];step=radius*2+padding
    for index,value in sorted(enumerate(values),key=lambda a:(a[1],a[0])):
        x=map_x(value)
        for j in range(1000):
            offset=0 if j==0 else ((j+1)//2)*step*(1 if j%2 else -1)
            if all((x-p['x'])**2+(offset-p['offset'])**2>=step**2-.00001 for p in placed):break
        else:raise ValueError('Could not place point without changing exact x.')
        placed.append({'index':index,'value':value,'x':x,'offset':offset})
    return placed
