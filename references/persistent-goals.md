# Persistent goal integration

Read when the task is ready for implementation or when resuming it. Use the names, arguments, and restrictions exposed by the current runtime. The following describes hosts with these tools; support is not guaranteed in every host.

## Check and create

1. Inspect available goal tools. Some Codex hosts expose `get_goal({})`, `create_goal({objective})`, and `update_goal({status})`. Check creation, readback, and resumption capabilities separately and record the supported operations in `STATE`. Creation support does not establish resumption support: the current `update_goal` contract only allows complete or blocked, not pause or resume. Use only a recovery operation explicitly exposed and allowed by the current host. When `functions.exec` is available, it can call `tools.*`; `functions` is not a shell executable.
2. Read with `get_goal` when available. Reuse an unfinished goal for the same task; handle a stopped goal using the recovery procedure below. If the old goal covers only a stage or conflicts with the latest task contract, record the difference and use the full contract in `STATE` for authorized work. Without a supported editing API, do not falsely complete the old goal to replace it. Never overwrite another unfinished goal. Ask for a specific user or host action only when needed to resolve a conflict. Respect user pauses and budget or usage limits.
3. Compose a self-contained objective from `STATE`: the final outcome, every important acceptance condition, required constraints, exclusions and behavior that must not change, necessary verification, the overall stopping condition, and the absolute path and section of `STATE`. State important acceptance conditions compactly and link to the detailed table; do not name only a plan or stage. If the host limits objective length, shorten the wording without dropping substantive requirements.
4. Call `create_goal` directly in the context of the user's explicit invocation of this skill. The invocation contract and UI default prompt explicitly request goal creation. Ordinary tasks and merely reading, creating, or reviewing the skill do not imply authorization for a goal. Pass `token_budget` only when the user explicitly supplies one.
5. After creation, call `get_goal` to confirm that the returned goal belongs to this task and is active. Record the actual result in `STATE`. If creation times out or has an uncertain result, read back before retrying to avoid duplicates. A tool name, feature flag, or written `/goal` command alone does not prove startup.
6. After successful creation and readback, execute the current unfinished step immediately. If no separate start API exists, do not invent one or ask the user for another command.

Objective content pattern (fill with actual facts; the user does not need to fill this template):

```text
Deliver: {entire final outcome}.
Acceptance: A1 {pass condition}; A2 {pass condition}; ...
Constraints and exclusions: {compatibility, protected behavior, and authorization boundaries}.
Verify: {necessary tests, builds, and runtime evidence}.
Complete only when the entire outcome is achieved and every necessary acceptance criterion has evidence. Handle remaining work and genuine blockers under applicable AGENTS.md and host instructions.
Recover: read {absolute STATE path and section}, applicable AGENTS.md, and latest user updates; verify actual state and continue.
```

## Recover after a wait or interruption

Run this procedure when requested information arrives, the user asks to continue, or a task is recovered after interruption or compaction. It continues an already invoked task; a discussion of the skill alone does not activate it.

1. **Reassess the cause.** Read the latest user decision, `STATE`, and actual goal state. Separate missing external information, an explicit user pause, a budget or usage limit, and a host failure. Record which dependency was resolved and its evidence. A purchased resource does not prove access works; release only steps whose inputs and permissions are sufficient. Preserve unresolved dependencies without retaining an obsolete blocker for the whole task.
2. **Apply the existing authorization.** Supplying information requested for an externally blocked task permits the already authorized dependent work to continue; no additional “resume” wording, plan approval, or skill invocation is required. New information alone does not override a user instruction to stay paused, cancellation, or a host limit. For an explicit pause, require the user's instruction to resume; for limits, follow the actual host controls. A status question or a mention of the skill does not lift either restriction.
3. **Reconcile scheduling and task progress.** After applying the authorization and limit checks above, use the cases below. A stopped goal eligible for recovery includes an externally blocked goal and a paused goal the user has explicitly asked to resume. Keep the original goal identity and acceptance criteria, and record the current recovery point. Restart any blocker audit according to the runtime's resumption rules rather than reusing an old count.

| Actual host state and capability | Action |
| --- | --- |
| Same task is active | Clear obsolete blocker records, update readback evidence, and execute the next necessary step. Do not create another goal or request another resume action. |
| Stopped goal is eligible for recovery; a permitted resume operation is exposed | Invoke that operation for the existing goal and read back its identity and status. On active, execute the next necessary step. If the call times out or is uncertain, read back before deciding whether a retry is needed. A success response followed by a still-stopped readback is not a successful recovery; use the next row. |
| Eligible goal remains stopped; no permitted resume operation is exposed, or recovery failed | Record **Host goal awaiting recovery; current conversation executing** when work can proceed. Immediately tell the user that automatic goal continuation has not resumed, why, and the supported recovery control. For a supported Codex desktop host, use its goal bar's Resume control; use `/goal resume` only in an interface that supports that command. Continue authorized work without waiting for that click, but do not promise further automatic turns. |
| Readback fails or conflicts with the expected task | Record status as unverified with the last known state and timestamp. Investigate the mismatch; do not guess active, mutate a different goal, or blindly repeat a mutation. Continue only work whose authorization and ownership remain clear. |
| User pause, cancellation, or an unlifted host limit | Retain the restriction and its recovery condition. Do not use conversation fallback, a new goal, or another execution path to bypass it. |

4. **Close the recovery record.** Keep task progress, actual goal state and timestamp, recovery capability, pending action, and the notice already delivered in `STATE`. Give the notice on the first recovery failure or mismatch instead of waiting for a status question. If an uncertain call is resolved by the immediately following readback in the same turn, combine the outcome into one notice; if it remains uncertain, say so promptly. Do not repeat an unchanged notice or re-request the same resume action on every reply; report a change, new failure, or explicit status request. When a fresh readback shows active, clear the pending host action. User assertions or a successful resume response without readback do not prove it.
5. **Report only observed continuation.** Continuing chat, modifying `STATE`, and goal readback are not evidence of an automatically scheduled next turn. Mark automatic continuation verified only if the host actually initiates a subsequent goal turn and it performs necessary work without another user nudge. Otherwise leave it unverified. This is scheduling evidence, not an extra business acceptance condition; do not manufacture idle turns or delay completed work to obtain it.

An external change that happens while no turn is running cannot be detected by this skill alone. Record how the next input or supported host event will trigger reassessment; do not promise unattended wake-up or create a monitor without a user request.

## Unavailable or restricted

Distinguish a disabled feature, tools not exposed, a failed call, a goal conflict, and a user pause. Documentation describing a feature does not establish that this conversation can call it.

If Codex CLI is installed and the feature might be disabled, check `codex --version` and `codex features list`. Only when this version supports `goals`, it is disabled, ordinary feature enablement is authorized for this task, and the host permits it, run `codex features enable goals`. Preserve other settings and verify again. A true flag does not guarantee that a running conversation gains tools. Do not restart or interrupt the user's work to test this.

If there is no supported goal interface for the current conversation, or it remains unusable after a normal repair targeted at the known cause, record that persistent goal startup is unavailable, the checks and error evidence, any repair, and the fallback execution mode in `STATE`. Briefly explain the limitation to the user. Continue currently executable work under applicable AGENTS.md and host instructions while retaining the complete state and recovery entry point. Do not claim goal mode is active or promise execution after the application closes.

Never fabricate startup by changing internal Codex databases or transcripts, injecting commands into an input field, or creating scheduled tasks. A user pause or budget limit is not a technical failure and must not be bypassed through fallback execution.

## Complete or blocked

Only perform the supported completion operation and read back its result when the overall outcome and every necessary acceptance condition are satisfied. Finishing a stage, writing a document, passing one test, or making a local commit is not overall completion.

Use `update_goal` only for states allowed by its current contract. Obey its actual-blocker definition, consecutive-turn threshold, budget constraints, and user-resumption rules. Record an initial local blocker and continue independent work instead of marking the whole goal blocked early. When its overall blocker conditions are met, report them truthfully. Do not manufacture empty turns to reach a threshold or falsely report complete just to stop.

Before marking an overall block, retain the blocker, affected steps, resolution evidence needed, remaining independent work, and resumption point in `STATE`. Explain that the goal is incomplete and automatic continuation will stop. If resumption requires a host control, include that action in the same notice and record its delivery; follow the recovery procedure when input arrives. Do not keep a genuinely blocked goal active merely to avoid the host's recovery limitation.

## Interface references

Goal availability depends on the version, host, and current conversation. Installing this skill does not make missing tools available; check the runtime each time.

- [Official skill and explicit-invocation configuration](https://learn.chatgpt.com/docs/build-skills)
- [Official persistent goal guide](https://learn.chatgpt.com/use-cases/follow-goals)
- [Official desktop goal controls](https://learn.chatgpt.com/docs/long-running-work)

A skill contains instructions and resources loaded on demand. It is not a background process; the supporting host owns persistent scheduling.
