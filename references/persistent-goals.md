# Persistent goal integration

Read when the task is ready for implementation or when resuming it. Use the names, arguments, and restrictions exposed by the current runtime. The following describes hosts with these tools; support is not guaranteed in every host.

## Check and create

1. Inspect available goal tools. The supported interface in some Codex hosts is `get_goal({})`, `create_goal({objective})`, and `update_goal({status})`. When the host exposes `functions.exec`, it can call `tools.*`; `functions` is not a shell executable.
2. Read with `get_goal` when available. Reuse an unfinished goal for the same task after checking it, rather than creating a duplicate. If it still reports blocked but the user explicitly requested resumption, continue executable work and record that the conversation resumed while the host goal remains blocked; do not claim it is active. Restart the blocker audit as required by the tool's user-resumption rules, and never invent a resume API. Without a resumption request, do not resume on your own. If the old goal covers only a stage or conflicts with the user's latest contract, record the difference and use the complete contract in `STATE` for authorized work. Without a supported editing API, do not falsely complete the old goal to replace it. Never overwrite another unfinished goal. Ask for a specific user or host action only when needed to resolve a conflict. Do not bypass a user pause or budget and usage limits.
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

## Unavailable or restricted

Distinguish a disabled feature, tools not exposed, a failed call, a goal conflict, and a user pause. Documentation describing a feature does not establish that this conversation can call it.

If Codex CLI is installed and the feature might be disabled, check `codex --version` and `codex features list`. Only when this version supports `goals`, it is disabled, ordinary feature enablement is authorized for this task, and the host permits it, run `codex features enable goals`. Preserve other settings and verify again. A true flag does not guarantee that a running conversation gains tools. Do not restart or interrupt the user's work to test this.

If there is no supported goal interface for the current conversation, or it remains unusable after a normal repair targeted at the known cause, record that persistent goal startup is unavailable, the checks and error evidence, any repair, and the fallback execution mode in `STATE`. Briefly explain the limitation to the user. Continue currently executable work under applicable AGENTS.md and host instructions while retaining the complete state and recovery entry point. Do not claim goal mode is active or promise execution after the application closes.

Never fabricate startup by changing internal Codex databases or transcripts, injecting commands into an input field, or creating scheduled tasks. A user pause or budget limit is not a technical failure and must not be bypassed through fallback execution.

## Complete or blocked

Only perform the supported completion operation and read back its result when the overall outcome and every necessary acceptance condition are satisfied. Finishing a stage, writing a document, passing one test, or making a local commit is not overall completion.

Use `update_goal` only for states allowed by its current contract. Obey its actual-blocker definition, consecutive-turn threshold, budget constraints, and user-resumption rules. Record an initial local blocker and continue independent work instead of marking the whole goal blocked early. When its overall blocker conditions are met, report them truthfully. Do not manufacture empty turns to reach a threshold or falsely report complete just to stop.

## Interface references

Goal availability depends on the version, host, and current conversation. Installing this skill does not make missing tools available; check the runtime each time.

- [Official skill and explicit-invocation configuration](https://learn.chatgpt.com/docs/build-skills)
- [Official persistent goal guide](https://learn.chatgpt.com/use-cases/follow-goals)

A skill contains instructions and resources loaded on demand. It is not a background process; the supporting host owns persistent scheduling.
