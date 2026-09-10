# Recovery A/B evaluation / 恢复行为对照评测

This benchmark compares two committed Chinese skill packages using a local stateful host. It measures actual tool choices, verified artifacts, authorization boundaries, and truthful recovery reports. It does **not** exercise native Codex goals, production systems, real UI controls, or unattended future turns.

本评测比较两个已提交的中文技能版本。执行者调用本地模拟宿主，实际生成准备文件与验证回执，再由不知道版本的独立评分者检查动作和陈述。模型说“会执行”不等于执行通过；模拟 active 也不证明真实后台调度。

## Frozen design / 冻结设计

- [Cases](cases.json): eight independently designed inputs, shared by both versions.
- [Rubric](rubric.json): four dimensions, ten points, and non-compensable critical failures.
- [Design](design.md): construction independence, masking, repetitions, and limitations.
- [Pre-registration](pre-registration.md): actual execution configuration and improvement criterion fixed before actor outputs.

Keep cases, rubric, host, packages, prompts, and sampling settings unchanged within a comparison. If a fixture defect invalidates a case, document it and rerun both versions for that case. Do not selectively retry poor outcomes or rewrite expectations after observing results.

案例、评分、宿主、技能快照和执行提示在开跑前固定。夹具缺陷导致无效时，记录原因并重跑对应的两版；不根据哪版失分调整标准或只重跑低分结果。

## Run / 执行

```shell
python -m unittest discover -s tests -v
python tests/evals/recovery_ab.py prepare --output .local/ab-example --design tests/evals --old-ref OLD_COMMIT --new-ref NEW_COMMIT
```

Preparation snapshots the selected language from Git, records hashes, and creates four independent actor directories. Each actor handles eight distinct case directories in a seeded order. `.control/manifest.json` contains the private version mapping and configuration; actors and judges must not read it. Use the same inherited model configuration without overrides and fresh agent context for each actor. The two actors in a repetition use identical case ordering. Context is shared among an actor's eight cases, a limitation even though files and host states are isolated.

Use [actor-prompt.md](actor-prompt.md), replacing only paths, run ID and the case order from the manifest. Assign R01/R02 concurrently, then two fresh actors for R03/R04. Record agent identities and elapsed time privately. Do not give an actor the rubric, another skill, previous results, or hidden host state. The wrapper supplies a test environment, not additional user authorization.

The CLI contract is discoverable through `capabilities`:

```shell
python .local/ab-example/recovery_host.py --case-dir .local/ab-example/R01/R01-C06 capabilities
```

The host creates actual local artifacts and audits every operation. Read errors, timeout responses and rejected operations specified by the cases are valid observations. A3 remains unmet throughout; completion is not permitted. Paused and budget-limited cases reject work. External blocking alone does not revoke authorized work or resume the goal.

After a complete paired batch, export blinded evidence:

```shell
python tests/evals/recovery_ab.py export --output .local/ab-example --run-ids R01 R02
python tests/evals/recovery_ab.py export --output .local/ab-example --run-ids R03 R04
```

Give an independent judge only the exported evidence, cases and rubric in `judge/`. Require per-dimension scores, critical failures, evidence references, unnecessary user actions and missing required notices. Score before revealing the version mapping. Check the judge's findings against actual CLI events and content hashes; keep an audit trail for any factual corrections, never silently change the frozen criteria.

An `audit_errors` entry means the record is incomplete: exclude the affected pair and repeat both versions with fresh actors after fixing the fixture. Preserve the original records. Private audit-counter defects with complete records can also be checked by deterministic operation replay; retain a score only when every observable return, goal business state and artifact matches. Any semantic mismatch requires paired actor reruns. Replay validates instrumentation and does not count as another model evaluation:

```shell
python tests/evals/recovery_ab.py replay --output .local/ab-example --destination .local/ab-replay --run-ids R01 R02 R03 R04
```

The host serializes operations across processes, including reads that update audit counters. This prevents parallel CLI calls from truncating audit records or losing state updates.

Replay alone cannot prove that an earlier audit captured every original call. Compare against an independent caller trace when available; otherwise disclose unverified history completeness and do not treat replay agreement as a strict proof of comparative performance.

在揭盲前逐例评分。先核对实际产物和调用，再判断状态文件与回复是否真实；允许不同措辞，不按字数或特定标题得分。报告两次重复、逐例差异及关键失败，不能用平均分掩盖暂停/预算越界。

## Evidence and limits / 证据与限制

Keep raw runs and local paths outside Git. Publish only reviewed, sanitized cases, aggregate results, relevant evidence and hashes. This benchmark does not cover starting from a vague new task, explicit-only discovery, full acceptance completion, long context recovery, or real goal scheduling. Test these separately when changing those behaviors. Exact provider model snapshots and sampling parameters may be unavailable; disclose that rather than claiming exact reproducibility.

The original [recovery review](../RECOVERY.md) is a separate single-version scenario review. It is not old/new comparison evidence. A/B outcomes must name the compared revisions and the tested scope.

## Supplemental pair / 补充对照

[Two supplemental cases](supplemental/design.md) cover an information-only update without a continuation instruction, and an explicitly lifted pause. They were registered after the main experiment started but before inspecting its behavioral outputs. Keep their eight executions separate from the main 32; use four additional fresh actors and the same packages/host:

```shell
python tests/evals/recovery_ab.py prepare --output .local/ab-supplemental --design tests/evals/supplemental --old-ref OLD_COMMIT --new-ref NEW_COMMIT --fixed-order
```

For each supplemental actor, adapt only the case count, paths and frozen order in the same actor prompt. The first repetition uses C09 then C10; the second reverses that order. The same blinded grading protocol applies.
