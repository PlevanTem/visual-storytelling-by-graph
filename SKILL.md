---
name: visual-storytelling-by-graph
description: "根据用户场景、数据语义和分析目的选择、设计、实现并验证可视化。Use for chart selection, narrative graphics, interactive analysis, or improving charts. Includes tables and no-chart outcomes; does not infer causal claims from descriptive data."
---

# Visual Storytelling by Graph

把用户的问题变成读者能够正确使用的表达。先确定读者任务，再决定数据变换、编码、阅读路径和交互。图表数量、复杂度和动画数量都不是质量指标。

## 按需入口

- 简单请求：确认指标与单位 → 选表达 → 实现 → 核对数据与实际尺寸。不要先提交长方案。
- 目标含糊：读 [意图与路由](references/intent-and-routing.md)。只问会改变设计的关键问题，其余明确假设并继续。
- 选图或修改图：读 [图表族与切换条件](references/chart-families.md)。用户指定图表时保留其要求，解释重要代价并建议替代，不擅自替换目标。
- 组成闭合、删失、交集、方向、轨迹或变换域等边缘任务：读 [专门方法](references/specialized-methods.md)，先核查数据前提、变换与解释边界。小众形式不自动优于简单表达。
- 汇报、信息图或交互分析：按需读 [叙事、交互与视觉设计](references/narrative-and-interaction.md)。探索任务不预设结论。
- 实现与验收：读 [实现与验证](references/implementation-and-validation.md)。只声明实际可用的能力。
- 评测：读 [评测方法](references/evaluation.md)。请求与数据在 `evals/requests/`、`evals/fixtures/`；评审答案在独立的 `evals/cases.json`。
- 核查依据：读 [来源与规则索引](references/sources.md)。不要默认加载全部参考资料。

## 核心流程

1. **理解问题。** 识别读者、具体问题、用途、阅读环境、行动和格式。区分探索、解释、监控、诊断与决策。分开用户希望证明的结论与数据支持的结论。
2. **核查语义。** 确定每行含义、单位、分母、时间窗口、聚合、独立或配对关系。列类型不能代替业务含义。合并比例重算分子与分母，不平均未加权比率；缺失不当零。
3. **抽象任务。** 比较什么、在哪个层级、与哪个基准比较？有多个任务时确定主要任务。决策还需选项、约束和权衡。
4. **选择表达。** 先排除缺少数据前提的方案，再比较任务适配、精度、信息保留、理解成本、空间、交互与实现成本。复杂任务比较少量候选，简单任务直接做。允许表格、直接数值、补数据或不制图。
5. **规划阅读。** 确定默认视图、焦点、尺度、顺序、注释和必要交互。有证据才用结论型标题；未知结果用问题型或描述型标题。故事不补造原因。
6. **实现。** 沿用已有工具与项目约束。静态报告保留完整意义；交互页面默认状态可读。不默认搭建 dashboard。
7. **验证并修正。** 核对计算、语义、实际渲染和关键操作。分开“检查通过”和“读者理解得到验证”。失败时回到对应环节，不能只换配色。

流程可以回退。发现粒度或问题理解有误时，重新规划，不强迫完成错误初案。

## 必须保留的判断

- 总量、比例、人均、增长率和百分点回答不同问题；切换后更新标题、单位与基准。
- 均值可能隐藏尾部和子群；是否补充分布由任务决定，不一律加图。
- 配对变化保留对象关系；独立样本不伪造连线。区间说明类型、水平与计算来源。
- 时序按真实时间定位；显式缺失和超出采样约定的间隙保留断点。平滑、分箱、抽样不静默改变主要发现。
- 精确比较优先考虑易比较的位置或长度；不存在跨任务通用的图表排名。
- 长度编码的柱形通常需要零基线；点图、线图尺度依任务选择并显式标示。双轴、对数、面积、三维需要说明收益与代价。
- 关联、前后变化、分组差异不自动构成因果证据。不按用户想要的故事改写事实。
- 流向图需要真实转移或边权；只有各阶段总量时不推断路径。地图要求空间关系有分析价值。
- 筛选后同步更新数据、分母、标题、样本量、摘要和注释。保留可见状态与复位方式。
- 关键结论不只放在 hover；交互支持目标设备。减少不承担任务的标签、色彩和控件。

## 可复查的记录

复杂任务内部保留简短设计记录，格式可调整、无关项可省略：

```json
{
  "question": "读者要回答什么",
  "audience": "谁使用",
  "purpose": "explain | explore | monitor | diagnose | decide",
  "grain_and_units": "对象、时间、度量口径",
  "evidence_status": "observed | inferred | unknown",
  "transformations": [],
  "selected_expression": "表达与理由",
  "alternatives": [],
  "interaction_contracts": [],
  "reader_questions": [],
  "assumptions": [],
  "verification": {"data": "not_run", "render": "not_run", "interaction": "not_run", "readers": "not_run"}
}
```

向普通用户优先交付产物、主要发现、必要口径和限制，不倾倒全部内部记录。

## 辅助脚本

核心 Skill 不绑定特定图表库、联网服务或示例生成器。

- `python scripts/audit_data.py input.csv --output audit.json`：标准库 CSV 审计；不理解单位、配对或因果，候选类型不等于业务类型。
- `python scripts/build_examples.py`：重建固定合成示例；不是任意数据的通用制图引擎。
- `python scripts/build_gallery.py`：重建 GitHub Pages 画廊和参数状态；主题只改变呈现，不改变数据。
- `python scripts/validate_bundle.py`：检查结构、链接、案例、统计和编码不变量；不能证明读者理解。

无数据时可提供方案或明确标注的模拟数据。不得将模拟案例、作者自检或未执行的 A/B 计划当成真实效果证据。
