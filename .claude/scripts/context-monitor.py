#!/usr/bin/env python3
"""
Claude Code Context Monitor

Real-time context usage monitoring with visual indicators and session analytics.
Displays a status line showing model, directory, context usage, cost, and duration.

Usage:
    Configure in settings.json:
    {
        "statusLine": {
            "type": "command",
            "command": "python3 .claude/scripts/context-monitor.py"
        }
    }

Credit: Adapted from github.com/davila7/claude-code-templates
"""

import json
import os
import re
import sys

CONTEXT_WINDOW_SIZE = 200_000


def parse_context_from_transcript(transcript_path: str) -> dict | None:
    """Parse context usage from Claude Code transcript file."""
    if not transcript_path or not os.path.exists(transcript_path):
        return None

    try:
        with open(transcript_path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()

        recent_lines = lines[-15:] if len(lines) > 15 else lines

        for line in reversed(recent_lines):
            try:
                data = json.loads(line.strip())

                if data.get("type") == "assistant":
                    usage = data.get("message", {}).get("usage", {})
                    if usage:
                        total_tokens = (
                            usage.get("input_tokens", 0)
                            + usage.get("cache_read_input_tokens", 0)
                            + usage.get("cache_creation_input_tokens", 0)
                        )
                        if total_tokens > 0:
                            return {
                                "percent": min(
                                    100, (total_tokens / CONTEXT_WINDOW_SIZE) * 100
                                ),
                                "tokens": total_tokens,
                            }

                elif data.get("type") == "system_message":
                    content = data.get("content", "")

                    match = re.search(r"Context left until auto-compact: (\d+)%", content)
                    if match:
                        return {
                            "percent": 100 - int(match.group(1)),
                            "warning": "auto-compact",
                        }

                    match = re.search(r"Context low \((\d+)% remaining\)", content)
                    if match:
                        return {
                            "percent": 100 - int(match.group(1)),
                            "warning": "low",
                        }

            except (json.JSONDecodeError, KeyError, ValueError):
                continue

        return None

    except (FileNotFoundError, PermissionError):
        return None


def format_context_display(context_info: dict | None) -> str:
    """Generate context display with visual progress bar and color indicators."""
    if not context_info:
        return "\033[34m???\033[0m"

    percent = context_info.get("percent", 0)
    warning = context_info.get("warning")

    # Color thresholds
    if percent >= 95:
        icon, color, alert = "\033[31;1m", "\033[31;1m", "CRIT"
    elif percent >= 90:
        icon, color, alert = "\033[31m", "\033[31m", "HIGH"
    elif percent >= 75:
        icon, color, alert = "\033[33m", "\033[33m", ""
    elif percent >= 50:
        icon, color, alert = "\033[33m", "\033[33m", ""
    else:
        icon, color, alert = "\033[32m", "\033[32m", ""

    # Progress bar
    segments = 8
    filled = int((percent / 100) * segments)
    bar = "\u2588" * filled + "\u2581" * (segments - filled)

    if warning == "auto-compact":
        alert = "COMPACT!"
    elif warning == "low":
        alert = "LOW!"

    reset = "\033[0m"
    alert_str = f" {alert}" if alert else ""

    return f"{color}{bar}{reset} {percent:.0f}%{alert_str}"


def format_directory(workspace: dict) -> str:
    """Get short directory display name."""
    current_dir = workspace.get("current_dir", "")
    project_dir = workspace.get("project_dir", "")

    if current_dir and project_dir:
        if current_dir.startswith(project_dir):
            rel_path = current_dir[len(project_dir) :].lstrip("/")
            return rel_path or os.path.basename(project_dir)
        return os.path.basename(current_dir)

    return os.path.basename(project_dir or current_dir or os.getcwd())


def format_session_metrics(cost_data: dict) -> str:
    """Format session cost, duration, and lines changed."""
    if not cost_data:
        return ""

    metrics = []
    reset = "\033[0m"

    # Cost
    cost_usd = cost_data.get("total_cost_usd", 0)
    if cost_usd > 0:
        if cost_usd >= 0.10:
            color = "\033[31m"
        elif cost_usd >= 0.05:
            color = "\033[33m"
        else:
            color = "\033[32m"

        cost_str = f"{cost_usd * 100:.0f}c" if cost_usd < 0.10 else f"${cost_usd:.2f}"
        metrics.append(f"{color}{cost_str}{reset}")

    # Duration
    duration_ms = cost_data.get("total_duration_ms", 0)
    if duration_ms > 0:
        minutes = duration_ms / 60_000
        color = "\033[33m" if minutes >= 30 else "\033[32m"
        duration_str = f"{duration_ms // 1000}s" if minutes < 1 else f"{minutes:.0f}m"
        metrics.append(f"{color}{duration_str}{reset}")

    # Lines changed
    lines_added = cost_data.get("total_lines_added", 0)
    lines_removed = cost_data.get("total_lines_removed", 0)
    if lines_added > 0 or lines_removed > 0:
        net = lines_added - lines_removed
        if net > 0:
            color = "\033[32m"
        elif net < 0:
            color = "\033[31m"
        else:
            color = "\033[33m"
        sign = "+" if net >= 0 else ""
        metrics.append(f"{color}{sign}{net}L{reset}")

    return f" | {' '.join(metrics)}" if metrics else ""


def main():
    try:
        data = json.load(sys.stdin)

        model_name = data.get("model", {}).get("display_name", "Claude")
        workspace = data.get("workspace", {})
        transcript_path = data.get("transcript_path", "")
        cost_data = data.get("cost", {})

        context_info = parse_context_from_transcript(transcript_path)
        context_display = format_context_display(context_info)
        directory = format_directory(workspace)
        metrics = format_session_metrics(cost_data)

        # Model color based on context usage
        if context_info:
            percent = context_info.get("percent", 0)
            if percent >= 90:
                model_color = "\033[31m"
            elif percent >= 75:
                model_color = "\033[33m"
            else:
                model_color = "\033[32m"
        else:
            model_color = "\033[34m"

        reset = "\033[0m"
        dim = "\033[90m"

        print(
            f"{model_color}{model_name}{reset} "
            f"{dim}{directory}{reset} "
            f"{context_display}"
            f"{metrics}"
        )

    except Exception as e:
        cwd = os.path.basename(os.getcwd())
        print(f"\033[34mClaude\033[0m \033[90m{cwd}\033[0m \033[31m[{e!s:.20}]\033[0m")


if __name__ == "__main__":
    main()
