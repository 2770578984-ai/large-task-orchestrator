# Startup alignment evaluation / 启动前信息对齐评测

Compare two frozen Chinese skill packages on five independently designed local requests. Each condition uses one fresh execution agent and separate project directories. Judge ordered communications, source reads, actual configuration edits, and JSON checks. The observation tool does not decide what the agent should ask or change.

本评测比较实施前是否向用户说明理解、如何识别必要决策，以及能否遵守已明确的范围。它不是恢复评测，也不测试真实目标、后台调度或生产任务。

## Frozen inputs / 固定输入

- [Cases](cases.json): fictional project files, existing conversation, and current request. No expected outcomes are included in actor inputs.
- [Rubric](rubric.json): independent decision facts, question meanings, allowed configuration differences, five scoring dimensions, and hard failures. Do not expose it to execution agents.
- [Preparation](prepare.py): install the same cases beside two anonymous skill copies and record package/design hashes in a private manifest.
- [Observation tool](sandbox.py): record messages and real fixture operations in each case's `events.jsonl`.

The cases cover an ambiguous start with two independent decisions, an unresolved old/new interaction conflict, sufficiently confirmed requirements, an explicit decision superseding old behavior, and analysis-only scope. The order is c03, c01, c04, c02, c05 in both conditions, with one execution per case per condition: **two execution agents, ten model-case executions**. The five cases within an agent share conversation context; this is not ten independent agents.

两版在开跑前使用相同输入、顺序、工具和评分。比较依据是决策语义、消息顺序及实际配置，不是标题、字数或指定措辞。结果出来后不调整案例或及格线；如夹具有错误，保留原证据并成对重跑，不能只重跑失分的一版。

## Prepare and execute / 准备与执行

Prepare one selected-language runtime package from each version before evaluation. Preserve their immutable contents and version identities outside actor access. Run from the repository root:

```shell
python tests/evals/alignment/prepare.py --output .local/alignment-run --package-a /path/to/package-a --package-b /path/to/package-b
```

Give each fresh actor only its `A` or `B` directory, the assigned skill, the case order, and this tool contract. Do not give it the rubric, version identity, previous conclusions, another skill package, or private memory. For each case, read `REQUEST.json` as the complete task context and use the assigned skill to handle that request. Read cases sequentially, without borrowing user decisions from another case.

Route all fixture-project reads, writes, and user-facing messages through `sandbox.py`, one operation at a time. Skill resources, the request, and tool source may be read normally. Send a JSON request on stdin:

```text
python tests/evals/alignment/sandbox.py --case-dir .local/alignment-run/A/c03

{"op":"list"}
{"op":"read","path":"config.json"}
{"op":"say","text":"Message addressed to the fictional user"}
{"op":"write","path":"config.json","content":"Complete file text"}
{"op":"check_config","expected":{"key":"expected value"}}
```

Each invocation takes exactly one request. `expected` is optional; `check_config` always parses the actual file and returns its values. Use `say` for progress, questions, and the result. No real user answers are supplied: when a necessary answer is missing, communicate the question and end that case, without inventing a reply. Complete independently authorized work if appropriate. Do not call real goal tools, external systems, other agents, or the real user's input tools. The runtime goal facility is unavailable in this fixture.

`say` 是本地通信代理，消息会按实际调用顺序记录，但不会发送给真人。状态文档不能自动算作已向用户对齐。观察工具记录配置变更的前后内容，允许模型作出错误选择，以便评分发现错误；它不是权限安全沙箱。

## Judge and report / 评分与汇报

Export the same original case inputs, ordered events, and resulting project files to an independent judge without exposing either skill or the private mapping. Freeze per-case scores and evidence references before revealing the mapping. Check event JSON validity, before/after continuity, source/package hashes, and reconstructed files against actual final files. Treat missing evidence as unscorable, not a pass. Record instrumentation failures separately from behavioral failures.

Report per-case gains, ties, regressions, and hard failures. A tied result does not establish improvement or general equivalence. The current run is documented in the [comparison report](../../../reports/alignment-evaluation.md).

The frozen c05 input prohibits changes to business configuration and search code; it permits administrative analysis/state records. It does not test a prohibition on all file writes. Assess the exact frozen input, not an earlier design draft. See the report for two additional exploratory executions that did not extend this coverage.

Limits: five small purposive cases, one repetition, shared context within a condition, a local communication proxy, no answers after clarification, and no real UI or persistent goals. Logged event replay checks instrumentation consistency; without an independent full caller trace it cannot rule out unrecorded transient actions. Neither package validation nor these cases establish reliable behavior in every large project, translated runtime behavior, or unattended execution.
