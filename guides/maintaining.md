# 维护与本地复现 / Maintenance

此页供修改 Skill、案例和画廊的人使用。日常分析数据，请从 [快速上手](../README.md#快速上手) 开始。

## 安装方式

快捷安装使用 [skills CLI](https://github.com/vercel-labs/skills)，要求 Node.js 22.20+。默认安装到当前项目，`-g` 为全局安装。本项目已在隔离项目中测试发现与安装，未写入个人全局目录。

```sh
npx skills add PlevanTem/visual-storytelling-by-graph --skill visual-storytelling-by-graph
```

也可以下载仓库 ZIP，让 Agent 读取根目录 `SKILL.md`，或按宿主要求放入本地技能目录。绘图和导出取决于宿主已有工具；核心指令不绑定图表库。

## Installation

The skills CLI requires Node.js 22.20+. Installation is project-local by default; `-g` selects global installation. Alternatively, download the repository and provide the root `SKILL.md` to your Agent. Isolated-project discovery and installation have been tested; personal global installation has not been performed.

## 文件索引 / Source map

| 目录 | 用途 |
|---|---|
| `SKILL.md`、`agents/` | 核心判断流程与发现元数据 |
| `references/` | 按需加载的任务、图表、方法、叙事和验证知识 |
| `evals/requests/`、`evals/fixtures/` | 模拟请求和固定原始数据 |
| `evals/cases.json` | 评审事实与设计约束；独立执行者不先读答案 |
| `site/` | 页面源文件 |
| `docs/` | 生成后的 GitHub Pages 发布文件 |
| `scripts/` | 固定示例构建、CSV审计和验证工具 |
| `verification/` | 检查、独立执行、安装和发布证据 |

## 重建与预览 / Rebuild

Python 3.10+，核心构建与确定性验证使用标准库。构建脚本复现固定示例，不是任意数据的自动选图引擎。

```sh
python scripts/build_examples.py
python scripts/build_gallery.py
python -m http.server 8037 --directory docs
```

打开 `http://localhost:8037/`。修改页面内容主要编辑 `site/`；作品元数据和生成逻辑在 `scripts/build_gallery.py`。图表变换与几何在 `scripts/gallery_charts.py` 和 `scripts/gallery_math.py`。

## 验证 / Checks

```sh
python scripts/validate_bundle.py
python scripts/browser_qa.py --url http://127.0.0.1:8037/ --initial
```

浏览器检查需要已有 Python Playwright 与 Chromium，不会自动安装。`--initial` 跳过远端仓库 ZIP 下载。截图在 `verification/screenshots/`。

更改页面或图表后，旧浏览器哈希会失效；应先运行受影响的浏览器检查，再运行完整验证。CI检查提交的数值、编码、资源和证据哈希，不会把旧截图当作新的浏览器测试。

## CSV审计

```sh
python scripts/audit_data.py your-data.csv --output audit.json
```

仅检查文件层面的缺失、重复、范围和候选类型，不修改输入，不推断业务单位、分母、配对或因果。

## 发布 / Publication

GitHub Pages 从 `main` 的 `/docs` 发布。推送后检查CI、Pages构建与公开HTTP文件；发布记录和实际检查范围见 [验证报告](../verification/REPORT.md)。

研究原始来源见 [来源索引](../references/sources.md)。真实读者理解、审美与无Skill／有Skill的对照实验是独立工作，不由重建命令证明。
