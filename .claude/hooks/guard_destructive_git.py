#!/usr/bin/env python3
"""PreToolUse guard: blocks 'git push --force' (without --force-with-lease)
and 'git reset --hard' before they reach the shell.

Deterministic safety net, not a prompt instruction. Fails open: any parsing
error lets the command through rather than blocking it wrongly.
"""
import json
import re
import shlex
import sys

SPLIT_CHARS = ("&&", "||", ";", "|", "\n")


def strip_heredocs(command: str) -> str:
    """Remove heredoc bodies (<<EOF ... EOF / <<'EOF' ... EOF) so that text
    merely *describing* a blocked command (e.g. inside a commit message)
    doesn't trigger a false positive."""
    lines = command.split("\n")
    out = []
    i = 0
    heredoc_re = re.compile(r"<<-?\s*['\"]?([A-Za-z_][A-Za-z0-9_]*)['\"]?")
    while i < len(lines):
        line = lines[i]
        match = heredoc_re.search(line)
        if match:
            delimiter = match.group(1)
            out.append(line[: match.start()])
            i += 1
            while i < len(lines) and lines[i].strip() != delimiter:
                i += 1
            i += 1  # skip the delimiter line itself
            continue
        out.append(line)
        i += 1
    return "\n".join(out)


def split_segments(command: str):
    """Split a shell command into segments on &&, ||, ;, | and newlines,
    without breaking apart tokens that live inside single/double quotes."""
    segments = []
    current = []
    quote = None
    i = 0
    n = len(command)
    while i < n:
        ch = command[i]

        if quote:
            current.append(ch)
            if ch == quote:
                quote = None
            i += 1
            continue

        if ch in ("'", '"'):
            quote = ch
            current.append(ch)
            i += 1
            continue

        matched_sep = None
        for sep in ("&&", "||"):
            if command.startswith(sep, i):
                matched_sep = sep
                break
        if matched_sep:
            segments.append("".join(current))
            current = []
            i += len(matched_sep)
            continue

        if ch in (";", "|", "\n"):
            segments.append("".join(current))
            current = []
            i += 1
            continue

        current.append(ch)
        i += 1

    segments.append("".join(current))
    return [s.strip() for s in segments if s.strip()]


def is_blocked(segment: str):
    # shlex respects quoting, so a quoted string like -m "... git push
    # --force ..." collapses into a single token instead of being split
    # into separate "git"/"push"/"--force" words.
    tokens = shlex.split(segment, posix=True)
    if not tokens:
        return None

    lower_tokens = [t.lower() for t in tokens]

    # Only treat "git" as the invocation if it's the first real token
    # (allowing leading VAR=value env assignments), not merely present
    # anywhere in the segment (e.g. inside an unrelated quoted argument).
    start = 0
    while start < len(tokens) and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", tokens[start]):
        start += 1

    if start < len(lower_tokens) and lower_tokens[start] == "git":
        rest = lower_tokens[start + 1:]

        if "push" in rest:
            has_force = any(
                t in ("--force", "-f") or t.startswith("--force=") for t in rest
            )
            has_force_with_lease = any(
                t == "--force-with-lease" or t.startswith("--force-with-lease=")
                for t in rest
            )
            if has_force and not has_force_with_lease:
                return "git push --force (without --force-with-lease) is blocked. Use --force-with-lease or ask the user to confirm."

        if "reset" in rest and "--hard" in rest:
            return "git reset --hard is blocked (discards uncommitted work). Ask the user to confirm or use a non-destructive alternative."

    return None


def main():
    try:
        payload = json.load(sys.stdin)
        tool_input = payload.get("tool_input", {})
        command = tool_input.get("command", "")
        if not command:
            return

        cleaned = strip_heredocs(command)
        for segment in split_segments(cleaned):
            reason = is_blocked(segment)
            if reason:
                print(json.dumps({"decision": "block", "reason": reason}))
                return
    except Exception:
        # Fail open: never block due to a parsing error.
        return


if __name__ == "__main__":
    main()
