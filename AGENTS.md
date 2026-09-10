# Repository guidance / 仓库约定

在本地工作区中，若上级 `../AGENTS.md` 存在，先读取适用约定；它不是本开源包的安装依赖。

- Keep the English and Chinese skill, goal reference, template, and README semantically aligned. 更新时同步中英文的实质行为。
- Preserve explicit-only invocation and existing authorization boundaries. 保留仅显式调用及原有授权边界。
- Runtime installation contains only the selected language's skill, UI metadata, reference, and template. 不把开发资料或运行状态安装到技能目录。
- Validate with `python -m unittest discover -s tests -v` and `python scripts/validate.py`. 按改动需要验证行为；结构检查不等于行为保证。
- For substantive recovery changes, compare against the preceding version on the same isolated cases and report gains, ties, regressions, and limits. A single-version review is not proof of improvement. 恢复规则实质变更须做同案旧新版对照，按证据修改，不把单版本正确推演写成效果提升。
- Append relevant changes and validation to root `WORKLOG.md`. 私人路径、凭据和运行明细不入库。
