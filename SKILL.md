---
name: large-task-orchestrator
description: Use only when the user explicitly invokes $large-task-orchestrator, selects Large Task Orchestrator, or asks to use this skill. Turn a complex request into a task definition, acceptance criteria, a plan, and recoverable state through investigation and necessary decisions, then start persistent goal execution when ready. Do not activate for ordinary complex tasks, status questions, or a mere mention of the name.
---

# Large Task Orchestrator

Turn an initial request into a complete, implementable, verifiable task and proceed into execution. Explicitly invoking this skill requests creating and starting a persistent goal for this task once it is ready, without another goal command. Respect any current request for analysis only, a pause, or other limits. Searching, reviewing, or editing this skill is not an invocation.

This skill owns requirement clarification, the task contract, the state entry point, and goal integration. Follow applicable global and project AGENTS.md instructions for sustained execution, local blockers, repair, recovery after compaction, and stopping; do not create a competing rule set. If no user-defined AGENTS.md exists, follow the host instructions and the task contract established here; the author's private rules are not an installation requirement. Maintain state and communicate in the user's language. Invocation does not expand permission for real accounts, spending, production, deletion, or external communication, and cannot override system or tool restrictions.

## 1. Investigate before identifying gaps

Understand the current user objective, conversation context, confirmed decisions, and applicable AGENTS.md instructions. Check existing task state to distinguish a new task from a recovery. Inspect relevant project structure, code and existing implementation, configuration, tests, documentation, conventions, and directly accessible external information. Locate relevant material with directory listings and search before reading it; an exhaustive repository scan is not a prerequisite.

Separate facts, user decisions, engineering assumptions, and unknowns. Keep sources for important findings. If the task itself is missing, ask only for the actual request; do not invent a task or goal.

Check whether the relevant dimensions below are clear enough for implementation. Omit irrelevant items instead of making the user answer a questionnaire:

- Final outcome, current state and problems, required behavior, observable effects, and behavior that must remain unchanged.
- Technical, business, compatibility, performance, security, data, and environment constraints.
- External systems, real accounts, high-impact dependencies, and the authorization granted for this task.
- Included and excluded scope, and how completion will be demonstrated.

## 2. Ask only for decisions the user must make

Resolve information available through investigation and routine choices consistent with the existing architecture yourself. File locations, naming, ordinary implementation, error handling, tool choice, and appropriate validation are engineering decisions.

Ask only about consequential product behavior, business rules, compatibility or data-structure choices, authorization boundaries, or required access and information that cannot reasonably be inferred. Check decisions and permissions already given in this task before asking again. Use established secure authorization channels for credentials; never put them in the task document.

Batch currently known, independent questions wherever possible. Explain each decision's importance, affected work, main options and tradeoffs, and a recommended choice with its reason when appropriate. Distinguish work that must wait for an answer from work that can proceed on a recorded assumption. Never replace a required answer with a default or timeout. Continue independent investigation and preparation while waiting. Ask follow-up questions when new evidence requires them, not as a sequence of minor implementation questions.

## 3. Establish one recoverable task entry point

When implementation has enough information, fill in the [task template](assets/current-task-template.md) yourself; do not hand the user a blank template. If a required decision is still pending, save the known definition and blockers as a draft as well.

Select `STATE` in this order and record its absolute path and section in progress updates and the goal:

1. Reuse this task's section in an existing project status document, adding the information required by the template while preserving other sections.
2. Otherwise create a fixed `CURRENT_TASK.md` in the actual project root. For a Chinese-language task, `当前大型任务.md` is an equivalent default. Without a project, use the current writable working directory, never the global skill installation directory.
3. Keep updating that entry point instead of creating files per stage, retry, or date. Reuse it when resuming the same task. Before starting a new task, check previous state and retain any necessary completion summary through the project's existing history mechanism. Never overwrite another unfinished task. Concurrent tasks need distinct sections or the project's established isolated workspaces, with ownership recorded.

Give acceptance criteria stable IDs such as A1, observable pass conditions, a verification method, evidence, and an explicit Met / Not met result. Unverified criteria remain Not met with a reason; planned execution is not evidence. Cover normal behavior, necessary error paths, compatibility, and relevant regressions. Choose tests, builds, or real execution according to risk, avoiding unrelated checks.

Use as many steps as the task needs. Record each step's status (Pending / In progress / Complete / Blocked), dependencies, acceptance IDs, and output. Merge the template's core facts into an existing document, keeping each status, progress item, and validation result in one place. Expand optional detail only for relevant dependencies, decisions, or recovery problems; do not mechanically fill every block.

## 4. Start persistent goal execution automatically

Once investigation is sufficient, the complete definition, acceptance criteria, and plan exist, necessary decisions have answers, and no genuine blocker prevents starting, follow [persistent goal integration](references/persistent-goals.md). Check runtime tools, create or reuse the goal, read back the result, and execute the first unfinished step. Continue independent work when only part of the task is blocked.

The task document is not an approval gate. Do not ask whether to start, approve the entire plan, or enter the next stage. If the user explicitly requests analysis and a plan only, deliver that scope without creating an implementation goal or changing the implementation. Respect runtime restrictions; this skill cannot bypass read-only or Plan mode.

## 5. Keep implementation facts in the task contract

Update `STATE` when a stage, important decision, or assumption changes; when problems or blockers appear; after validation; and before compaction or handoff. Preserve the final outcome, constraints, acceptance IDs, current step, completed and remaining work, problems, blockers, and evidence. Keep current state concise and link long logs. Revise steps, dependencies, and verification plans when facts justify it, recording why. Ask again only for changes to the user's outcome, important constraints, product or business decisions, or authorization. Never silently weaken acceptance criteria.

On recovery or receipt of missing information for this task, read `STATE`, applicable AGENTS.md instructions, and the latest user updates. Verify the directory, branch or working-tree changes, and runtime facts. Reassess the affected blockers and follow the recovery procedure in [persistent goal integration](references/persistent-goals.md). Supplying the requested external information is enough to continue previously authorized work; do not require a special “continue” phrase or another skill invocation. An explicit user pause or usage limit still applies until properly lifted. Preserve valid evidence and ownership of other tasks' changes.

Track continued task work and the host goal's actual state separately. If work can proceed but the goal remains blocked, immediately explain the supported recovery action and record it in `STATE`; do not leave the limitation only in the document or describe the goal as active. A readback of active and an observed automatic follow-up turn are different evidence.

Before finishing, compare the original outcome and latest user decisions with the requirements, constraints, every acceptance criterion, remaining work, blockers, and verification results in `STATE`. Follow global instructions to investigate failed tests, repair and verify again, and complete executable necessary work. Only mark the goal complete under the current tool contract when the entire outcome is achieved and every necessary acceptance criterion has supporting evidence.

The final report states completion of the outcome, key changes, important decisions and assumptions, actual validation and acceptance results, known limitations, and unresolved issues. If external conditions block completion, report verified progress, affected steps, the required input, and the recovery entry point. State that the overall task remains incomplete; do not use completion language or replace executable work with an offer to continue.
