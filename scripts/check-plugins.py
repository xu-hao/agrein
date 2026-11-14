"""Read-only native validation of the checkout and an exact disposable payload."""

import json
from pathlib import Path
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SKILL_COUNT = 2


def run(*command):
    print("$ " + " ".join(map(str, command)), flush=True)
    result = subprocess.run(
        command, cwd=ROOT, text=True, capture_output=True, timeout=60
    )
    print(result.stdout, flush=True)
    if result.stderr:
        print(result.stderr, flush=True)
    result.check_returncode()
    return result.stdout


def validate_agy(path, *, strict=False):
    flags = ("--strict", "--json") if strict else ("--json",)
    report = json.loads(run("agy", "plugin", "validate", str(path), *flags))
    # Fail closed even if a client returns exit zero with error findings.
    forbidden = {"error", "warning"} if strict else {"error"}
    findings = report["findings"]
    if any(finding["severity"] in forbidden for finding in findings):
        raise ValueError(f"Antigravity reported rejected findings for {path}")
    count = report["components"]["skills"]
    if type(count) is not int or count != SKILL_COUNT:
        raise ValueError(f"Expected {SKILL_COUNT} skills in {path}, got {count!r}")


def main():
    run("claude", "plugin", "validate", str(ROOT), "--strict")
    validate_agy(ROOT)

    # The checkout includes portable metadata and contributor instructions that
    # Antigravity intentionally ignores. Check its exact host payload strictly.
    # Copy only these directories: CLAUDE.md -> AGENTS.md stays untouched in the
    # checkout and is never copied as a dangling symlink into the host payload.
    with tempfile.TemporaryDirectory(prefix=f"{ROOT.name}-native-plugin-") as directory:
        payload = Path(directory)
        shutil.copytree(ROOT / ".antigravity-plugin", payload / ".antigravity-plugin")
        shutil.copytree(ROOT / "skills", payload / "skills")
        validate_agy(payload, strict=True)
    print("Verified Claude manifests and Antigravity checkout/exact payload; no installs")


if __name__ == "__main__":
    main()
