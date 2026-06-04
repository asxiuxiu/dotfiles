#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rewrite today's (or a given day's) Git commits to natural-looking evening timestamps.
Uses git rebase -i --root with a generated sequence-editor script.
"""

import argparse
import os
import random
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta


def parse_args():
    parser = argparse.ArgumentParser(
        description="Rewrite commit author/committer and timestamps for today's commits."
    )
    parser.add_argument("--author", default="asxiuxiu", help="Author/committer name")
    parser.add_argument(
        "--email", default="licheng1996121@gmail.com", help="Author/committer email"
    )
    parser.add_argument(
        "--date",
        default=None,
        help="Target date (YYYY-MM-DD). Defaults to today.",
    )
    parser.add_argument(
        "--start-time",
        default="18:30",
        help="Earliest time of day (HH:MM). Default: 18:30",
    )
    parser.add_argument(
        "--end-time",
        default="23:59",
        help="Latest time of day (HH:MM). Default: 23:59",
    )
    parser.add_argument(
        "--min-gap",
        type=int,
        default=600,
        help="Minimum gap between commits in seconds (default: 600 = 10 min)",
    )
    return parser.parse_args()


def get_today_commits(target_date: str):
    result = subprocess.run(
        [
            "git",
            "log",
            "--reverse",
            f'--since={target_date} 00:00',
            f'--until={target_date} 23:59:59',
            "--format=%H %s",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    lines = [line.strip() for line in result.stdout.strip().splitlines() if line.strip()]
    commits = []
    for line in lines:
        hash_val, _, msg = line.partition(" ")
        commits.append((hash_val.strip(), msg.strip()))
    return commits


def generate_natural_times(count: int, date_str: str, start_str: str, end_str: str, min_gap: int):
    start_dt = datetime.strptime(f"{date_str} {start_str}:00", "%Y-%m-%d %H:%M:%S")
    # Use 59 seconds for the end bound so we don't roll into the next day unexpectedly
    end_dt = datetime.strptime(f"{date_str} {end_str}:59", "%Y-%m-%d %H:%M:%S")
    if end_dt <= start_dt:
        raise ValueError("end-time must be later than start-time")

    total_seconds = int((end_dt - start_dt).total_seconds())
    times = []
    attempts = 0
    while len(times) < count and attempts < count * 5000:
        attempts += 1
        offset = random.randint(0, total_seconds)
        t = start_dt + timedelta(seconds=offset)
        # Avoid too-regular-looking timestamps (exact 5-minute or 10-minute marks with 0 seconds)
        if t.minute % 5 == 0 and t.second == 0:
            continue
        if t.second == 0:
            continue
        if any(abs((t - existing).total_seconds()) < min_gap for existing in times):
            continue
        times.append(t)

    if len(times) < count:
        raise RuntimeError(
            f"Could not generate {count} distinct times within the window. "
            "Try widening the time range or reducing --min-gap."
        )

    times.sort()
    return times


def build_todo_lines(commits, times, author_name, author_email):
    lines = []
    for (hash_val, msg), t in zip(commits, times):
        date_str = t.strftime("%Y-%m-%d %H:%M:%S %z")
        lines.append(f"pick {hash_val} {msg}")
        lines.append(
            f'exec export GIT_AUTHOR_NAME="{author_name}" GIT_AUTHOR_EMAIL="{author_email}" '
            f'GIT_COMMITTER_NAME="{author_name}" GIT_COMMITTER_EMAIL="{author_email}" '
            f'GIT_AUTHOR_DATE="{date_str}" GIT_COMMITTER_DATE="{date_str}" && '
            f'git commit --amend --no-edit --reset-author --date="{date_str}"'
        )
    return "\n".join(lines) + "\n"


def run_rebase(todo_content: str):
    tmpdir = tempfile.mkdtemp(prefix="git_rewrite_")
    todo_path = os.path.join(tmpdir, "todo.txt")
    editor_path = os.path.join(tmpdir, "editor.py")

    with open(todo_path, "w", encoding="utf-8") as f:
        f.write(todo_content)

    editor_code = (
        "import sys, shutil\n"
        f"shutil.copyfile(r'{todo_path}', sys.argv[1])\n"
    )
    with open(editor_path, "w", encoding="utf-8") as f:
        f.write(editor_code)

    env = os.environ.copy()
    env["GIT_SEQUENCE_EDITOR"] = f'"{sys.executable}" "{editor_path}"'

    print("Starting interactive rebase. This will rewrite commit hashes...")
    try:
        subprocess.run(["git", "rebase", "-i", "--root"], env=env, check=True)
    except subprocess.CalledProcessError as exc:
        print(f"Rebase failed: {exc}")
        sys.exit(1)
    finally:
        try:
            os.remove(todo_path)
            os.remove(editor_path)
            os.rmdir(tmpdir)
        except OSError:
            pass


def main():
    args = parse_args()

    target_date = args.date or datetime.now().strftime("%Y-%m-%d")
    commits = get_today_commits(target_date)
    if not commits:
        print(f"No commits found on {target_date}.")
        sys.exit(0)

    print(f"Found {len(commits)} commit(s) on {target_date}.")
    times = generate_natural_times(
        len(commits),
        target_date,
        args.start_time,
        args.end_time,
        args.min_gap,
    )

    for i, (c, t) in enumerate(zip(commits, times), 1):
        print(f"  {i}. {c[1][:50]}... -> {t.strftime('%H:%M:%S')}")

    todo = build_todo_lines(commits, times, args.author, args.email)
    run_rebase(todo)
    print("Done. Commit hashes have been rewritten.")
    print("If this branch was already pushed, you will need to force-push.")


if __name__ == "__main__":
    main()
