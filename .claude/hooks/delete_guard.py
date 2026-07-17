# -*- coding: utf-8 -*-
# delete-guard:
# PreToolUse hook on Bash|PowerShell. Asks for confirmation on delete
# commands (File Operations Discipline, CLAUDE.md: never delete without
# explicit confirmation; archive/ instead of unlink). Plain rmdir without
# /s stays allowed (safe for empty directories - it fails on content).
# Fail-open: any error => no output => the tool runs normally.
import json
import re
import sys

PATTERNS = [
    r"(^|[;&|]\s*)rm\s",
    r"\brm\s+-\w*[rf]",
    r"\brm\s+--(force|recursive)",
    r"\bRemove-Item\b",
    r"\brmdir\s+/s",
    r"\bdel\s+/[fqs]",
    r"shutil\.rmtree",
    r"\bos\.(remove|unlink|rmdir)\s*\(",
    r"\.unlink\s*\(",
]


def main():
    try:
        data = json.load(sys.stdin)
        cmd = (data.get("tool_input") or {}).get("command") or ""
        if any(re.search(p, cmd, re.IGNORECASE) for p in PATTERNS):
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "ask",
                    "permissionDecisionReason": (
                        "Delete command detected. File Operations Discipline "
                        "(CLAUDE.md): deletion only with explicit OK and a "
                        "recovery path (archive/ instead of unlink)."
                    ),
                }
            }))
    except Exception:
        pass


if __name__ == "__main__":
    main()
