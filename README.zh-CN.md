# 大型任务编排

[English](README.md) | [简体中文](README.zh-CN.md) · [MIT 许可证](LICENSE)

一个**仅显式调用的 Codex Skill**：把复杂需求整理为完整任务定义、可验证的验收标准、执行计划和可恢复的任务状态。当前宿主支持持久目标时，自动创建目标并开始执行，无需再次要求“继续”。

你描述最终需求，回答确实需要你决定的问题。Codex 负责调查项目、填写任务文档，并推进已授权的实施与验证。

```mermaid
flowchart LR
    A[主动调用] --> B[调查项目与上下文]
    B --> C[解决必要决策]
    C --> D[建立目标、验收和状态]
    D --> E[条件允许时启动持久目标]
    E --> F[实施、验证和修复]
    F --> G[逐项复核验收]
    G -->|未满足| F
    G -->|全部满足| H[完成并汇报]
```

## 能做什么

- 先调查已有上下文、实现、测试、配置和项目约定，再判断是否需要提问。
- 只询问影响最终结果、且无法通过调查或合理工程判断解决的问题。
- 优先复用项目既有状态文档，维护一个固定的当前任务入口。
- 记录验收证据、决定、假设、进度、剩余工作和阻塞。
- 当前环境支持时建立或复用持久目标，并读回工具结果；不会把配置开关或文字命令当作启动证据。
- 目标工具不可用时明确说明限制，保留完整状态并继续可执行工作。
- 尊重“仅分析”、暂停、运行时限制、既有决定及操作授权边界。

本技能配合适用的 `AGENTS.md` 使用，无需作者的私人配置或项目文件。调用不会额外授予生产修改、费用、删除或对外发送权限。

## 安装

要求：支持本地 Skill 的 Codex 宿主、用于克隆仓库的 Git，以及用于安装器的 Python 3.10+。技能本身由指令与资源组成，运行时不因本技能而依赖 Python 或第三方包。

```shell
git clone https://github.com/2770578984-ai/large-task-orchestrator.git
cd large-task-orchestrator
python scripts/install.py --language zh-CN
```

如果需要英文指令和英文显示名称 **Large Task Orchestrator**：

```shell
python scripts/install.py --language en
```

设置了 `CODEX_HOME` 时，默认安装到 `$CODEX_HOME/skills/large-task-orchestrator`；否则使用 `~/.codex/skills/large-task-orchestrator`。安装器只复制所选语言的 Skill、界面元数据、目标参考、任务模板和许可证；目标路径已存在时拒绝覆盖。

如需安装到 Codex 文档列出的用户技能目录，或其他指定位置：

```shell
python scripts/install.py --language zh-CN --dest /absolute/path/to/.agents/skills/large-task-orchestrator
```

Windows 可向 `--dest` 传入完整路径，例如 `C:/path/to/.agents/skills/large-task-orchestrator`。更新或切换语言前，先检查并备份已有安装；同名技能仅保留一份。Codex 通常自动发现变化，选择器未刷新时可重新打开应用。参见[官方 Skill 文档](https://learn.chatgpt.com/docs/build-skills)。

## 使用

在 Codex 中选择技能，或主动输入：

```text
$large-task-orchestrator
把这个服务迁移到新的存储适配器，保持公开 API 行为兼容。
先调查已有实现和测试，建立验收标准，然后完成迁移及必要验证。
```

主动调用即明确请求：任务具备执行条件后自动创建并启动持久目标，无需另输目标命令。如果说明“先只分析和制定方案，不要开始实施”，则只处理该范围。

两个语言版本使用相同内部名称。`SKILL.md` 是英文入口，`SKILL.zh-CN.md` 是中文源文件；安装器将所选版本放到规范要求的 `SKILL.md` 文件名下，不会安装两份相互竞争的同名技能，也不会同时加载两种语言。

运行时策略为：

```yaml
policy:
  allow_implicit_invocation: false
```

普通复杂任务不会自动触发本技能。仅阅读或审查技能也不视为调用。

## 任务状态与恢复

优先复用已有任务状态专题。没有既定入口时，中文任务在项目中创建固定的 `当前大型任务.md`，英文任务可使用 `CURRENT_TASK.md`。状态包含背景、最终目标、当前事实、需求、范围排除、约束、已确认决定、假设、验收、计划、进度、已完成与剩余事项、阻塞和验证结果。

任务状态保存在工作项目中，不写入技能安装目录。恢复时核对已记录决定、实际文件和运行证据；旧完成标记的证据失效时，会重新检查和修正。

## 持久目标与能力限制

部分 Codex 宿主暴露 `get_goal`、`create_goal` 和 `update_goal`。技能读取当前工具契约，在显式调用上下文中建立目标，并读回真实状态；不会虚构接口或自行设置预算。已有未完成目标、暂停与用量限制仍受保护。

安装 Skill 无法提供宿主本来没有的工具。目标机制不可用时，记录并说明限制，保留任务契约，按宿主与项目指令继续可执行工作。Skill 不是后台服务，也不保证关闭应用后仍持续运行。参见[持久目标说明](https://learn.chatgpt.com/use-cases/follow-goals)。

## 仓库内容与验证

| 英文 | 中文 | 用途 |
| --- | --- | --- |
| [SKILL.md](SKILL.md) | [SKILL.zh-CN.md](SKILL.zh-CN.md) | 工作流指令 |
| [Goal integration](references/persistent-goals.md) | [目标接入](references/persistent-goals.zh-CN.md) | 目标工具与降级处理 |
| [Task template](assets/current-task-template.md) | [任务模板](assets/current-task-template.zh-CN.md) | 可恢复任务状态 |
| [UI metadata](agents/openai.yaml) | [界面元数据](agents/openai.zh-CN.yaml) | 显示名称与调用策略 |

维护者检查命令：

```shell
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python scripts/validate.py
```

包检查覆盖两种语言安装、单一可发现入口、资源引用、已有文件防覆盖及调用元数据。它们不能证明模型行为或翻译语义等价，仍需审查和隔离行为验证。

原始中文版已实测显式与普通请求、仅方案范围、状态恢复、目标工具受限，以及持久目标从创建到完成的真实流程。两组实现样例分别通过 16 和 7 项业务测试；这 **23 项是样例测试，不是 23 种独立 Skill 场景**。这些检查没有证明数小时连续运行、强制上下文压缩或关闭应用后的调度。仓库不包含私人对话原始记录。

## 贡献与许可证

修改时保持两种语言的行为一致，保留仅显式调用、证据验收及授权边界。可以通过 GitHub 提交可复现的问题或范围明确的改进，并在 [WORKLOG.md](WORKLOG.md) 记录修改及验证。

使用 [MIT 许可证](LICENSE) 开源。
