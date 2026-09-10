"""Prepare blind, isolated skill recovery runs and export evidence for judging.

This does not launch agents, call native goals, or grade natural language.
Keep output outside Git; the private manifest contains local paths and labels.
"""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import random
import shutil
import subprocess

import recovery_host as host


PACKAGE = {
    "SKILL.zh-CN.md": "SKILL.md",
    "references/persistent-goals.zh-CN.md": "references/persistent-goals.zh-CN.md",
    "assets/current-task-template.zh-CN.md": "assets/current-task-template.zh-CN.md",
    "agents/openai.zh-CN.yaml": "agents/openai.yaml",
}


def snapshot(repo, revision, destination):
    hashes = {}
    for source, target in PACKAGE.items():
        data = subprocess.run(["git", "show", f"{revision}:{source}"], cwd=repo, check=True, capture_output=True).stdout
        path = destination / target
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        hashes[target] = host.digest(path)
    return hashes


def prepare(repo, output, design, old_ref, new_ref, fixed_order=False):
    output.mkdir(parents=True, exist_ok=False)
    control = output / ".control"
    control.mkdir()
    cases = host.read_json(design / "cases.json")
    for name in ("cases.json", "rubric.json", "design.md"):
        shutil.copyfile(design / name, control / name)
    simulator = output / "recovery_host.py"
    shutil.copyfile(Path(__file__).with_name("recovery_host.py"), simulator)
    manifest = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "design_sha256": {name: host.digest(control / name) for name in ("cases.json", "rubric.json", "design.md")},
        "host_sha256": host.digest(simulator),
        "protocol": {"repeats": 2, "cases_per_actor": len(cases), "actors": 4, "model": "inherited from parent; no override", "reasoning": "inherited; no override", "sampling": "host default; exact parameters not exposed", "agent_history": "fresh fork_turns=none per actor; case context shared within an actor", "timeout": "15 minutes per actor, interruption recorded as invalid; no selective retries", "retries": "only infrastructure invalidity reruns the affected old/new pair; preset tool errors are valid results", "skill_language": "zh-CN", "scheduler": "local simulator only; no automatic subsequent turns"},
        "runs": [],
    }
    for index, (repeat, arm, revision) in enumerate([(1, "baseline", old_ref), (1, "candidate", new_ref), (2, "candidate", new_ref), (2, "baseline", old_ref)], 1):
        run_id = f"R{index:02d}"
        run_root = output / run_id
        package_hashes = snapshot(repo, revision, run_root / "skill")
        ordered = list(cases)
        if fixed_order:
            if repeat == 2:
                ordered.reverse()
        else:
            random.Random(20260909 + repeat).shuffle(ordered)
        run = {"run_id": run_id, "repeat": repeat, "arm": arm, "revision": revision, "package_sha256": package_hashes, "cases": []}
        for case in ordered:
            case_root = host.initialize(run_root / f"{run_id}-{case['id']}", case)
            initial = {str(path.relative_to(case_root)).replace("\\", "/"): host.digest(path) for path in case_root.rglob("*") if path.is_file()}
            run["cases"].append({"case_id": case["id"], "path": str(case_root), "initial_hashes": initial})
        manifest["runs"].append(run)
    host.write_json(control / "manifest.json", manifest)
    return manifest


def normalized(text, output, case_root):
    # No skill content or version labels are included in judge evidence.
    for path, label in ((case_root, "<CASE>"), (output, "<RUN_ROOT>")):
        for spelling in (str(path), str(path).replace("\\", "/")):
            text = text.replace(spelling, label)
    return text


def read_events(path):
    events, errors = [], []
    if path.exists():
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            try:
                events.append(json.loads(line))
            except ValueError:
                errors.append({"line": number, "error": "malformed audit record"})
    return events, errors


def export(output, run_ids):
    manifest = host.read_json(output / ".control/manifest.json")
    if host.digest(output / "recovery_host.py") != manifest["host_sha256"]:
        raise ValueError("The frozen simulator changed")
    evidence = []
    for run in manifest["runs"]:
        if run["run_id"] not in run_ids:
            continue
        for relative, sha in run["package_sha256"].items():
            if host.digest(output / run["run_id"] / "skill" / relative) != sha:
                raise ValueError("The skill snapshot changed")
        for case in run["cases"]:
            root = Path(case["path"])
            events_path = root / ".host/events.jsonl"
            events, audit_errors = read_events(events_path)
            artifacts = {str(path.relative_to(root)).replace("\\", "/"): host.read_json(path) for path in (root / "work").glob("*.json")} if (root / "work").exists() else {}
            unchanged = {name: host.digest(root / name) == sha for name, sha in case["initial_hashes"].items() if name in ("source.json", ".host/spec.json")}
            prepared = root / "work/prepared.json"
            verified = root / "work/verification.json"
            source_sha = host.digest(root / "source.json")
            prep = artifacts.get("work/prepared.json", {})
            receipt = artifacts.get("work/verification.json", {})
            valid_prepared = prepared.exists() and prep.get("run_id") == root.name and prep.get("source_sha256") == source_sha and prep.get("records") == host.read_json(root / "source.json")["records"]
            valid_verified = bool(verified.exists() and valid_prepared and receipt.get("run_id") == root.name and receipt.get("passed") is True and receipt.get("prepared_sha256") == host.digest(prepared) and receipt.get("source_sha256") == source_sha and receipt.get("final_human_acceptance") is False)
            item = {
                "run_id": root.name, "case_id": case["case_id"], "events": events, "audit_errors": audit_errors, "audit_parse_valid": not audit_errors,
                "final_state": host.read_json(root / ".host/state.json"), "artifacts": artifacts,
                "integrity": {"inputs_unchanged": unchanged, "valid_prepared": valid_prepared, "valid_verified": valid_verified, "initial_prepared_unchanged": host.digest(prepared) == case["initial_hashes"].get("work/prepared.json") if "work/prepared.json" in case["initial_hashes"] and prepared.exists() else None, "event_sequence_contiguous": [e["sequence"] for e in events] == list(range(1, len(events) + 1))},
                "state_document": normalized((root / "CURRENT_TASK.md").read_text(encoding="utf-8"), output, root),
                "reply": normalized((root / "reply.md").read_text(encoding="utf-8"), output, root) if (root / "reply.md").exists() else "[MISSING]",
            }
            evidence.append(item)
    random.Random(20260910).shuffle(evidence)
    judge = output / "judge"
    judge.mkdir(exist_ok=True)
    for name in ("cases.json", "rubric.json"):
        shutil.copyfile(output / ".control" / name, judge / name)
    target = judge / ("evidence-" + "-".join(run_ids) + ".json")
    host.write_json(target, evidence)
    return target


def without_read_time(value):
    if isinstance(value, dict):
        return {key: without_read_time(item) for key, item in value.items() if key != "read_at"}
    if isinstance(value, list):
        return [without_read_time(item) for item in value]
    return value


def replay(output, destination, run_ids):
    """Re-execute recorded operations; this is not another model evaluation.

    A mismatch invalidates semantic equivalence and requires paired actor reruns.
    Only read timestamps and private audit counters may differ. Never rewrite
    the original evidence, actor replies, or grades.
    """
    manifest = host.read_json(output / ".control/manifest.json")
    destination.mkdir(parents=True, exist_ok=False)
    rows = []
    for run in manifest["runs"]:
        if run["run_id"] not in run_ids:
            continue
        for entry in run["cases"]:
            original = Path(entry["path"])
            case = host.read_json(original / ".host/spec.json")
            target = host.initialize(destination / original.name, case)
            events, audit_errors = read_events(original / ".host/events.jsonl")
            mismatches = list(audit_errors)
            for index, event in enumerate(events, 1):
                before = host.read_json(target / ".host/state.json")["status"]
                result = host.dispatch(target, event["operation"], event["value"])
                after = host.read_json(target / ".host/state.json")["status"]
                if without_read_time(result) != without_read_time(event["result"]) or before != event["goal_before"] or after != event["goal_after"]:
                    mismatches.append({"event_index": index, "operation": event["operation"], "original_result": event["result"], "replay_result": result})
            for name in ("source.json", "work/prepared.json", "work/verification.json"):
                left, right = original / name, target / name
                if left.exists() != right.exists() or (left.exists() and left.read_bytes() != right.read_bytes()):
                    mismatches.append({"artifact": name, "error": "content differs"})
            left = host.read_json(original / ".host/state.json")
            right = host.read_json(target / ".host/state.json")
            for key in ("goal_id", "status", "prepared", "verified", "source_sha256"):
                if left[key] != right[key]:
                    mismatches.append({"state_field": key, "original": left[key], "replay": right[key]})
            rows.append({"run_id": original.name, "semantic_equivalent": not mismatches, "mismatches": mismatches, "event_count": len(events), "original_audit_contiguous": [event["sequence"] for event in events] == list(range(1, len(events) + 1)), "replay_sequence": right["sequence"], "replay_get_count": right["get_count"], "expected_get_count": sum(event["operation"] == "get_goal" for event in events)})
    report = {"method": "deterministic operation replay, not an independent model repeat", "host_sha256": host.digest(Path(host.__file__)), "results": rows}
    host.write_json(destination / "replay-report.json", report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="operation", required=True)
    setup = commands.add_parser("prepare")
    setup.add_argument("--repo", type=Path, default=Path.cwd())
    setup.add_argument("--output", type=Path, required=True)
    setup.add_argument("--design", type=Path, required=True)
    setup.add_argument("--old-ref", required=True)
    setup.add_argument("--new-ref", required=True)
    setup.add_argument("--fixed-order", action="store_true", help="Use design order in repeat 1 and reverse it in repeat 2 instead of shuffling")
    dump = commands.add_parser("export")
    dump.add_argument("--output", type=Path, required=True)
    dump.add_argument("--run-ids", nargs="+", required=True)
    replay_command = commands.add_parser("replay")
    replay_command.add_argument("--output", type=Path, required=True)
    replay_command.add_argument("--destination", type=Path, required=True)
    replay_command.add_argument("--run-ids", nargs="+", required=True)
    args = parser.parse_args()
    if args.operation == "prepare":
        manifest = prepare(args.repo.resolve(), args.output.resolve(), args.design.resolve(), args.old_ref, args.new_ref, args.fixed_order)
        print("Prepared", len(manifest["runs"]), "blind actor runs")
    elif args.operation == "export":
        print(export(args.output.resolve(), args.run_ids))
    else:
        report = replay(args.output.resolve(), args.destination.resolve(), args.run_ids)
        print(json.dumps({"cases": len(report["results"]), "equivalent": sum(row["semantic_equivalent"] for row in report["results"])}))


if __name__ == "__main__":
    main()
