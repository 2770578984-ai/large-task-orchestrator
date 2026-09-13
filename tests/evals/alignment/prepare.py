"""Materialize paired, isolated alignment cases from two frozen skill packages."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil


def hashes(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*")) if p.is_file()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--package-a", type=Path, required=True)
    parser.add_argument("--package-b", type=Path, required=True)
    args = parser.parse_args()
    design = Path(__file__).resolve().parent
    output = args.output.resolve()
    if output.exists():
        parser.error("Output exists; preserve prior runs and choose a new path")
    cases = json.loads((design / "cases.json").read_text(encoding="utf-8"))["cases"]
    order = ["c03", "c01", "c04", "c02", "c05"]
    if len(cases) != len(order) or {c["id"] for c in cases} != set(order):
        parser.error("Expected the frozen five-case design")
    packages = {"A": args.package_a.resolve(), "B": args.package_b.resolve()}
    for package in packages.values():
        if not (package / "SKILL.md").is_file():
            parser.error("Both packages must contain a runtime SKILL.md")
    output.mkdir(parents=True)
    manifest = {"case_order": order, "packages": {}, "design_hashes": {
        name: hashlib.sha256((design / name).read_bytes()).hexdigest()
        for name in ("cases.json", "rubric.json", "sandbox.py", "prepare.py")}}
    for run_id, package in packages.items():
        actor = output / run_id
        shutil.copytree(package, actor / "skill")
        manifest["packages"][run_id] = {"source": str(package), "hashes": hashes(package)}
        for case in cases:
            folder = actor / case["id"]
            project = folder / "project"
            project.mkdir(parents=True)
            request = {key: case[key] for key in ("id", "user_request", "prior_conversation")}
            (folder / "REQUEST.json").write_text(
                json.dumps(request, ensure_ascii=False, indent=2), encoding="utf-8")
            for relative, content in case["files"].items():
                target = (project / relative).resolve()
                if not target.is_relative_to(project.resolve()):
                    raise ValueError("Fixture path escapes project")
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")
    control = output / ".control"
    control.mkdir()
    (control / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(output), "case_order": order, "actors": ["A", "B"]}))


if __name__ == "__main__":
    main()
