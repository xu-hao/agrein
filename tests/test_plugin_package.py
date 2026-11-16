"""Observable package contracts and native-validator orchestration behavior."""

import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt
import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILLS = {
    "ticket-delivery",
    "epic-queue",
    "bug-investigation",
    "owner-escalation",
}
MANIFESTS = ("plugin.json", ".claude-plugin/plugin.json", ".antigravity-plugin/plugin.json")
SKILL_DOCS = sorted((ROOT / "skills").rglob("*.md"))


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("manifest", MANIFESTS)
def test_manifest_contract(manifest):
    data = load_json(ROOT / manifest)
    assert isinstance(data, dict)
    assert data["name"] == "agrein"
    assert data["version"] == "0.1.0"
    assert re.fullmatch(r"\d+\.\d+\.\d+", data["version"])
    assert isinstance(data["description"], str) and data["description"].strip()
    assert data["author"] == {"name": "agrein contributors"}
    assert data["repository"] == "https://github.com/xu-hao/agrein"
    # All hosts use their default skills/ discovery, with no divergent override.
    assert "skills" not in data
    allowed = {"name", "version", "description", "author", "repository"}
    if manifest == "plugin.json":
        assert data["$schema"] == "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
        allowed.add("$schema")
    elif manifest.startswith(".antigravity-plugin/"):
        assert data["$schema"] == "https://antigravity.google/schemas/v1/plugin.json"
        assert data["displayName"] == "agrein"
        allowed.update(("$schema", "displayName"))
    assert set(data) == allowed


@pytest.mark.parametrize("host", ("codex", "claude", "antigravity"))
def test_host_discovers_identical_shared_skills(host):
    plugin_root = ROOT
    if host in {"codex", "claude"}:
        marketplace_path = (
            ".agents/plugins/marketplace.json" if host == "codex"
            else ".claude-plugin/marketplace.json"
        )
        marketplace = load_json(ROOT / marketplace_path)
        assert marketplace["name"] == "agrein"
        assert len(marketplace["plugins"]) == 1
        entry = marketplace["plugins"][0]
        assert entry["name"] == "agrein"
        if host == "codex":
            assert entry["source"] == {"source": "local", "path": "./"}
            assert entry["policy"] == {
                "installation": "AVAILABLE", "authentication": "ON_INSTALL"
            }
            assert entry["category"] == "Productivity"
            source = entry["source"]["path"]
        else:
            assert marketplace["owner"] == {"name": "agrein contributors"}
            assert isinstance(marketplace["description"], str)
            assert isinstance(entry["description"], str)
            source = entry["source"]
        plugin_root = (ROOT / source).resolve()
    assert plugin_root == ROOT
    discovered = {path.parent.name for path in (plugin_root / "skills").glob("*/SKILL.md")}
    assert discovered == SKILLS
    assert {path.name for path in (plugin_root / "skills").iterdir()} == SKILLS


@pytest.mark.parametrize("skill", sorted(SKILLS))
def test_skill_frontmatter_is_native_yaml(skill):
    text = (ROOT / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
    opening, frontmatter, body = text.split("---", 2)
    assert not opening
    metadata = yaml.safe_load(frontmatter)
    assert isinstance(metadata, dict)
    assert metadata["name"] == skill
    assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", metadata["name"])
    assert isinstance(metadata["description"], str)
    assert 0 < len(metadata["description"].strip()) <= 1024
    assert body.strip()


def relative_targets(document):
    """Parse actual Markdown links, avoiding false positives from code examples."""
    for token in MarkdownIt().parse(document.read_text(encoding="utf-8")):
        for child in token.children or ():
            target = child.attrGet("href") if child.type == "link_open" else None
            if child.type == "image":
                target = child.attrGet("src")
            if target:
                parsed = urlsplit(target)
                if not parsed.scheme and not parsed.netloc and parsed.path:
                    yield (document.parent / unquote(parsed.path)).resolve()


@pytest.mark.parametrize("document", SKILL_DOCS, ids=lambda path: str(path.relative_to(ROOT)))
def test_skill_and_reference_relative_links_resolve(document):
    for target in relative_targets(document):
        assert target.is_relative_to(ROOT), f"Link escapes package: {target}"
        assert target.is_file(), f"Broken link from {document} to {target}"


def test_markdown_link_check_observes_missing_files_and_ignores_code(tmp_path):
    document = tmp_path / "SKILL.md"
    document.write_text("[Missing](references/not%20here.md)\n\n```text\n[x](fake.md)\n```\n")
    targets = list(relative_targets(document))
    assert targets == [tmp_path / "references" / "not here.md"]
    assert not targets[0].exists()


def test_contributor_symlink_resolves_to_canonical_instructions():
    link = ROOT / "CLAUDE.md"
    assert link.is_symlink()
    assert link.readlink() == Path("AGENTS.md")
    assert link.resolve() == ROOT / "AGENTS.md"
    assert link.read_bytes() == (ROOT / "AGENTS.md").read_bytes()


FAKE_CLIENT = '''#!/usr/bin/env python3
import json
import os
from pathlib import Path
import sys

host = Path(sys.argv[0]).name
args = sys.argv[1:]
root = Path(args[2])
strict = "--strict" in args
with open(os.environ["AGREIN_TEST_LOG"], "a") as log:
    log.write(json.dumps({"host": host, "args": args}) + "\\n")
case = os.environ["AGREIN_TEST_CASE"]
if host == "claude":
    assert args == ["plugin", "validate", str(root), "--strict"]
    assert (root / ".claude-plugin" / "marketplace.json").is_file()
    sys.exit(9 if case == "claude-exit" else 0)
assert args[:2] == ["plugin", "validate"]
assert args[-1] == "--json"
if strict:
    assert set(p.name for p in root.iterdir()) == {".antigravity-plugin", "skills"}
    assert (root / ".antigravity-plugin" / "plugin.json").is_file()
    assert {p.parent.name for p in root.glob("skills/*/SKILL.md")} == {
        "ticket-delivery",
        "epic-queue",
        "bug-investigation",
        "owner-escalation",
    }
    if case == "strict-exit":
        sys.exit(8)
elif case == "checkout-exit":
    sys.exit(7)
if case == "invalid-json":
    print("invalid JSON")
    sys.exit(0)
findings = [] if strict else [{"severity": "warning", "message": "ignored contributor file"}]
if case == "checkout-error" and not strict:
    findings = [{"severity": "error", "message": "rejected skill"}]
if case == "strict-warning" and strict:
    findings = [{"severity": "warning", "message": "ignored payload field"}]
if case == "strict-error" and strict:
    findings = [{"severity": "error", "message": "rejected payload"}]
count = 4
if (case == "checkout-count" and not strict) or (case == "strict-count" and strict):
    count = 3
print(json.dumps({"components": {"skills": count}, "findings": findings}))
'''


@pytest.fixture
def native_check(tmp_path):
    # Use a disposable package with the real instruction symlink and script.
    package = tmp_path / "agrein-ticket-test-package"
    package.mkdir()
    for folder in ("skills", ".agents", ".claude-plugin", ".antigravity-plugin", "scripts"):
        shutil.copytree(ROOT / folder, package / folder)
    for file in ("plugin.json", "AGENTS.md"):
        shutil.copy2(ROOT / file, package / file)
    (package / "CLAUDE.md").symlink_to("AGENTS.md")
    binaries = tmp_path / "bin"
    binaries.mkdir()
    for host in ("claude", "agy"):
        binary = binaries / host
        binary.write_text(FAKE_CLIENT)
        binary.chmod(0o755)
    log = tmp_path / "native-calls.jsonl"

    def run(case):
        env = {
            **os.environ,
            "PATH": str(binaries) + os.pathsep + os.environ["PATH"],
            "TMPDIR": str(tmp_path),
            "AGREIN_TEST_LOG": str(log),
            "AGREIN_TEST_CASE": case,
        }
        result = subprocess.run(
            [sys.executable, str(package / "scripts" / "check-plugins.py")],
            cwd=package, env=env, capture_output=True, text=True, timeout=30,
        )
        calls = [json.loads(line) for line in log.read_text().splitlines()]
        # Validation must never rewrite the checkout or leave a temporary payload.
        assert (package / "CLAUDE.md").is_symlink()
        assert (package / "CLAUDE.md").read_bytes() == (ROOT / "AGENTS.md").read_bytes()
        assert not list(tmp_path.glob("agrein-ticket-test-package-native-plugin-*"))
        return result, calls

    return run


def test_native_check_runs_all_hosts_and_cleans_payload(native_check):
    result, calls = native_check("success")
    assert result.returncode == 0, result.stdout + result.stderr
    assert [call["host"] for call in calls] == ["claude", "agy", "agy"]
    assert "--strict" not in calls[1]["args"]
    assert "--strict" in calls[2]["args"]
    assert not Path(calls[2]["args"][2]).exists()


@pytest.mark.parametrize("case,call_count", [
    ("claude-exit", 1), ("checkout-exit", 2), ("checkout-error", 2),
    ("checkout-count", 2), ("invalid-json", 2), ("strict-exit", 3),
    ("strict-warning", 3), ("strict-error", 3), ("strict-count", 3),
])
def test_native_check_rejects_failed_or_inconsistent_validations(native_check, case, call_count):
    result, calls = native_check(case)
    assert result.returncode != 0
    assert len(calls) == call_count
