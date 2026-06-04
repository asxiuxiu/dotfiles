---
name: git-rewrite-today-commits
description: Batch-rewrite today's Git commits to shift their author/committer timestamps into a natural-looking evening/night window (default 18:30–23:59) with randomized, non-round minutes/seconds. Also updates author/committer name and email. Use when the user asks to "change today's commit times", "make commits look like they were done in the evening", "batch modify git author/date", or "rewrite commit history for today".
---

# Git Rewrite Today’s Commits

## What it does

Rewrites **today’s** (or a specific date’s) commits so they appear to have been authored and committed at naturally random evening/night times. It also updates the author and committer identity.

- Time window defaults to **18:30 – 23:59:59**.
- Generated times avoid round numbers (e.g. `:00`, `:30`) and are spaced at least 10 minutes apart to look realistic.
- **Rewrites commit hashes** via `git rebase -i --root`. If the repo was already pushed, a force-push is required afterwards.

## Quick use

Run the bundled script from the repo root:

```powershell
python "$env:USERPROFILE\.config\agents\skills\git-rewrite-today-commits\scripts\rewrite_today_commits.py" --author "asxiuxiu" --email "licheng1996121@gmail.com"
```

Optional flags:

- `--date YYYY-MM-DD` — target a specific day instead of today
- `--start-time HH:MM` — earliest time (default 18:30)
- `--end-time HH:MM` — latest time (default 23:59)

## Manual workflow (if the script cannot be run directly)

1. List today’s commits in chronological order:
   ```powershell
   git log --reverse --since="YYYY-MM-DD 00:00" --until="YYYY-MM-DD 23:59:59" --format="%H %s"
   ```
2. Generate one random timestamp per commit inside the desired evening window. Avoid round minutes/seconds and keep commits ≥ 10 min apart.
3. Build an interactive rebase todo file with `pick <hash> <msg>` followed by `exec git commit --amend --no-edit --reset-author --date="<timestamp>"` for each commit, setting both `GIT_AUTHOR_*` and `GIT_COMMITTER_*` environment variables.
4. Run `git rebase -i --root` and inject the todo file via `GIT_SEQUENCE_EDITOR`.

## Safety notes

- This permanently rewrites history for the selected commits. Do not use on shared branches unless you intend to force-push.
- The script operates only on the current branch (`HEAD`).
