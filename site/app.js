'use strict';
const UI = {
  "en": {
    "scenarios": "Use cases",
    "collection": "Examples",
    "skill": "Get started",
    "edition": "VISUAL STORYTELLING / WITH YOUR AGENT",
    "heroAudience": "YOUR QUESTION · YOUR DATA · A CLEARER VIEW",
    "intro": "A visualization Skill for your Agent.",
    "shape": "See what",
    "evidence": "matters.",
    "heroDescription": "Give your Agent a question and your data.<br>Choose an appropriate chart, uncover the important patterns, and explain them clearly.",
    "enter": "See what the examples reveal",
    "startOwn": "Use it with your own data →",
    "heroNote": "Start with the question. Give the chart a purpose.",
    "scenarioLabel": "WHEN YOU HAVE DATA, AND A QUESTION",
    "scenarioTitle": "Does this sound familiar?",
    "scenarioIntro": "For reviews, product analysis, research and exploration.<br>You do not need to know the chart name.",
    "scenario1Title": "Explain a change",
    "scenario1Body": "Revenue moved. Which gains and losses explain it, and what belongs in the review?",
    "scenario2Title": "Look beyond the average",
    "scenario2Body": "The typical request is faster. Did the longest waits become worse?",
    "scenario3Title": "Compare with uncertainty",
    "scenario3Body": "Which differences are worth discussing, and how much do we actually know?",
    "scenario4Title": "Explore a complex structure",
    "scenario4Body": "Your data contains paths, memberships, compositions or signals. How should people read it?",
    "seeCase": "See a case ↗",
    "scenarioFit": "Bring a table, time series, paired records or specialist data your Agent can read. The Skill helps connect the question, data meaning and expression.",
    "selected": "QUESTIONS, EXPRESSED / 20 EXAMPLES",
    "collectionTitle": "What could your data reveal?",
    "synthetic": "Synthetic examples show what each expression can reveal.<br>Open a work for the data, reasoning and limits.",
    "all": "All examples",
    "change": "Changes",
    "compare": "Comparisons",
    "distribution": "Distributions",
    "structure": "Structure",
    "fitLabel": "FIT & EXPECTATIONS",
    "fitTitle": "Know what to bring.<br>Know what to expect.",
    "fit1Title": "Data with enough meaning",
    "fit1Body": "Tables and time series support everyday questions. Pairing, intervals, compositions and paths need their corresponding data. Units, denominators and sampling rules matter.",
    "fit2Title": "An output for the task",
    "fit2Body": "Expect a suitable chart or table, findings and important limits. Interactive, editable or exportable outputs depend on your Agent's available tools.",
    "fit3Title": "Claims the data can support",
    "fit3Body": "Missing evidence stays explicit. A before/after change is not proof of causality. When a key input is absent, the result should explain what is needed.",
    "startLabel": "START WITH YOUR OWN DATA",
    "skillTitle": "Your question.<br>Your next chart.",
    "skillDescription": "Add the Skill to your Agent, then share the question, data, reader and desired output. You can refine the result in the same conversation.",
    "readSkill": "Read the Skill ↗",
    "quickInstall": "1 / ADD TO YOUR AGENT",
    "copy": "Copy command",
    "download": "Download Skill ↓",
    "installNote": "Choose your Agent during installation, or give it the downloaded SKILL.md.",
    "installOptions": "Other ways to get started ↗",
    "requestLabel": "2 / SHARE YOUR QUESTION",
    "copyRequest": "Copy request",
    "requestTemplate": "Use $visual-storytelling-by-graph.\nQuestion: [what I need to understand]\nData: [attach a file or paste the table and field meanings]\nReader: [who will use this]\nOutput: [one chart / a report page / interactive exploration]\nChoose a suitable expression. Explain the findings and important limits.\nAsk if a critical definition is unclear.",
    "followup": "Then ask: “Compare the segments”, “Show the tail”, or “Make this readable in one slide.”",
    "step1": "Add the Skill",
    "step2": "Share a question + data",
    "step3": "Name the reader + output",
    "step4": "Inspect, ask, refine",
    "methodLabel": "THE DECISIONS BEHIND THE EXPRESSION",
    "methodTitle": "A method you can follow.",
    "methodIntro": "The intended advantage is a repeatable design process.<br>Each layer answers a different question.",
    "layer1Title": "Intent",
    "layer1Body": "Who needs to understand what, and for which decision?",
    "layer2Title": "Data meaning",
    "layer2Body": "Preserve units, denominators and pairing. A total and a rate answer different questions.",
    "layer3Title": "Expression",
    "layer3Body": "Keep distributions for tail questions; compare alternatives against the task.",
    "layer4Title": "Reading & interaction",
    "layer4Body": "Make the finding visible first. Add filters or detail only when they help the reader.",
    "layer5Title": "Checks & revision",
    "layer5Body": "Do the calculations, marks, display and operations agree?",
    "methodProof": "Inspectable examples and four independent specialist Agent runs support the implementation. Comparative gains, human comprehension and aesthetic preference have not been measured.",
    "footerNote": "Start with your question. Bring the result back to your context.",
    "userGuide": "User guide ↗",
    "maintenance": "Maintenance & reproduction ↗",
    "sources": "Research & sources ↗",
    "verification": "Evidence & limits ↗",
    "readWork": "Read the work",
    "question": "THE QUESTION",
    "why": "WHY THIS EXPRESSION",
    "boundary": "READ WITH CARE",
    "method": "Method & evidence ↗",
    "export": "Download current SVG ↓",
    "rawData": "Source data ↗"
  },
  "zh": {
    "scenarios": "使用场景",
    "collection": "案例效果",
    "skill": "快速上手",
    "edition": "图表叙事 / 与你的 Agent 一起",
    "heroAudience": "你的问题 · 你的数据 · 更清楚的表达",
    "intro": "让 Agent 围绕你的问题选择图表。",
    "shape": "看清",
    "evidence": "重点。",
    "heroDescription": "把问题和数据交给 Agent。<br>选择合适的图表，看清值得关注的变化、差异和关系，再把它讲清楚。",
    "enter": "看看案例能揭示什么",
    "startOwn": "用到你自己的数据 →",
    "heroNote": "从问题出发，让图表承担明确任务。",
    "scenarioLabel": "当你有一份数据，也有一个问题",
    "scenarioTitle": "你是否也在做这些事？",
    "scenarioIntro": "适合复盘、产品分析、研究和探索。<br>你不必先知道图表名称。",
    "scenario1Title": "解释一次变化",
    "scenario1Body": "收入变了，主要增减来自哪里？汇报时该突出什么？",
    "scenario2Title": "不只看平均值",
    "scenario2Body": "典型请求更快了，最慢的一批是否反而更差？",
    "scenario3Title": "带着不确定性比较",
    "scenario3Body": "哪些差异值得讨论？现有数据到底能说明多少？",
    "scenario4Title": "读懂复杂结构",
    "scenario4Body": "组成、路径、标签交集或信号，怎样表达才便于理解？",
    "seeCase": "看一个案例 ↗",
    "scenarioFit": "提供 Agent 能读取的表格、时序、配对记录或专门数据。Skill 会把问题、数据含义和表达方式连接起来。",
    "selected": "把问题表达出来 / 20 个案例",
    "collectionTitle": "你的数据，可能揭示什么？",
    "synthetic": "合成案例用于展示表达方式。<br>点开作品查看数据、选择理由和解释边界。",
    "all": "全部案例",
    "change": "变化与趋势",
    "compare": "比较与差异",
    "distribution": "分布与异常",
    "structure": "构成与关系",
    "fitLabel": "能力与适用边界",
    "fitTitle": "知道需要什么，<br>也知道能得到什么。",
    "fit1Title": "数据要有足够的含义",
    "fit1Body": "表格和时序支持常见问题；配对、区间、组成和路径需要对应结构。单位、分母和采样规则会影响表达。",
    "fit2Title": "交付适合当前任务的结果",
    "fit2Body": "通常得到图表或表格、主要发现和重要限制；交互、编辑和导出取决于当前 Agent 的可用工具。",
    "fit3Title": "结论跟随证据",
    "fit3Body": "缺少的证据要明确保留。前后变化不能直接证明因果；关键输入不足时，应说明需要补充什么。",
    "startLabel": "现在，用你自己的数据试试",
    "skillTitle": "你的问题，<br>下一张图。",
    "skillDescription": "把 Skill 加入你的 Agent，提供问题、数据、读者和交付方式。第一版之后，继续在同一对话里比较、追问和调整。",
    "readSkill": "阅读核心 Skill ↗",
    "quickInstall": "1 / 加入你的 Agent",
    "copy": "复制安装命令",
    "download": "下载 Skill ↓",
    "installNote": "安装时选择 Agent，或让它读取下载后的 SKILL.md。",
    "installOptions": "其他上手方式 ↗",
    "requestLabel": "2 / 提供你的问题",
    "copyRequest": "复制请求模板",
    "requestTemplate": "使用 $visual-storytelling-by-graph。\n我想回答：[你要弄清的问题]\n数据：[附文件，或粘贴数据及字段含义]\n读者：[谁看、了解多少背景]\n交付：[一张图／一页汇报／可交互探索]\n请选择合适的表达，指出主要发现和重要限制。\n关键口径不明确时请先问，不需要我指定图表类型。",
    "followup": "接着追问：“分组比较一下”“不要只看均值，看看尾部”“改成周会上能读懂的一张图”。",
    "step1": "加入 Skill",
    "step2": "给问题和数据",
    "step3": "说明读者与交付",
    "step4": "看结果、追问、调整",
    "methodLabel": "表达背后的判断环节",
    "methodTitle": "让选图有章可循。",
    "methodIntro": "目标是让设计判断更完整、更可重复。<br>每一层解决一个不同的问题。",
    "layer1Title": "用户意图",
    "layer1Body": "谁要理解什么，用于怎样的行动或决策？",
    "layer2Title": "数据语义",
    "layer2Body": "保留单位、分母和配对。总量与发生率，回答的是不同问题。",
    "layer3Title": "表达选择",
    "layer3Body": "问尾部，就保留分布；根据任务比较候选表达。",
    "layer4Title": "叙事与交互",
    "layer4Body": "让关键发现先被看见；筛选和细节查看都应服务读者的问题。",
    "layer5Title": "检查与修订",
    "layer5Body": "计算、图形编码、实际显示和操作是否一致？",
    "methodProof": "已有可复查案例，以及4个专门请求的独立 Agent 执行记录。相对基线的提升、真实读者理解和审美偏好尚未测量。",
    "footerNote": "从你的问题出发，把结果带回你的场景。",
    "userGuide": "使用指引 ↗",
    "maintenance": "维护与复现 ↗",
    "sources": "研究与方法来源 ↗",
    "verification": "效果证据与边界 ↗",
    "readWork": "作品解读",
    "question": "用户的问题",
    "why": "为什么这样表达",
    "boundary": "解释边界",
    "method": "方法与证据 ↗",
    "export": "下载当前 SVG ↓",
    "rawData": "原始数据 ↗"
  }
};
let lang='en',filter='all',current=null,stateIndex=0,returnFocus=null;
const gallery=document.getElementById('gallery'),dialog=document.getElementById('exhibit');
const image=document.getElementById('exhibit-image'),mobile=document.getElementById('exhibit-mobile'),info=document.getElementById('exhibit-info');
const visibleWorks=()=>WORKS.filter(w=>filter==='all'||w.tasks.includes(filter));
function setLanguage(value){lang=value;document.documentElement.lang=lang==='zh'?'zh-CN':'en';document.getElementById('language').textContent=lang==='en'?'中文':'EN';document.querySelectorAll('[data-i18n]').forEach(el=>{el.innerHTML=UI[lang][el.dataset.i18n]});document.querySelectorAll('[data-i18n-text]').forEach(el=>{el.textContent=UI[lang][el.dataset.i18nText]});document.querySelectorAll('.work').forEach(card=>{const w=WORKS.find(w=>w.id===card.dataset.id);card.querySelector('.work-title').textContent=w.title[lang];card.querySelector('.work-insight').textContent=w.insight[lang];card.querySelector('.work-open').setAttribute('aria-label',(lang==='en'?'Open ':'打开 ')+w.title[lang])});if(current)updateExhibit(false)}
function setFilter(value){filter=value;document.querySelectorAll('[data-filter]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.filter===filter)));document.querySelectorAll('.work').forEach(el=>{const w=WORKS.find(w=>w.id===el.dataset.id);el.hidden=filter!=='all'&&!w.tasks.includes(filter);el.classList.toggle('filtered',filter!=='all')});document.getElementById('work-count').textContent=visibleWorks().length+' / '+WORKS.length}
function updateExhibit(rebuildStates=true){
 const w=current,s=w.states[stateIndex];
 document.getElementById('exhibit-number').textContent=String(WORKS.indexOf(w)+1).padStart(2,'0')+' / '+WORKS.length;
 document.getElementById('exhibit-heading').textContent=w.type;
 mobile.srcset=s.mobile;image.src=s.chart;image.alt=w.title[lang]+' — '+s.summary[lang];
 document.getElementById('state-summary').textContent=s.summary[lang];
 document.getElementById('work-question').textContent=w.question[lang];document.getElementById('work-why').textContent=w.why[lang];document.getElementById('work-boundary').textContent=w.boundary[lang];
 document.getElementById('download-data').href=w.data;document.getElementById('method-link').href=w.method;
 const download=document.getElementById('download-svg');download.href=matchMedia('(max-width:600px)').matches?s.mobile:s.chart;download.download=w.id.toLowerCase()+'-'+s.key+'.svg';download.setAttribute('aria-disabled',String(s.available===false));download.tabIndex=s.available===false?-1:0;
 const controls=document.getElementById('state-controls');
 if(rebuildStates||controls.childElementCount!==w.states.length){controls.replaceChildren();if(w.states.length>1)w.states.forEach((state,index)=>{const b=document.createElement('button');b.type='button';b.textContent=state.label[lang];b.dataset.index=index;b.setAttribute('aria-pressed',String(index===stateIndex));b.addEventListener('click',()=>{stateIndex=index;updateExhibit(false)});controls.append(b)})}
 controls.querySelectorAll('button').forEach((b,i)=>{b.textContent=w.states[i].label[lang];b.setAttribute('aria-pressed',String(i===stateIndex))});
 dialog.dataset.case=w.id;dialog.dataset.state=s.key;
}
function syncWorkURL(){history.replaceState(null,'','#work-'+current.id)}
function openWork(id,trigger){current=WORKS.find(w=>w.id===id);if(!current)return;stateIndex=current.defaultState||0;returnFocus=trigger||document.activeElement;info.hidden=true;document.getElementById('toggle-info').setAttribute('aria-expanded','false');updateExhibit();document.body.classList.add('modal-open');if(!dialog.open)dialog.showModal();syncWorkURL();document.getElementById('close-exhibit').focus()}
function navigate(delta){const list=visibleWorks();let i=list.findIndex(w=>w.id===current.id);if(i<0)i=0;current=list[(i+delta+list.length)%list.length];stateIndex=current.defaultState||0;updateExhibit();syncWorkURL();document.querySelector('.exhibit-stage').scrollTop=0}
document.addEventListener('click',event=>{const opener=event.target.closest('[data-open]');if(opener){event.preventDefault();openWork(opener.dataset.open,opener)}});
document.querySelectorAll('[data-filter]').forEach(b=>b.addEventListener('click',()=>setFilter(b.dataset.filter)));
document.getElementById('language').addEventListener('click',()=>setLanguage(lang==='en'?'zh':'en'));
document.getElementById('close-exhibit').addEventListener('click',()=>dialog.close());
dialog.addEventListener('close',()=>{document.body.classList.remove('modal-open');current=null;if(location.hash.startsWith('#work-'))history.replaceState(null,'','#collection');if(returnFocus&&returnFocus.isConnected)returnFocus.focus()});
document.getElementById('previous').addEventListener('click',()=>navigate(-1));document.getElementById('next').addEventListener('click',()=>navigate(1));
document.getElementById('toggle-info').addEventListener('click',()=>{info.hidden=!info.hidden;document.getElementById('toggle-info').setAttribute('aria-expanded',String(!info.hidden))});
dialog.addEventListener('keydown',event=>{if(event.altKey||event.metaKey||event.ctrlKey)return;if(event.key==='ArrowRight'){event.preventDefault();navigate(1)}if(event.key==='ArrowLeft'){event.preventDefault();navigate(-1)}});
function wireCopy(buttonId,contentId,statusId){document.getElementById(buttonId).addEventListener('click',async()=>{const content=document.getElementById(contentId),status=document.getElementById(statusId);try{await navigator.clipboard.writeText(content.textContent);status.textContent=lang==='en'?'Copied.':'已复制。'}catch{const selection=window.getSelection(),range=document.createRange();range.selectNodeContents(content);selection.removeAllRanges();selection.addRange(range);status.textContent=lang==='en'?'Selected. Press Ctrl/Cmd+C to copy.':'已选中，请按 Ctrl/Cmd+C 复制。'}})}
wireCopy('copy-install','install-command','copy-status');wireCopy('copy-request','request-template','request-status');
window.addEventListener('resize',()=>{if(current)updateExhibit(false)});
function followWorkLink(){const match=location.hash.match(/^#work-(C\d{2})$/);if(!match||!WORKS.some(w=>w.id===match[1]))return;setFilter('all');openWork(match[1],document.querySelector('.work[data-id="'+match[1]+'"] .work-open'))}
window.addEventListener('hashchange',followWorkLink);
setLanguage('en');setFilter('all');followWorkLink();
