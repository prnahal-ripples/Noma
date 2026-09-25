# `.claude/launch.json` — why it conflicted, and how to fix it in any repo

**Status:** fixed in `noise-design/Noma` (`b781f43`, `f62ab28`) and
`noise-design/noiseFit` (`d695dba`, `87f2297`), 2026-09-09/10.
**Applies to:** any repo where people run Claude Code. Nothing NOMA-specific.

---

## The symptom

Three things, which look unrelated but are all the same cause:

1. `git status` always showed `M .claude/launch.json`, in a repo you had not
   knowingly touched. Reverting it worked, and then it came back.
2. Pushing or pulling produced a **merge conflict on that file** whenever two
   sessions, two machines, or two people had both been in the repo.
3. The file kept getting **swept into unrelated commits** — anything using
   `git add -A` or `git add .` picked it up. In the NOMA first-run work it had
   to be pulled back out of **three** commits, and it was still committed four
   separate times with different contents before anyone caught the pattern.

## The cause

`.claude/launch.json` is the **preview-server registry** Claude Code reads to
start a local dev server. It is *machine-local state* that was being *tracked
in git*.

Every session that starts a preview writes an entry into it, and those entries
carry **absolute, session-scoped paths**. Two real examples found in the two
repos on the same day:

```
/private/tmp/claude-502/-Users-…-Desktop-Noma-main/50ee420e-…/scratchpad/serve-dash.py
/private/tmp/claude-502/-Users-…-scratch-workspaces-83ad1b7b-…-2026-09-08-…/scratchpad/coach
```

Those paths exist for one session on one machine. To anyone else — and to the
same person tomorrow — they are meaningless, and they will 404 or fail to
launch. So the file's content is *guaranteed* to differ between any two
checkouts, which is the definition of a file that must not be tracked.

Worse, a session that only wanted to add its own entry would sometimes
overwrite entries someone else relied on. In noiseFit, a session on 8 Sep
replaced the shared `noisefit-dashboard` server with its own `coach-preview`
entry, so the dashboard's own preview stopped resolving for everyone.

## The fix

Stop tracking the live file; keep a committed template beside it.

⚠ **Do not rename the live file.** `.claude/launch.json` is the exact path the
preview tooling reads. If you rename it, previews silently stop resolving in
that repo. Only the *template* gets a project-specific name — which is also the
point of naming it, since a file called `launch.example.json` is
indistinguishable when two repos are open side by side.

```bash
# from the repo root
REPO=Noma        # -> launch.Noma.json ; use your own project name

# 1 · keep the entries worth sharing as a template
cp .claude/launch.json ".claude/launch.$REPO.json"
#    then EDIT that copy: delete every entry with a /private/tmp path or any
#    other machine-specific absolute path. What should remain is the servers
#    the team genuinely shares (plain localhost URLs, or commands with
#    repo-relative paths).

# 2 · stop tracking the live file, without deleting it from disk
git rm --cached .claude/launch.json

# 3 · ignore it from now on
cat >> .gitignore <<EOF

# Machine-local preview servers. Sessions rewrite this with session-scoped
# /private/tmp paths; see .claude/launch.$REPO.json for the shared baseline.
.claude/launch.json
EOF

git add .gitignore ".claude/launch.$REPO.json"
git commit -m "Stop tracking .claude/launch.json; ship a template instead"
```

### Verify it worked

```bash
git status --short                              # expect: clean
git ls-files .claude/ | grep launch             # expect: only launch.<REPO>.json
git check-ignore -v .claude/launch.json         # expect: a .gitignore hit
ls .claude/launch.json                          # expect: STILL THERE on disk
```

Then **start a preview server** from the repo. That is the step people skip,
and it is the only one that proves the tooling still resolves its config.

## Things that will bite you

- **Untrack only `launch.json`.** Everything else under `.claude/` is usually
  real shared content and must stay tracked — in these two repos that is the
  rules files (`.claude/rules/*.md`) and a skill
  (`.claude/skills/animate-text/`). `git rm -r --cached .claude` would throw
  those away.
- **`git rm --cached`, never `git rm`.** The plain form deletes the working
  file and the person loses their local server config.
- **Do not silently drop other people's entries** when you edit the template.
  Check what is in the live file first. In noiseFit the shared dashboard entry
  had already been clobbered by another session, so the fix put it back
  *alongside* the newer entry rather than choosing between them.
- **A path under `/private/tmp` existing today proves nothing.** Those
  directories are session scratch space and get cleaned up. Treat any absolute
  path outside the repo as temporary by default.

## This procedure was tested, not just written

The commands above were run end to end in a throwaway repo that reproduced the
situation (a tracked `launch.json` holding one shared entry and one
`/private/tmp` entry, plus a shared rules file). Result: clean `git status`,
only the template tracked, the live file ignored but still on disk, the shared
rules file untouched, and the scratch entry stripped from the template while
the team entry survived.

The conflict itself was then reproduced and confirmed gone: two clones of a
bare repo, each writing its own `launch.json` with its own `/private/tmp`
path, both committing real work — `git pull --rebase` and `git push` both
succeeded with no conflict, and each clone kept its own config. Before the
fix, that same sequence is what produced the merge conflict.

## Why this was not caught sooner

The file is small, it is inside a dot-directory, and each individual instance
looked like a one-line accident rather than a pattern. The tell was frequency:
once you notice the same path in a fourth commit, it is not an accident, it is
a file in the wrong category. **State that a tool writes per-session belongs in
`.gitignore`, and the shared baseline belongs in a template next to it.**
