# Work log / 工作记录

Current: startup alignment is explicit in both languages and the installed Chinese skill. The main comparison scored 49/50 versus 50/50, with both versions passing five cases; only one acceptance-communication gain was observed. 当前：双语技能及本机中文版已增加启动前信息对齐，主对照仅测得一处验收沟通改善，不能据此宣称全面提升。 Recovery policy is unchanged; its earlier A/B comparison tied and did not establish native automatic resumption. 恢复规则保留，此前恢复对照打平，未证明原生自动接续。

## 2026-09-09

- Prepared equivalent English and Chinese skill instructions, persistent-goal references, task templates, UI metadata, and README files. 整理中英文技能与配套资料。
- Added a standard-library installer that selects one language and refuses existing destinations. Added package and installer checks. 增加语言安装、防覆盖与包检查。
- Kept runtime goal capability checks and explicit-only invocation, and removed installation-specific facts from the public instructions. 保留运行时核验与显式调用，移除仅适用于作者环境的事实。
- Public source includes no private execution transcripts or application configuration. 开源源文件不包含私人运行记录或应用配置。
- Validation: five installer tests and package checks passed; both selected-language packages passed the official skill-creator structural validator and were discovered by Codex app-server with correct display names and no loading errors. 验证：5 项安装测试、包检查及两种语言的官方结构检查通过；实际发现与中英文名称正确。
- Reviewed translation parity, preserved the original installed skill, and scanned public files for private paths, credentials, and session identifiers with no matches. 审查双语一致性，保留原安装；公开文件隐私检查无命中。
- These checks validate packaging and discovery; they do not extend the original edition's behavior evidence to multi-hour scheduling or every translated workflow. 包检查不扩大原始行为实测的结论范围。

## 2026-09-10

- Separate continued task work from persistent-goal scheduling. Reassess externally blocked steps when requested information arrives, retain the original goal and evidence, and respect explicit pauses and host limits. 区分工作继续与目标调度，信息到位后重查阻塞，保留原目标及证据，遵守暂停与用量限制。
- Check resume capability independently of creation, read back recovery results, and immediately explain any necessary host action. Track pending recovery and notices without repeating unchanged requests. 单独核验恢复能力，读回结果，及时说明宿主恢复动作并记录，避免重复提示。
- Extend the task template and bilingual READMEs with actual goal status, recovery capability, and observed automatic-continuation evidence. Add synthetic recovery inputs and an independent evaluation rubric outside the runtime package. 补齐模板及双语说明，新增不随技能加载的恢复评测资料。
- Validation: five installer tests, package checks, official structural checks for both language packages and the installed skill, and actual Codex discovery of all three packages passed. Installed Chinese display name, explicit-only policy, and existing resource paths are preserved. 已通过五项安装测试、包检查、三个包的官方结构检查及实际发现；安装版保留中文名称、显式调用策略和既有资源路径。
- Independently reviewed 12 synthetic recovery decisions against their observable checks: unavailable resume operations, partial input, retained or explicitly released user pauses, host limits, active readback, timeout reconciliation, genuine blocking, readback failure, local blockers, and a success response with still-blocked readback. Kept missing returns unverified. 独立评测并复核 12 个合成恢复情境，覆盖上述分支；缺失返回保持未核验。
- The evaluation identified ambiguous execution-mode examples and transient-failure notice timing; both language templates and references now clarify them. Synthetic inputs also distinguish post-recovery scheduling evidence from audit triggers. 根据评测补清执行模式示例、同轮异常提示合并及模拟调度证据的范围。
- No live persistent goal or production task was used as a fixture. The current host exposes no permitted agent resume operation, so native automatic resumption and subsequent unattended scheduling were not validated. Simulated decisions and package discovery do not establish that capability. 未使用真实目标或生产任务作为夹具；当前宿主没有获准调用的恢复接口，原生自动恢复及后续无人催促调度未实测，模拟与发现检查不扩大这一结论。

### Comparative evaluation / 旧新版效果对照

- Correct the evidence boundary: the earlier 12-case review tested only the revised skill and did not demonstrate an advantage over the initial release. 明确此前 12 例是新版单独评测，不能证明比旧版更好。
- Compare commits `39470af` and `755569a` using independent case design, masked skill snapshots, actual local CLI artifacts, and blind grading. Eight primary cases and two separately preregistered supplemental cases, two repetitions per version. 独立设计、冻结输入与评分，执行者不见版本身份，评分者不见技能。
- Ten fresh execution agents performed 44 model-case executions: 40 scored observations and four original observations replaced by a paired infrastructure rerun. Both versions scored 16/16 primary and 4/4 supplemental passes, all 10/10; no critical failures, unnecessary user actions, or missing notices were observed in retained evidence. 两版主实验与补充实验均打平，未测得相对优势。
- Fix a simulator concurrency defect with cross-process locking. Replay retained logs without changing original evidence; rerun both sides of the two cases with truncated logs using fresh agents. Replay is instrumentation validation, not more model samples. 修复审计并发问题，留存日志核验语义等价，损坏日志两版成对重跑，不虚增样本数。
- Retained-log replay cannot independently rule out entirely missing original calls; full actor tool history was not cross-audited. Disclose this additional limit rather than treating the scores as strict superiority evidence. 披露原调用历史未独立逐项核对的完整性限制，回放一致不当作原始记录完整性证明。
- Add the reusable benchmark, evidence exporter/replayer, fixture tests, comparison report, and aligned README evidence disclosures. Preserve runtime skill files; the installed Chinese package matches the evaluated candidate after normalizing existing resource links. 补齐评测与文档，运行时技能正文保留已发布修订，本机安装与候选核对一致。
- Validation: 28 software tests and package checks passed. These are separate from the 40 scored behavioral executions. No live goals, production services, real UI controls or unattended scheduling were tested. 原始运行明细留在本地，不入公开仓库。

## 2026-09-12

- Reduce the bilingual task templates to core goal, acceptance, plan, blockers and completion fields. Expand runtime-goal, recovery and unattended-continuation evidence only when relevant; keep identity, evidence and authorization requirements. 中英文任务模板保留核心状态，运行时目标、恢复和自动续轮证据按需展开，身份、证据和授权边界保留。
- Align both skill entrypoints and synchronize the selected-language local installation. Explicit-only UI metadata and persistent-goal references are unchanged. 同步双语入口与本机选定语言安装版；显式调用元数据及恢复规则原文未改。
- Validation: package validation and 28 software tests passed. Independent forward reading exercises the compact template; this is not a new recovery A/B comparison or evidence of native automatic resumption. 包检查和 28 项软件测试通过；独立前向阅读覆盖简化模板，不作为新的恢复对照、质量提升或原生自动恢复证明。

## 2026-09-13

- Make startup alignment visible after investigation and before implementation: explain the outcome, scope, acceptance, important sources, assumptions, and unresolved decisions. 调查后、实施前向用户对齐信息，不能只写任务文档或宣布开始。
- Distinguish current implementation from requested behavior. Do not silently preserve an old feature or retire an omitted one without sufficient decision evidence. 已有明确决定时直接落实，重要取舍未明确时集中询问；信息充分后自动执行，恢复时复用已有对齐。
- Align the English/Chinese skill, UI prompt, template, and README, and synchronize the existing selected-language installation after checking and backing it up. 同步双语资源及本机安装，保留显式调用、授权边界和目标恢复规则。
- Add independently designed startup-alignment cases, a local observation tool, and isolated old/new execution. Results and limits are recorded in [the comparison report](reports/alignment-evaluation.md). 增加独立案例设计及旧新版隔离执行，对照结果与限制以报告为准。
- Main blind grading found 49/50 versus 50/50: one improvement in communicating acceptance before implementation, equal pass counts. Two exploratory executions did not test strict zero-file-write behavior because the frozen case permitted analysis records; a review using pre-freeze draft wording was corrected and its unnecessary rule removed. Ten scored cases, twelve total model-case executions; the delivered runtime matches the main candidate. 主评测仅一处验收沟通改善；纠正混用案例草稿的复核误判，两次追加运行不计为新增通过或只读保证，运行时回到主评测快照。
- Validation: 28 software tests, package/link checks, Skill Creator validation, installation parity, and actual app-server discovery passed. Observation records matched final files; execution logs and frozen hashes remained intact. No GitHub push or live business operation was performed. 验证通过；日志、备份和机器路径不入库，本轮未推送或操作业务系统。
