"""Check package structure, local links, and explicit-invocation policy; not behavior."""

from pathlib import Path
import re
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from install import LANGUAGES, NAME, package_files


def validate(root=ROOT):
    errors = []
    for language in LANGUAGES:
        mapping = package_files(language)
        for source in mapping:
            if not (root / source).is_file():
                errors.append(f"{language}: missing {source}")
        suffix = "" if language == "en" else ".zh-CN"
        skill = root / f"SKILL{suffix}.md"
        if not skill.is_file():
            continue
        content = skill.read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", content, re.S)
        if not match:
            errors.append(f"{language}: missing YAML frontmatter")
            continue
        metadata = yaml.safe_load(match.group(1))
        if not isinstance(metadata, dict) or metadata.get("name") != NAME or not isinstance(metadata.get("description"), str) or not metadata["description"].strip():
            errors.append(f"{language}: invalid skill metadata")
        ui_path = root / f"agents/openai{suffix}.yaml"
        if ui_path.is_file():
            ui = yaml.safe_load(ui_path.read_text(encoding="utf-8"))
            if ui.get("policy", {}).get("allow_implicit_invocation") is not False:
                errors.append(f"{language}: implicit invocation must be disabled")
            interface = ui.get("interface", {})
            if f"${NAME}" not in interface.get("default_prompt", ""):
                errors.append(f"{language}: default prompt must explicitly invoke the skill")
            if not 25 <= len(interface.get("short_description", "")) <= 64:
                errors.append(f"{language}: invalid short description length")
        installed_names = set(mapping.values())
        for target in re.findall(r"\]\(([^)]+)\)", content):
            if not target.startswith(("https://", "http://", "#")) and target not in installed_names:
                errors.append(f"{language}: runtime link is not installed: {target}")
    for document in root.rglob("*.md"):
        if any(part in (".git", ".local") for part in document.relative_to(root).parts):
            continue
        text = document.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)]+)\)", text):
            if target.startswith(("https://", "http://", "#")):
                continue
            path = target.split("#", 1)[0]
            if not (document.parent / path).exists():
                errors.append(f"{document.relative_to(root)}: broken local link {target}")
    return errors


if __name__ == "__main__":
    problems = validate()
    for problem in problems:
        print(problem)
    print("Package validation passed." if not problems else "Package validation failed.")
    raise SystemExit(bool(problems))
