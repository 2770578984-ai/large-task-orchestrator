import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


EVALS = Path(__file__).parent / "evals"
spec = importlib.util.spec_from_file_location("recovery_host", EVALS / "recovery_host.py")
host = importlib.util.module_from_spec(spec)
spec.loader.exec_module(host)
with patch.dict(sys.modules, {"recovery_host": host}):
    spec = importlib.util.spec_from_file_location("recovery_ab", EVALS / "recovery_ab.py")
    ab = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ab)


class RecoveryEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name) / "run"

        def fake_snapshot(repo, revision, destination):
            destination.mkdir(parents=True)
            skill = destination / "SKILL.md"
            skill.write_text("private package " + revision, encoding="utf-8")
            return {"SKILL.md": host.digest(skill)}

        with patch.object(ab, "snapshot", fake_snapshot):
            self.manifest = ab.prepare(EVALS, self.output, EVALS, "OLD_PRIVATE_REF", "NEW_PRIVATE_REF")

    def test_export_preserves_verified_actions_without_revealing_package(self):
        root = self.output / "R01/R01-C06"
        host.dispatch(root, "work", "verify")
        (root / "reply.md").write_text("本轮回执：" + str(root / "work/verification.json"), encoding="utf-8")
        path = ab.export(self.output, ["R01", "R02"])
        text = path.read_text(encoding="utf-8")
        self.assertNotIn("OLD_PRIVATE_REF", text)
        self.assertNotIn("NEW_PRIVATE_REF", text)
        self.assertNotIn(str(self.output).replace("\\", "\\\\"), text)
        evidence = host.read_json(path)
        self.assertEqual(len(evidence), 16)
        item = next(item for item in evidence if item["run_id"] == "R01-C06")
        self.assertTrue(item["integrity"]["valid_verified"])
        self.assertEqual(item["events"][0]["operation"], "work")
        self.assertEqual(item["final_state"]["status"], "blocked")

    def test_frozen_host_and_skill_tampering_are_rejected(self):
        frozen_host = self.output / "recovery_host.py"
        original = frozen_host.read_bytes()
        frozen_host.write_bytes(original + b"\n# altered\n")
        with self.assertRaisesRegex(ValueError, "simulator changed"):
            ab.export(self.output, ["R01"])
        frozen_host.write_bytes(original)
        (self.output / "R01/skill/SKILL.md").write_text("changed", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "snapshot changed"):
            ab.export(self.output, ["R01"])

    def test_inputs_have_unique_run_ids_and_paired_order(self):
        runs = self.manifest["runs"]
        paths = [case["path"] for run in runs for case in run["cases"]]
        self.assertEqual(len({Path(path).name for path in paths}), 32)
        self.assertEqual([case["case_id"] for case in runs[0]["cases"]], [case["case_id"] for case in runs[1]["cases"]])
        self.assertEqual([case["case_id"] for case in runs[2]["cases"]], [case["case_id"] for case in runs[3]["cases"]])
        for path in paths:
            self.assertFalse((Path(path) / "scenario.json").exists())

    def test_replay_detects_semantic_changes_without_rewriting_originals(self):
        run = self.manifest["runs"][0]
        for case in run["cases"]:
            host.dispatch(Path(case["path"]), "get_goal")
        report = ab.replay(self.output, Path(self.temp.name) / "replay", ["R01"])
        self.assertTrue(all(row["semantic_equivalent"] for row in report["results"]))
        first = Path(run["cases"][0]["path"]) / ".host/events.jsonl"
        event = host.read_json(first)
        event["result"]["goal"]["status"] = "forged"
        host.write_json(first, event)
        # A JSONL record remains a single line, as in a CLI event log.
        first.write_text(ab.json.dumps(event) + "\n", encoding="utf-8")
        original_hash = host.digest(first)
        report = ab.replay(self.output, Path(self.temp.name) / "mismatch", ["R01"])
        self.assertFalse(report["results"][0]["semantic_equivalent"])
        self.assertEqual(host.digest(first), original_hash)

    def test_malformed_audit_is_explicitly_flagged(self):
        root = Path(self.manifest["runs"][0]["cases"][0]["path"])
        host.dispatch(root, "get_goal")
        path = root / ".host/events.jsonl"
        with path.open("a", encoding="utf-8") as stream:
            stream.write("truncated record\n")
        evidence = host.read_json(ab.export(self.output, ["R01"]))
        item = next(item for item in evidence if item["run_id"] == root.name)
        self.assertFalse(item["audit_parse_valid"])
        self.assertEqual(item["audit_errors"][0]["line"], 2)
        self.assertEqual(len(item["events"]), 1)


if __name__ == "__main__":
    unittest.main()
