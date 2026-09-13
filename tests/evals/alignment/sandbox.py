"""Local evaluation I/O: record communications and real fixture-file operations.

Read one JSON request from stdin. This is an observation aid, not a security sandbox
or a native goal host. Each actor owns separate case directories.
"""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys


def perform(case, request):
    op = request["op"]
    project = (case / "project").resolve()
    if op == "list":
        return {"files": sorted(p.relative_to(project).as_posix()
                                for p in project.rglob("*") if p.is_file())}
    if op == "say":
        return {"message": request["text"]}
    if op == "check_config":
        config = json.loads((project / "config.json").read_text(encoding="utf-8"))
        result = {"valid_json": True, "config": config}
        if "expected" in request:
            result["matches_expected"] = config == request["expected"]
        return result
    if op not in ("read", "write"):
        raise ValueError("Supported operations: list, read, say, write, check_config")
    path = (project / request["path"]).resolve()
    if not path.is_relative_to(project) or path == project:
        raise ValueError("Path must stay inside this case project")
    if op == "read":
        return {"content": path.read_text(encoding="utf-8")}
    before = path.read_text(encoding="utf-8") if path.exists() else None
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(request["content"], encoding="utf-8")
    return {"before": before, "after": path.read_text(encoding="utf-8")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-dir", required=True, type=Path)
    args = parser.parse_args()
    case = args.case_dir.resolve()
    if not (case / "project").is_dir():
        parser.error("Expected an existing isolated project directory")
    request = json.load(sys.stdin)
    event = {"time": datetime.now(timezone.utc).isoformat(), "request": request}
    try:
        event["result"] = perform(case, request)
    except (OSError, KeyError, ValueError) as exc:
        event["error"] = str(exc)
    with (case / "events.jsonl").open("a", encoding="utf-8") as trace:
        trace.write(json.dumps(event, ensure_ascii=False) + "\n")
    print(json.dumps(event, ensure_ascii=False))
    return int("error" in event)


if __name__ == "__main__":
    sys.exit(main())
