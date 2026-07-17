# -*- coding: utf-8 -*-
# wiki-ask-guard:
# PreToolUse hook on Write|Edit. Asks for confirmation on writes into
# knowledge/wiki/ ("Do not write casually", CLAUDE.md) - but only once per
# session: after the first wiki write goes through, the PostToolUse run
# (argument "post") drops a session marker into the system temp directory;
# further wiki writes in the same session pass silently.
# A denial sets no marker (PostToolUse only fires on success), so the guard
# asks again on the next attempt.
# Exception: glossary.md (declared retrieval infrastructure, "May write
# carefully" in CLAUDE.md).
# Fail-open: any error => no output => the tool runs normally.
import json
import os
import re
import sys
import tempfile
import time

MARKER_PREFIX = "claude_wiki_guard_"
MARKER_MAX_AGE_S = 7 * 24 * 3600


def is_wiki_path(fp):
    p = (fp or "").replace("\\", "/").lower()
    return "/knowledge/wiki/" in p and not p.endswith("/glossary.md")


def marker_path(session_id):
    sid = re.sub(r"[^A-Za-z0-9_-]", "", session_id or "")
    if not sid:
        return None
    return os.path.join(tempfile.gettempdir(), MARKER_PREFIX + sid)


def cleanup_stale_markers():
    # Housekeeping of this hook's own marker files in the temp dir,
    # never vault content.
    try:
        d = tempfile.gettempdir()
        now = time.time()
        for name in os.listdir(d):
            if name.startswith(MARKER_PREFIX):
                fp = os.path.join(d, name)
                if now - os.path.getmtime(fp) > MARKER_MAX_AGE_S:
                    os.remove(fp)
    except Exception:
        pass


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "pre"
    try:
        data = json.load(sys.stdin)
        fp = (data.get("tool_input") or {}).get("file_path") or ""
        if not is_wiki_path(fp):
            return
        marker = marker_path(data.get("session_id"))

        if mode == "post":
            if marker and not os.path.exists(marker):
                cleanup_stale_markers()
                with open(marker, "w"):
                    pass
            return

        if marker and os.path.exists(marker):
            return
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "ask",
                "permissionDecisionReason": (
                    "knowledge/wiki is 'Do not write casually' (CLAUDE.md). "
                    "Is this an explicit Knowledge Mode operation? Confirm or deny. "
                    "After one approval this session will not ask again."
                ),
            }
        }))
    except Exception:
        pass


if __name__ == "__main__":
    main()
