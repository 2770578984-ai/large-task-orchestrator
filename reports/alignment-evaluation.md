# Startup alignment comparison / 启动前信息对齐对照

Date / 日期：2026-09-13

The skill revision makes user-facing alignment an explicit step after investigation and before implementation: communicate the outcome, scope, acceptance, sources, assumptions, and unresolved consequential decisions. An unresolved product choice cannot become a preservation constraint merely because the old code implements it. Sufficiently decided work continues without another plan-approval request.

本轮把启动前信息对齐写入中英文入口、调用提示和任务模板，并同步本机中文安装。评测检查说明与实施的先后次序、决策依据、必要问题和实际修改范围，不测持久目标恢复。

## Compared packages / 比较版本

- Baseline: commit `23b39c5184be897ea187df50333c6e7fe0aca895`.
- Candidate: the startup-alignment revision in this report's commit, frozen before the main execution agents ran. The delivered runtime instructions match this snapshot.
- Both actors loaded the Chinese runtime package. English instruction parity was reviewed, but English behavior was not independently evaluated.

SHA-256 of each `SKILL.md`, decoded as UTF-8 and normalized to LF:

| Baseline / 旧版 | Candidate / 新版 |
| --- | --- |
| `429a1d787b8e9f237f1a1d1caf2915843b0992865d33d179e22995cd7b5dcb1f` | `61defe5339fe55c9053a2b21070ba64f7f895730a5b10dd10791b9b0598e1f9e` |

## Method / 方法

An independent design agent created [five fictional cases](../tests/evals/alignment/cases.json) and a [semantic rubric](../tests/evals/alignment/rubric.json) without reading the candidate. Inputs, scoring, packages, tool, order, and repetition count were frozen before execution. Two fresh execution agents received anonymous skill copies and identical case inputs in c03, c01, c04, c02, c05 order: **ten model-case executions, one repetition per version**. No model override was requested; the actors inherited the parent configuration. An exact provider snapshot and sampling configuration were not independently verified.

Each case used separate project files. The local observation tool recorded source reads, messages addressed to the fictional user, writes with before/after content, and actual JSON checks. No follow-up answers were supplied. Necessary unanswered choices had to remain pending; approved independent work could proceed. The tool recorded choices without enforcing the expected answer.

评分者只读取匿名事件、原始案例、结果文件和冻结规则，不读取技能或版本映射。正文对齐及提问写入本地消息代理；内部任务记录不算已向用户说明。按语义评分，不要求特定标题或措辞。

Frozen input hashes (UTF-8 / LF):

- Cases: `2f634d05ebdee824276a039af199532399181a544f74e0486082b0265068990e`.
- Rubric: `41ea8d0515e3c2328dbb717a0fc6b27a7730406618a1836860d8a8d1cd108715`.

## Results / 结果

**The main comparison found one point of improvement in pre-implementation acceptance communication, with equal case-pass counts.** This is limited diagnostic evidence, not proof of general superiority.

| Case / 案例 | Baseline | Candidate | Recorded difference / 差异 |
| --- | ---: | ---: | --- |
| c01 Ambiguous start / 模糊起步 | 9/10 | 10/10 | Candidate communicated its JSON verification before editing; baseline left that detail in internal state until after the edit. 新版在修改前说明验收，旧版该项只写入内部状态。 |
| c02 Unresolved interaction / 未决交互差异 | 10/10 | 10/10 | Both surfaced the shared-undo conflict, asked the unresolved question, and retained dependent settings. 两版均识别差异并保留待决配置。 |
| c03 Confirmed requirements / 需求已明确 | 10/10 | 10/10 | Both aligned and implemented without reapproval. 两版均先说明并直接落实。 |
| c04 Explicit override / 明确覆盖旧行为 | 10/10 | 10/10 | Both followed the latest decision and preserved the protected values. 两版均采用最新决定。 |
| c05 Analysis only / 仅分析 | 10/10 | 10/10 | Both kept business files unchanged and wrote permitted analysis/state records. 两版保留业务文件，生成允许的分析状态。 |
| Total / 合计 | 49/50 | 50/50 | One score gain, four ties; no extra case pass. 一个得分改善、四个持平，通过数未增加。 |

The frozen rubric gave both versions 5/5 passes and recorded no missing/extra questions or hard failures. All 91 recorded operations matched read/write/check results and final files; frozen package and input hashes stayed unchanged. These checks do not establish full caller-history completeness.

The frozen c05 request says “今天先不改业务配置和搜索代码”; both versions respected that boundary. Its analysis/state records are permitted by the scenario. This case does not establish compliance with a different request prohibiting every file write.

主评测唯一分差依据：旧版 c01 第 6 条用户消息说明已定标题/排序和待决选择，但验收方法只见第 7 条内部状态；第 8 条随后修改配置。新版 c01 第 5 条消息已说明 JSON 校验，第 7 条才修改配置。差异是沟通内容和顺序，不能用它推断复杂项目中所有提问都更可靠。

## Additional exploratory runs / 追加探索运行

After main grading, the review mistakenly used wording from a pre-freeze case draft to infer a strict read-only defect. Two additional fresh actors then exercised the frozen c05 input with the candidate and a temporary instruction variant. Both preserved business files and wrote analysis/state records, which the actual input allows. Re-reading every input and checking its hash resolved the mistaken premise; the case had not changed during execution.

The temporary rule was removed, restoring the delivered candidate to the main tested snapshot. Keep these two executions as exploratory records, not additional scored observations or proof of a strict read-only fix. **Twelve model-case executions occurred in total; ten belong to the scored comparison.** The original main grades and cases remain unchanged.

复核应以冻结后的实际输入为准。两次追加运行没有覆盖“禁止所有文件写入”，不计为新增通过样本，也不据此增加运行时规则。它们与主评测原始记录均保留在本地。

## Package validation / 包验证

- The existing 28 software tests and package/link checks passed; these are not model-case samples.
- The installed Chinese skill and the English source passed the Skill Creator validator. The installed contents match the delivered source after normalizing existing localized resource links.
- Codex app-server discovered exactly one enabled user skill with the Chinese display name and updated invocation prompt. The explicit-only policy remains false for implicit invocation.
- The new observation/preparation tools were exercised by the actual paired runs. Existing-output refusal and out-of-project access refusal were also checked in isolated fixtures.

## Limits / 限制

- Five small purposive cases and one repetition do not establish statistical reliability or behavior in every large project. The cases make relevant files easier to locate than a large production repository.
- Each version's five cases share one agent's conversation context, so order and carryover may affect later cases. Versions and project files are isolated.
- The analysis-only case protects business configuration and code while allowing task-state files; strict zero-file-write behavior is outside the scored comparison.
- Local `say` events are a communication proxy. They show content and order relative to changes, not real delivery, user comprehension, or handling of a later answer.
- Ordered event/file consistency checks are instrumentation validation, not more model samples. Without an independent complete caller trace they cannot rule out unrecorded transient operations.
- No real goal tools, UI flow, background scheduling, production services, external recipients, forced compaction, or recovery were exercised. The earlier recovery A/B result remains a separate evaluation.

Raw execution records, installation backups, host discovery output, and private machine paths stay outside Git. See the [reusable evaluation procedure](../tests/evals/alignment/README.md).
