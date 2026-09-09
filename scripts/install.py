"""Install one language as a single discoverable Codex skill (standard library only)."""

import argparse
import os
from pathlib import Path
import shutil

NAME = "large-task-orchestrator"
ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ("en", "zh-CN")


def package_files(language):
    if language not in LANGUAGES:
        raise ValueError(f"Unsupported language: {language}")
    suffix = "" if language == "en" else ".zh-CN"
    return {
        f"SKILL{suffix}.md": "SKILL.md",
        f"agents/openai{suffix}.yaml": "agents/openai.yaml",
        f"references/persistent-goals{suffix}.md": f"references/persistent-goals{suffix}.md",
        f"assets/current-task-template{suffix}.md": f"assets/current-task-template{suffix}.md",
        "LICENSE": "LICENSE",
    }


def default_destination():
    codex_root = os.environ.get("CODEX_HOME")
    return (Path(codex_root).expanduser() if codex_root else Path.home() / ".codex") / "skills" / NAME


def install(destination, language="en"):
    destination = Path(destination).expanduser()
    # Refuse existing directories, files, and dangling symlinks; do not overwrite an installation.
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f"Destination already exists; inspect or back it up first: {destination}")
    mapping = package_files(language)
    for source in mapping:
        if not (ROOT / source).is_file():
            raise FileNotFoundError(f"Missing package file: {source}")
    destination.mkdir(parents=True, exist_ok=False)
    for source, target in mapping.items():
        output = destination / target
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / source, output)
    return destination.resolve()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--language", choices=LANGUAGES, default="en")
    parser.add_argument("--dest", type=Path, default=None, help="Full destination skill directory")
    args = parser.parse_args()
    try:
        result = install(args.dest if args.dest is not None else default_destination(), args.language)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Install failed: {exc}\n")
    print(f"Installed {NAME} ({args.language}) at {result}")
    print(f"Invoke explicitly with ${NAME}.")


if __name__ == "__main__":
    main()
