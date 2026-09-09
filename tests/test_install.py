import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from install import default_destination, install, NAME, package_files


class InstallTests(unittest.TestCase):
    def test_both_languages_install_one_runtime_entry_and_resolvable_resources(self):
        import re
        for language in ("en", "zh-CN"):
            with self.subTest(language=language), tempfile.TemporaryDirectory() as directory:
                target = Path(directory) / NAME
                install(target, language)
                self.assertEqual(len(list(target.rglob("SKILL.md"))), 1)
                content = (target / "SKILL.md").read_text(encoding="utf-8")
                for link in re.findall(r"\]\(([^)]+)\)", content):
                    self.assertTrue((target / link).is_file(), link)
                self.assertIn("allow_implicit_invocation: false", (target / "agents/openai.yaml").read_text(encoding="utf-8"))
                self.assertEqual(set(str(p.relative_to(target)).replace("\\", "/") for p in target.rglob("*") if p.is_file()), set(package_files(language).values()))

    def test_existing_installation_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / NAME
            target.mkdir()
            marker = target / "user-change.txt"
            marker.write_text("keep me", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                install(target)
            self.assertEqual(marker.read_text(encoding="utf-8"), "keep me")
            self.assertFalse((target / "SKILL.md").exists())

    def test_invalid_language_does_not_create_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / NAME
            with self.assertRaises(ValueError):
                install(target, "unsupported")
            self.assertFalse(target.exists())

    def test_codex_home_is_respected(self):
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {"CODEX_HOME": directory}):
            self.assertEqual(default_destination(), Path(directory) / "skills" / NAME)

    def test_empty_codex_home_uses_user_default(self):
        with patch.dict(os.environ, {"CODEX_HOME": ""}):
            self.assertEqual(default_destination(), Path.home() / ".codex/skills" / NAME)


if __name__ == "__main__":
    unittest.main()
