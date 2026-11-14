# 实现与验证

## 能力状态 [R08]

| 状态 | 能说什么 |
|---|---|
| 设计上适合 | 表达支持任务的理由；无运行保证 |
| 工具支持 | 已检查当前 API 或组件；未证明运行 |
| 已生成 | 文件存在；未证明正常显示 |
| 已渲染 | 在记录环境、尺寸与状态下实际显示 |
| 已操作 | 关键路径实际执行并核对结果 |
| 已测读者 | 有读者、任务、方法和观察结果 |

示例渲染器只覆盖固定合成案例，不是通用编译器。Skill 可使用其他工具；不能把示例能力当作设计边界。

## 可重复实现

保留输入、变换、设计记录、源文件和必要依赖；固定随机种子或直接保存生成数据。外部 API 按当前官方文档核实。CSV 审计命令：

```sh
python scripts/audit_data.py my-data.csv --output audit.json
```

不联网、不改源文件。空字符串、NA、N/A、null、none、NaN 按缺失统计；数值推断排除 Infinity 等非有限值。候选类型不能决定业务聚合。

## 分层验收 [R09]

1. **数据与语义：** 从原始分子分母、配对或时间戳重算重点；检查排序、单位、筛选、n、区间与标题；对照图形坐标与值。SVG 包含某个数字不等于编码正确。
2. **图形与版面：** 实际渲染目标尺寸；检查裁剪、重叠、字体、密度、焦点、尺度与静态可读性。自动边界检查不能代替看图。
3. **交互：** 实际执行主要筛选、单位切换、复位和键盘路径；逐项核对数据、分母、标题、摘要；检查空结果、缺测与降级。
4. **读者理解：** 预先定义可核验问题，真实目标读者完成任务；记录正确性、时间、误读与解释过程。模型从原始数据答对，不等于人从图中能答对。

每项记录 status（pass / fail / not_run / not_applicable）、method、evidence、scope、limitations。状态绑定文件、环境、尺寸与状态，修改后重跑受影响检查。不报告无样本依据的“专业度 95 分”或“理解提升 30%”。

## 演示与检查

```sh
python scripts/build_examples.py
python scripts/validate_bundle.py
```

浏览器检查需可选 Python Playwright 与 Chromium：

```sh
python scripts/browser_qa.py
```

不会自动安装依赖。先从 Skill 根目录运行 `python -m http.server 8037 --directory docs`；浏览器脚本默认检查该本机地址，可用 `--url` 指定其他本机或已发布地址。截图在 `verification/screenshots/`，结果在 `verification/gallery-browser.json`。核心 Skill 无此依赖。
