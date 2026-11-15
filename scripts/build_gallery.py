"""Build the self-contained GitHub Pages collection from fixed synthetic fixtures."""
import hashlib,html,json,shutil,statistics,xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from gallery_charts import render,load,BG

ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs';ASSETS=DOCS/'assets'
REPO='https://github.com/PlevanTem/visual-storytelling-by-graph'
def bilingual(en,zh):return {'en':en,'zh':zh}
def slug(s):return s.lower().replace('.','-').replace(' ','-')
def dump(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Display metadata is kept with the build source; input data remains in evals/fixtures.
META=[
('C13','matter','Ternary composition','Three parts. One whole.','三部分，一个整体。','Compare closed sediment compositions across three environments.','Closed barycentric coordinates preserve all three parts and their 100% constraint.','三元坐标保留三部分的闭合关系；分组切换只过滤点，不改变尺度。','No geological classifications or independent causal interpretation.','未推断土壤分类；闭合组成不能当成三个独立原因。'),
('C14','matter','Area-scaled wind rose','The wind has an address.','风，有来处。','Where does wind arrive from, and where are the faster observations?','Equal-angle sectors encode count by area; nested rings separate speed bins.','等角扇区以面积表示次数，环带区分速度档，半径按次数平方根映射。','Only non-calm observations; direction is FROM, clockwise from north.','只含非静风观测；方向为来向，由北顺时针；分母为240。'),
('C19','time','Scalar recurrence','A signal remembers.','信号的回声。','Inspect recurring scalar states while changing a distance threshold.','Time-by-time proximity reveals repeated states; a fixed scale makes thresholds comparable.','时间×时间矩阵保留相近状态；阈值切换时数据尺度不变。','Embedding dimension 1. Threshold-dependent texture does not establish chaos.','嵌入维度为1；纹理依赖阈值，不证明混沌或真实机制。'),
('C18','relations','Object-level alluvial','Routes to a second life.','通往第二次生命。','Trace actual device paths through intake, diagnosis and outcome.','Each ribbon follows a complete observed path; constant width encodes unique devices.','完整记录汇总为路径，带宽按对象数保持一致，节点和阶段守恒。','Complete records only; observed pathways do not identify causes.','仅展示完整记录；路径描述转移，不解释原因。'),
('C17','relations','Exact-set intersections','Overlaps, accounted for.','交叠，自有边界。','Compare exact archive-tag intersections and isolate multi-tag objects.','Bars quantify exclusive membership patterns; the dot matrix shows included and excluded tags.','计数柱与成员矩阵配对，区分精确模式和包含式交集。','Universe contains at least one tag. Filtered object count changes explicitly.','总体仅含至少一个标签的对象；筛选后明确更新对象数。'),
('C15','time','Kaplan–Meier','Still readable.','仍然可读。','Compare time to unreadability while retaining right-censored specimens.','Event-only steps, censor marks and risk counts keep incomplete follow-up visible.','只在事件时刻下降，删失记号与风险集保留不完整观察。','Independent, non-informative censoring assumed; no causal or long-term extrapolation.','假设独立、非信息性删失；未估计置信带，不作因果或远期外推。'),
('C21','time','Ordered phase trajectory','One input. Two histories.','同一输入，两种历史。','Show why the same input has different responses during a cycle.','Ordered coordinates and directional arrows retain the trajectory rather than averaging it away.','按采样顺序连接，并显示方向；同一输入的多个响应不被平均掉。','Normalized illustration, not a fitted law or evidence of a physical mechanism.','归一化示意，不是拟合物理定律，也不识别真实机制。'),
('C20','time','Mirrored horizon','Heat, folded.','折叠的温度。','Compare signed temperature anomalies across many stations in a compact space.','Three common 2°C bands fold amplitude into height and colour while preserving sign.','以共同的2°C带宽折叠幅度，保留正负方向和变化时段。','Blue is negative, amber positive; use raw data for precise values.','蓝为负、琥珀为正；压缩增加读数成本，精确值需查数据。'),
('C24','time','STFT magnitude','A tone in motion.','移动的频率。','Separate a rising synthetic tone from a fixed-frequency component.','A windowed transform exposes when frequencies occur, using one global amplitude reference.','窗口化变换把频率放回时间，使用共同的全局幅度参考。','Relative magnitude dB, not PSD; resolution depends on window and hop.','相对幅度dB而非PSD；窗口与步长决定时频分辨率，不识别声源。'),
('C22','matter','Ridgeline KDE','The shape of the tide.','潮汐的形状。','Compare turbidity distributions and inspect sensitivity to smoothing bandwidth.','Shared horizontal and absolute-density scales support cross-group comparison.','共同横轴与绝对密度尺度支持比较；带宽参数显式可见。','Density is not point probability. Smoothing does not change the observations.','密度不是点概率；平滑不改变原始观测，也不能证明真实多峰。'),
('C16','evidence','Bland–Altman','Agreement, examined.','一致性，需要另看。','Can highly correlated acoustic methods be treated as interchangeable?','Paired differences against paired means expose bias and spread separately from correlation.','以配对均值对照差值，区分相关、偏差、容许误差与一致性界限。','Descriptive mean ±1.96 sample SD; assumptions not established; tolerance is separate.','mean±1.96样本SD为描述性界限，假设未建立；±3dB容许误差单独给定。'),
('C23','matter','Exact-value beeswarm','Averages miss the crowd.','均值之外的人群。','Compare cohorts with identical means but different individual waiting times.','Every exact x value and duplicate stays visible; y displacement only resolves collisions.','保留每个精确横坐标与重复值，只沿纵向避碰。','Synthetic n=12 per cohort; no population inference from these small samples.','各组n=12的合成小样本，不据此推断总体。'),
('C01','evidence','Revenue bridge','Explain the change.','把变化讲清。','Explain opening revenue, signed contributions and closing revenue.','A waterfall preserves additivity, negative losses and the endpoint.','瀑布表达保留起点、带符号贡献与终点，避免把变动误作构成。','Accounting contributions, not a causal model of the business.','会计贡献分解不是经营因果模型；数据为合成。'),
('C02','time','Empirical CDF','Keep the tail.','别丢掉尾部。','Did a release improve typical latency while making long waits worse?','An empirical step distribution preserves the crossing and tail; quantile labels support quick reading.','经验阶梯分布保留交叉与尾部，分位数摘要降低读数成本。','Independent n=20 samples per version; nearest-rank quantiles; not universal improvement.','每版本20个独立请求；nearest-rank分位数，不声称普遍改善。'),
('C03','evidence','Paired change','Preserve the pairs.','保留每一对。','Find which participants became faster or slower after training.','Individual matched lines preserve direction and the lone slower participant.','连接同一参与者的前后测，保留方向与唯一变慢者。','No control group; observed change is not proof of training causality.','无对照组；前后变化不证明培训因果效果。'),
('C04','relations','Stratified rates','Check the denominator.','先看分母。','Why did pooled conversion fall while both source-level rates rose?','Pooled and stratified rates share an axis; counts and denominators remain explicit.','共同尺度并列总体与分组率；来源切换同步分子、分母与标题。','Observational composition effects, not causal version effects. Missing source data is not zero.','观察性构成差异不是版本因果效果；无数据来源不显示为零。'),
('C05','time','Irregular time series','Show the gaps.','让缺测可见。','When did a sensor exceed its threshold, and where is sampling coverage absent?','Actual timestamps and broken segments preserve irregular intervals and missing coverage.','按真实时间定位，并在缺测和长间隙处断开。','Exceeding-sample share is not continuous exceedance duration.','超阈样本比例不等于持续超阈时长。'),
('C06','matter','Aligned measures','Volume or intensity?','总量，还是强度？','Allocate capacity while comparing demand per resident across regions.','Separate aligned axes retain two different measures without an unnecessary map.','分开单位和尺度，共同地区顺序支持对照；地图并非必需。','Per-capita intensity cannot replace total demand in capacity planning.','人均强度不能替代总量用于容量规划。'),
('C07','evidence','Point intervals','Keep uncertainty visible.','不确定性也要可见。','Compare experimental effect sizes with their supplied intervals.','Points and intervals preserve magnitude, width and the zero reference.','点和区间保留效应大小、宽度及零参考。','Supplied 95% CIs are not recomputed; containing zero does not prove no effect.','输入提供的95%CI未重新估计；含零不等于证明无效。'),
('C08','evidence','Exact-value table','Let a table do the work.','让表格完成任务。','Reconcile invoices, due dates, credits and the exact net payable.','A table prioritizes lookup precision and traceability rather than unnecessary charting.','精确查值与对账优先；保留金额精度、贷项和净合计。','Synthetic records, integer cents; no financial conclusion beyond the supplied ledger.','合成记录，以整数分存储金额，不外推到真实财务结论。')]

def summaries(cid,key,meta):
    if cid=='C13':return bilingual(f'{key}: {meta["n"]} closed compositions. All coordinates use the same triangle.',f'{key}：{meta["n"]}个闭合组成，坐标尺度不变。')
    if cid=='C17':return bilingual(f'{meta["n"]} unique objects / {meta["patterns"]} exact membership patterns.',f'{meta["n"]}个唯一对象 / {meta["patterns"]}个精确成员模式。')
    if cid=='C19':return bilingual(f'epsilon={key}; off-diagonal recurrence {meta["rate"]:.2%}; denominator 4032.',f'epsilon={key}；非对角递归率{meta["rate"]:.2%}；分母4032。')
    if cid=='C22':return bilingual(f'Bandwidth {key} NTU. Six groups, 24 samples each; fixed absolute density scale.',f'带宽{key} NTU；6组，每组24个观测；绝对密度缩放固定。')
    if cid=='C04' and key!='All':
        if not meta['available']:return bilingual('Partner has no observations. A conversion rate cannot be computed.','Partner无观测，不能计算转化率；不是0%。')
        rs={r['version']:r for r in meta['rows']};a,b=rs['Old'],rs['New'];return bilingual(f'{key}: Old {a["success"]}/{a["n"]}={a["success"]/a["n"]:.1%}; New {b["success"]}/{b["n"]}={b["success"]/b["n"]:.1%}.',f'{key}：Old {a["success"]}/{a["n"]}={a["success"]/a["n"]:.1%}；New {b["success"]}/{b["n"]}={b["success"]/b["n"]:.1%}。')
    if cid=='C15':return bilingual('At last follow-up: Dry 57.75% at 100 cycles; Humid 30.00% at 88 cycles.','末次观察处：Dry在100周期为57.75%；Humid在88周期为30.00%。')
    if cid=='C16':return bilingual(f'Descriptive bias {meta["bias"]:+.2f} dB; LoA [{meta["loa"][0]:+.2f}, {meta["loa"][1]:+.2f}].',f'描述性偏差{meta["bias"]:+.2f} dB；一致性界限[{meta["loa"][0]:+.2f}, {meta["loa"][1]:+.2f}]。')
    if cid=='C23':return bilingual('All three means are 15 minutes; medians 15 / 15 / 8; the longest wait is 92.','三组均值均15分钟；中位数15 / 15 / 8；最长等待92分钟。')
    return bilingual('Synthetic data. Read the work for the question, method and interpretation limits.','合成数据；打开作品解读查看问题、方法和解释边界。')

def main():
    ASSETS.mkdir(parents=True,exist_ok=True);(DOCS/'data').mkdir(exist_ok=True);(DOCS/'downloads').mkdir(exist_ok=True)
    cases={c['id']:c for c in json.loads((ROOT/'evals/cases.json').read_text(encoding='utf-8'))}
    works=[];audit=[];cards=[]
    everyday=['C01','C02','C04','C03','C06','C07','C05','C08']
    ordered=[next(item for item in META if item[0]==cid) for cid in everyday]+[item for item in META if item[0] not in everyday]
    tasks={
        'change':['C01','C03','C05','C15','C20','C21','C24'],
        'compare':['C03','C04','C06','C07','C13','C15','C16','C22','C23'],
        'distribution':['C02','C14','C22','C23'],
        'structure':['C13','C17','C18','C19','C21','C24']}
    insights={
        'C01':bilingual('Trace a $300k net change back to gains and losses.','把30万美元净变化追溯到各项增减。'),
        'C02':bilingual('p50 improves; p95 rises from 480 to 900 ms.','p50改善，p95却从480升至900ms。'),
        'C04':bilingual('Both sources improve while pooled conversion falls.','两个来源均提高，总体转化率却下降。'),
        'C03':bilingual('11 of 12 finish faster; one becomes slower.','12人中11人更快，1人变慢。'),
        'C06':bilingual('North leads in volume; South leads per resident.','North总量最高，South人均强度最高。'),
        'C07':bilingual("A's interval stays above zero; B remains imprecise.",'A的区间在零以上，B仍有较大不确定性。'),
        'C05':bilingual('High readings and missing coverage remain distinct.','超阈观测与缺测时段分别可见。'),
        'C08':bilingual('$4,215.75 net payable, with the credit retained.','净应付4,215.75美元，保留贷项。'),
        'C13':bilingual('Read mixtures across three parts that sum to 100%.','比较共同构成100%的三种组分。'),
        'C14':bilingual('SE accounts for 25% of the observed non-calm winds.','SE占非静风观测的25%。'),
        'C15':bilingual('Some specimens are still readable when follow-up ends.','保留观察结束时仍可读的样本。'),
        'C16':bilingual('Bias is +2 dB; agreement needs more than correlation.','偏差为+2dB；一致性需要超越相关来看。'),
        'C17':bilingual('The multi-tag filter reveals 42 of 64 objects.','筛出64个对象中的42个多标签对象。'),
        'C18':bilingual('Follow 60 recorded devices; 34 end in reuse.','追踪60台设备，34台最终再用。'),
        'C19':bilingual('Changing the threshold changes recurrence, not the signal.','阈值改变递归图，不改变原始信号。'),
        'C20':bilingual('Compare 48 days of signed anomalies across 8 stations.','比较8站点、48天的正负距平。'),
        'C21':bilingual('The same input has different responses across a cycle.','同一输入在循环中对应不同响应。'),
        'C22':bilingual('Change smoothing while preserving every observation.','改变平滑程度，保留原始观测。'),
        'C23':bilingual('Equal means of 15 minutes; the longest wait is 92.','均值同为15分钟，最长等待却达92分钟。'),
        'C24':bilingual('Separate a rising tone from a fixed 38 Hz component.','区分扫频和固定38Hz分量。')}
    for number,item in enumerate(ordered,1):
        cid,category,typ,title_en,title_zh,question_en,why_en,why_zh,boundary_en,boundary_zh=item
        case=cases[cid];keys={'C13':['All','Estuary','Dune','Loess'],'C17':['All','Overlaps'],'C19':['0.1','0.25','0.45'],'C22':['2','5','10'],'C04':['All','Organic','Paid','Partner']}.get(cid,['All'])
        default=1 if cid in ['C19','C22'] else 0
        states=[]
        for key in keys:
            rendered=[];meta={}
            for mobile in [False,True]:
                canvas,text=render(cid,mobile,key);stem=cid.lower()+'-'+slug(key)+('-mobile' if mobile else '')
                path=ASSETS/(stem+'.svg');path.write_text(text,encoding='utf-8');rendered.append('assets/'+path.name)
                root=ET.fromstring(text);md=root.find('{http://www.w3.org/2000/svg}metadata')
                if md is not None:meta=json.loads(md.text)
                audit.append({'case':cid,'state':key,'mobile':mobile,'file':path.relative_to(ROOT).as_posix(),'meta':meta})
            label=bilingual(key,key)
            if cid=='C17':label=bilingual('All exact patterns' if key=='All' else 'At least 2 tags','全部精确模式' if key=='All' else '至少2个标签')
            if cid=='C19':label=bilingual('epsilon '+key,'epsilon '+key)
            if cid=='C22':label=bilingual('h = '+key+' NTU','h = '+key+' NTU')
            if cid=='C04' and key=='All':label=bilingual('Overview / Reset','概览 / 复位')
            states.append({'key':key,'label':label,'chart':rendered[0],'mobile':rendered[1],'summary':summaries(cid,key,meta),'available':meta.get('available',True)})
        selected=states[default];full=(DOCS/selected['chart']).read_text(encoding='utf-8');canvas,_=render(cid,False,keys[default]);root=ET.fromstring(full)
        # Crop only preview framing. Full downloads retain titles, scales and notes.
        top=max(0,canvas.top-32);height=canvas.bottom-canvas.top+98
        root.set('viewBox',f'0 {top:.2f} {canvas.w} {height:.2f}');root.set('width','1000');root.set('height',str(round(height)))
        preview=ASSETS/(cid.lower()+'-preview.svg');ET.register_namespace('','http://www.w3.org/2000/svg');ET.ElementTree(root).write(preview,encoding='unicode')
        fixture=ROOT/case['fixture'];shutil.copy2(fixture,DOCS/'data'/fixture.name)
        question=(ROOT/case['request']).read_text(encoding='utf-8').split('\n\n')[1]
        method='references/specialized-methods.md' if int(cid[1:])>=13 else 'references/chart-families.md'
        work={'id':cid,'category':category,'tasks':[name for name,ids in tasks.items() if cid in ids],'type':typ,'title':bilingual(title_en,title_zh),'insight':insights[cid],'question':bilingual(question_en,question),'why':bilingual(why_en,why_zh),'boundary':bilingual(boundary_en,boundary_zh),'states':states,'defaultState':default,'data':'data/'+fixture.name,'method':REPO+'/blob/main/'+method,'preview':'assets/'+preview.name}
        works.append(work)
        cards.append(f'<article class="work" id="work-{cid}" data-id="{cid}"><a class="work-open" href="{selected["chart"]}" data-open="{cid}" aria-label="Open {html.escape(title_en,quote=True)}"><div class="work-art"><img src="assets/{preview.name}" alt="{html.escape(typ,quote=True)}" loading="lazy" width="1000" height="500"></div><div class="work-meta"><span class="work-number">{number:02}</span><h3 class="work-title">{html.escape(title_en)}</h3><span class="work-type">{html.escape(typ)}</span></div><p class="work-insight">{html.escape(insights[cid]["en"])}</p></a></article>')
    # Hero keeps real composition coordinates but removes the opaque page rectangle.
    hero=ET.parse(ASSETS/'c13-all.svg').getroot();hero.set('viewBox','125 120 750 525');hero.set('width','1200');hero.set('height','840')
    first=hero.find('{http://www.w3.org/2000/svg}rect')
    if first is not None:hero.remove(first)
    for element in list(hero):
        tag=element.tag.split('}')[-1]
        if tag=='circle' and element.get('data-mark')!='ternary':hero.remove(element)
        elif tag=='text' and (float(element.get('y','0'))<170 or element.text in ['Estuary','Dune','Loess']):hero.remove(element)
        elif tag=='line' and float(element.get('y1','0'))<170 and float(element.get('y2','0'))<170:hero.remove(element)
    ET.ElementTree(hero).write(ASSETS/'hero.svg',encoding='unicode')
    (ASSETS/'mark.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 36 36"><rect width="36" height="36" fill="#0c1112"/><path d="M3 29L12 18L22 23L33 5M3 18L12 26L22 9L33 15" fill="none" stroke="#c3d8c7" stroke-width="1.6"/></svg>',encoding='utf-8')
    template=(ROOT/'site/index.template.html').read_text(encoding='utf-8')
    (DOCS/'index.html').write_text(template.replace('__GALLERY__','\n'.join(cards)),encoding='utf-8')
    for src,dest in [('style.css','style.css'),('app.js','app.js')]:shutil.copy2(ROOT/'site'/src,DOCS/dest)
    (DOCS/'collection.js').write_text('const WORKS = '+json.dumps(works,ensure_ascii=False,indent=2)+';\n',encoding='utf-8')
    (DOCS/'.nojekyll').write_text('',encoding='utf-8');dump(DOCS/'collection.json',works)
    dump(ROOT/'verification/gallery-build.json',{'works':len(works),'states':sum(len(w['states']) for w in works),'assets':audit,'limits':'Author renderers; synthetic data; no human-reader measurement.'})
    print(f'Built {len(works)} works, {sum(len(w["states"]) for w in works)} states, {len(audit)} full SVG assets, bilingual static gallery.')

if __name__=='__main__':main()
