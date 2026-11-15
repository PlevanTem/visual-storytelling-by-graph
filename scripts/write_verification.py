"""Write a scoped verification ledger from existing evidence, without fabricating results."""
import hashlib,json,platform
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(name):
    p=ROOT/name
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else None
def status(value):return '通过' if value=='pass' else '失败' if value=='fail' else '尚未执行'
def main():
    s=read('verification/structural-checks.json');b=read('verification/gallery-browser.json');pub=read('verification/deployment.json');installer=read('verification/installer-check.json')
    sb=status(s.get('status') if s else None);bb=status(b.get('status') if b else None)
    pub_current=bool(pub and pub.get('status')=='pass' and all((ROOT/c['file']).exists() and hashlib.sha256((ROOT/c['file']).read_bytes().replace(b'\r\n',b'\n')).hexdigest()==c.get('sha256') for c in pub.get('checks',[])))
    remote='已发布且HTTP核对通过' if pub_current else '上一版本已核验；当前改动待发布' if pub else '尚未执行'
    install='隔离项目安装、读取和发现通过' if installer and installer.get('status')=='pass' else '命令按官方文档提供，尚未实际运行'
    text=f'''# 验证记录 / Verification ledger

2026-11-15 · visual-storytelling-by-graph · 0.2.0

20件画廊作品，31个展示状态，62份完整桌面／手机SVG；24个模拟请求，23份JSON数据。全部数据为合成数据。基础版保存在此前本地交付中，本报告不把旧版检查自动算作新版通过。

## 已执行情况

| 检查 | 状态 | 范围与证据 |
|---|---|---|
| Skill命名与格式 | 通过 | skill-creator quick_validate实际运行；根目录frontmatter与调用名一致 |
| 结构与链接 | {sb} | [确定性记录](structural-checks.json)；24个请求与对应数据、页面资源、本地链接 |
| 数值与实际编码 | {sb} | 62份画廊SVG的坐标、路径、面积、分母与变换；另核对原有16份基础SVG与CSV边界输入 |
| 浏览器页面和状态 | {bb} | [浏览器记录](gallery-browser.json)；Chromium桌面1440×1000，全部31状态；手机390×844，20件默认作品 |
| SVG文字布局 | {bb} | 62份完整SVG文字边界与两两相交检查；不代表发现全部图形遮挡 |
| 页面交互 | {bb} | 分析目的筛选、场景入口、案例直达、需求模板复制、展览打开／关闭、焦点恢复、方向键、Escape、参数、作品解读、中英文与当前SVG导出 |
| 独立Agent前测 | 完成4请求 | [独立报告](independent/REPORT.md)；C15/C17/C19/C23，7个SVG状态；114项数据／编码断言，11项浏览器检查 |
| 快捷安装器 | {install} | {'[发现记录](installer-check.json)' if installer else '以仓库根目录SKILL.md作为发现入口'} |
| GitHub Pages | {remote} | {'[发布与HTTP证据](deployment.json)' if pub else 'main /docs 静态发布，当前尚未把计划标为上线'} |

浏览器环境：Chromium {b.get('browser','未记录') if b else '未记录'}；Python {platform.python_version()}。无需框架或CDN；浏览器QA需要已有Python Playwright与Chromium。

## 重要发现与修正

- 用户入口按使用场景、案例效果、能力边界、快速上手与方法架构重组；重建命令和工程细节移至[维护索引](../guides/maintaining.md)。此调整不改变图表计算与几何。
- 新版风玫瑰手机视图的北向标签与速度图例相交，已调整图形中心与半径并重跑。保留[修正前记录](iterations/gallery-before-wind-spacing.json)。
- 看图后拉开KM风险集行标签与首列数字，补齐老化周期与Bland–Altman两轴语义，并重跑受影响检查。
- Hero仅裁切预览框，不改变三元坐标；移除了裁切中不完整的图例与标题线。完整图和数据仍在展览中。
- STFT输入明确为频率随时间增加的合成扫频与38Hz固定分量，图中是全局参考的相对幅度，不是PSD或声源识别。
- 新增独立前测从原始请求和数据执行，未提供作者图、评审答案或预期数值。独立执行者报告未读取禁止材料；这不是完整访问审计或真实读者研究。
- 独立产物与主画廊分开保留。重复构建、归档或重测不会增加独立样本数。

## 观察边界

已直接查看桌面／手机首屏和代表性图表截图，并针对观察到的问题修正。作者看图是主观产物检查，不等于高审美已得到盲测或统计验证。画廊的暗色、衬线排版和异幅编排是设计选择。

## 尚未执行

- 真实目标读者的读图正确率、耗时、误读、审美偏好实验。
- 控制模型、工具、数据与预算的无Skill／有Skill对照。
- 多模型、多次独立运行与未见数据上的泛化测试。
- Firefox、Safari、实体手机触屏与完整屏幕阅读器会话。
- 每种方法的真实行业适用性、因果识别、KM置信区间或其他未声明统计推断。
- 个人全局Skill目录安装；此次实际安装仅发生在隔离测试项目，未使用全局安装参数。

## 复验

```sh
python scripts/build_examples.py
python scripts/build_gallery.py
python scripts/validate_bundle.py
python -m http.server 8037 --directory docs
```

另一个终端运行 `python scripts/browser_qa.py --url http://127.0.0.1:8037/`。修改产物后应重跑受影响检查，不能沿用旧截图作为新状态证据。CI只核查已提交产物的数值和哈希，不宣称重新执行浏览器。

工作脉络：更名 → 扩展专门方法与数据 → 独立前测 → 构建画廊 → 数值与几何核对 → 浏览器与版面修订 → 仓库、安装入口和Pages发布核验。
'''
    (ROOT/'verification/REPORT.md').write_text(text,encoding='utf-8')
    print('Verification ledger synchronized with available records.')
if __name__=='__main__':main()
