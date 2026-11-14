# 来源与规则索引

基础资料查阅：2026-11-14；专门方法扩展查阅：2026-11-15。链接原始资源，不分发全文或产品图片。

| ID | 来源与定位 | 采用的内容 | 不能推出 |
|---|---|---|---|
| S01 | [Origin 产品页](https://www.originlab.com/index.aspx?go=Products/Origin)，Graph Types / Data Exploration / Slicer | 图表与探索能力范围 | 本包已实现全部图表或某图最优 |
| S02 | [Tamara Munzner, Nested Model, 2009](https://www.cs.ubc.ca/labs/imager/tr/2009/NestedModel/)，摘要、模型、validity | 问题→抽象→编码与交互→算法；分层验证 | 文件或渲染通过就满足用户 |
| S03 | [Matthew Brehmer & Tamara Munzner, Multi-Level Typology, 2013](https://www.cs.ubc.ca/labs/imager/tr/2013/MultiLevelTaskTypology/)，摘要与框架 | 任务的 why / how / what；任务序列 | 本包意图字段是已校准问卷 |
| S04 | [Edward Segel & Jeffrey Heer, Narrative Visualization, 2010](https://vis.stanford.edu/files/2010-Narrative-InfoVis.pdf)，§4.4 | 作者引导与读者探索及混合结构 | 所有数据要同一个故事模板 |
| S05 | [Ji Soo Yi, Youn ah Kang, John T. Stasko & Julie A. Jacko, Role of Interaction, 2007](https://faculty.cc.gatech.edu/~john.stasko/papers/infovis07-interaction.pdf)，摘要与类别 | 围绕用户意图理解交互 | 七类必须全部实现 |
| S06 | [Jeffrey Heer & Michael Bostock, Crowdsourcing Graphical Perception, 2010](https://hci.stanford.edu/publications/2010/crowd-perception/heer-chi2010.pdf)，感知、实验与局限 | 编码、任务、尺寸和情境影响读取，需实证检查 | 万能图表排名或本项目已测读者 |

## 工程规则

### 扩展原始资料

| ID | 原始来源 | 采用内容与边界 |
|---|---|---|
| S07 | [Alexander Lex, Nils Gehlenborg, Hendrik Strobelt, Romain Vuillemot, Hanspeter Pfister, UpSet, 2014](https://vcg.seas.harvard.edu/publications/20140101-upset-visualization-of-intersecting-sets/paper) | 成员矩阵与交集量；本包实现是简化的精确模式展示，非完整 UpSet 软件 |
| S08 | [NIST, Kaplan–Meier approach](https://itl.nist.gov/div898/handbook/apr/section2/apr215.htm) | 风险集、删失与乘积极限估计；本例扩展为并列事件数 d，不包含区间与因果检验 |
| S09 | [GraphPad, Bland–Altman results](https://www.graphpad.com/guides/prism/latest/statistics/bland-altman_results.htm)、[NIST, Bland Altman Plot](https://www.itl.nist.gov/div898/software/dataplot/refman1/auxillar/blandalt.htm) | 配对差值与均值、偏差及一致性界限；本例选 1.96s，非 NIST 近似 2s，不将其当均值 CI |
| S10 | [Jeffrey Heer, Nicholas Kong, Maneesh Agrawala, Sizing the Horizon, 2009](https://idl.uw.edu/papers/horizon) | 分带与折叠思路及尺寸／层数的影响；不声称所有情境更优 |
| S11 | [Eckmann, Kamphorst & Ruelle, Recurrence Plots of Dynamical Systems, 1987](https://fiteoweb.unige.ch/~eckmannj/ps_files/recurrenceplots.pdf)、[作者团队维护的定义](https://www.recurrence-plot.tk/glance.php?show_intro=1) | 近邻状态矩阵；本例为固定阈值、标量维度，非隐藏动力系统重建 |
| S12 | [SciPy STFT documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.stft.html) | 窗口、步长、时频表示与幅度／功率含义；实际实现用标准库 DFT，未调用或复制 SciPy 源码 |

三元重心映射、风向扇区面积、转移守恒、KDE 和点避碰为本项目按定义实现的工程数学，不假借上述论文作为整套实现的效果背书。

下列为本项目综合设计，不是论文原文，也不是已验证的 Agent 工作流。

| ID | 规则 | 依据类型与边界 |
|---|---|---|
| R01 | 领域问题转成可检查任务 | S02、S03 启发；字段为工程选择，简单请求不完整建模 |
| R02 | 先确认粒度、分母、单位、聚合 | 数学与分析约束；CSV 不代替语义 |
| R03 | 依据解释／探索选择阅读控制 | S04 + 工程路由；具体场景需验证 |
| R04 | 先检查前提再比较候选 | S02、S03 + 工程综合；无唯一图表与万能分 |
| R05 | 精确比较通常优先位置与长度 | S06；受任务、密度和尺寸影响 |
| R06 | 对齐、层级、直接标签、语义色和实际尺寸 | 工程规范；未经本项目读者实验校准 |
| R07 | 交互有任务、状态、更新、复位与降级 | S05 启发；合同是工程设计 |
| R08 | 分开适合、支持、生成、渲染、操作与效果 | S02 启发 + 工程状态；绑定产物和环境 |
| R09 | 分层验证数据、渲染、操作和理解 | S02、S06 + 工程验收；通过仅覆盖所测范围 |
| R10 | 标题不超出数据证据 | 逻辑与统计约束；相关、前后、分组不自动识别因果 |

新增图表补前提、切换条件和失败案例；新增工具核实当前官方文档和版本。网页查阅日期不能替代论文出版年份。
