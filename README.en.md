# visual-storytelling-by-graph

[中文](README.md) · [Explore the examples](https://plevantem.github.io/visual-storytelling-by-graph/) · [Get started](#get-started)

**Bring your question and data to an Agent. Choose an appropriate chart and make the important changes, differences and relationships understandable.**

For product managers, analysts, operators, researchers and teams who need to explore or explain data quickly. Start with what you want to understand; you do not need to know a chart name.

![Gallery preview](docs/assets/social-preview.png)

## When to use it

| Your situation | A useful question | What the Skill considers |
|---|---|---|
| Business reviews | What changed, and where did the gains and losses come from? | Contributions, trends, baselines and reading order |
| Product and experience analysis | Is the new version better, or does the average hide differences? | Segments, distributions, tails, sample sizes and denominators |
| Experiments and research | Which differences matter, and how uncertain are they? | Pairing, interval meaning and claim strength |
| Monitoring and diagnosis | Where are the anomalies and missing observations? | Time spacing, thresholds, gaps and useful detail |
| Complex-data exploration | How should compositions, paths, intersections or signals be shown? | Data prerequisites, specialist expressions and necessary interaction |

Simple charts remain useful for common tasks. Specialist forms are selected when the question and data warrant them.

## See what the examples reveal

[Open the gallery](https://plevantem.github.io/visual-storytelling-by-graph/). Each work includes the question, chart, parameters, reasoning, source data and interpretation limits.

| Simulated question | What becomes visible | Example |
|---|---|---|
| Did requests get faster? | p50 falls from 200 to 150 ms while p95 rises from 480 to 900 ms | [Latency distribution · C02](https://plevantem.github.io/visual-storytelling-by-graph/#work-C02) |
| Why did pooled conversion fall when both sources improved? | The source mix changes; pooled conversion falls from 50% to 34.5% | [Stratified rates · C04](https://plevantem.github.io/visual-storytelling-by-graph/#work-C04) |
| Do equal average waits mean similar experiences? | All means are 15 minutes, but the longest wait is 92 | [Exact-value beeswarm · C23](https://plevantem.github.io/visual-storytelling-by-graph/#work-C23) |
| Who became faster after training? | Eleven of twelve participants improve; one becomes slower | [Paired change · C03](https://plevantem.github.io/visual-storytelling-by-graph/#work-C03) |
| Which objects have multiple tags? | Exact intersections expose 42 multi-tag objects out of 64 | [Set intersections · C17](https://plevantem.github.io/visual-storytelling-by-graph/#work-C17) |

The 20-work collection combines everyday charts with twelve specialist examples, from compositions and censored lifetimes to intersections and time-frequency views. **All examples use synthetic data; their findings are demonstrations, not promised outcomes for your data.**

## Fit and capability boundaries

| Capability | What it needs |
|---|---|
| Comparison, trends, composition, distributions and relationships | Understandable metrics, units, periods and comparable definitions |
| Pairing, intervals and missing coverage | Object correspondence, interval meaning or sampling rules |
| Specialist compositions, paths, memberships and signals | The corresponding data structure; a path needs actual transitions |
| Annotated charts, presentation graphics, exploration and exports | An Agent that can read your data and run the necessary tools |
| Findings and candidate explanations | Supporting evidence; missing denominators, controls or other critical inputs must be made explicit |

A table may be the best answer for exact lookup. Interaction is added when it helps the task. Correlation or a before/after difference does not by itself establish causality.

## Get started

**1. Add the Skill to your Agent.**

```sh
npx skills add PlevanTem/visual-storytelling-by-graph --skill visual-storytelling-by-graph
```

Choose your Agent during installation. You can also [download the repository](https://github.com/PlevanTem/visual-storytelling-by-graph/archive/refs/heads/main.zip) and provide its `SKILL.md` to an Agent that supports local skills. [Installation options and prerequisites](guides/maintaining.md#installation).

**2. Share your question, data, reader and output.**

```text
Use $visual-storytelling-by-graph.

Question: [what you need to understand]
Data: [attach a file or paste the table and field meanings]
Reader: [who will use this, and their background]
Output: [one chart / a report page / interactive exploration]

Choose an appropriate expression and explain the findings and important limits.
Ask if a critical definition is unclear. I do not need to specify the chart type.
```

**3. Refine the first result.**

- “Compare the overall result with individual segments.”
- “Show the distribution and tail, not just the mean.”
- “Make the key finding readable in one chart for a weekly review.”

Expect an appropriate expression, a readable chart or table, findings and material assumptions. Editable, exportable or interactive outputs depend on the tools available to your Agent.

## How the method improves the design process

**Intent → data meaning → expression → narrative and interaction → checks and revision**

| Layer | The decision it adds | How it appears in a case |
|---|---|---|
| Intent | Who needs to answer which question, and why? | The same latency data can support a concise executive view or an SRE diagnosis |
| Data meaning | What is a row, denominator, unit or pair? | Conversion retains counts; paired changes connect the same objects |
| Expression | Which candidate preserves the information the task needs? | Tail questions retain distributions; exact reconciliation can use a table |
| Narrative and interaction | What should be seen first, and which actions help? | Findings are visible by default; filters update the scope and summary |
| Checks and revision | Do calculations, marks, rendering and operations agree? | Values, gaps, parameter states and exports are checked separately |

The intended advantage is a repeatable set of decisions around the user's question. Try a familiar question and dataset to judge its fit with your workflow.

The method draws on Munzner's layered design and validation, Brehmer and Munzner's task abstraction, Segel and Heer's narrative framing, and Yi et al.'s interaction intents. [Sources and adoption limits](references/sources.md).

Available evidence includes inspectable cases, chart and interaction checks, and four independent specialist Agent executions. **Controlled improvements over a baseline, human comprehension and aesthetic preference have not been measured.** [Evidence and unexecuted tests](verification/REPORT.md).

## Further reading

- [Core Skill](SKILL.md): the instructions used by the Agent.
- [Chart capabilities](references/chart-families.md) and [specialist prerequisites](references/specialized-methods.md).
- [Research and sources](references/sources.md): task abstraction, layered validation, narrative control and interaction intent.
- [Maintenance and local reproduction](guides/maintaining.md): for changing the repository or gallery; not a prerequisite for everyday use.
