# Team repositories

**Only needed if your practical has students working in teams on their own
data.** Delete this directory if it does not.

The model, from one module that ran it:

- **One private GitHub repository per team**, in a course organisation, created
  from a **team template repository**. Students are added as **outside
  collaborators on their own repository** — never as organisation members, which
  would let them see every other team's work.
- **The repository's README is the lab notebook.** No separate written protocol
  to mark: the repository already carries the evidence, and discussing the work
  teaches more than a document nobody reads twice.
- **The template ships the semester's questions empty**, as a `findings.json`
  with every value `null`, and an obstacle-log table in the README. Prose in the
  first session is forgotten by the third; a file with empty headings sitting in
  the repository is not.
- **`null` and `[]` are different statements** — *not recorded* against *we
  looked and found none* — and saying so in the template is worth more than
  saying it in a lecture.

## The two scripts

| | |
|---|---|
| `build-team-template.py` | writes the template repository from this one, so it is a **build artefact** and nothing is authored there |
| `create-team-repos.py` | a roster becomes one private repository per team, personalised, with the students invited |

Both are idempotent and both have a read-only `--dry-run`.

```bash
./instructor/team-repos/build-team-template.py ~/git/<module>-team-template --dry-run
./instructor/team-repos/create-team-repos.py ~/roster.tsv \
    --term ws2627 --prefix <module> --template <org>/<module>-team-template --dry-run
```

**Adapt `personalise()` in `create-team-repos.py` to your own template.** The
pattern to keep is in its docstring: **verify each edit by looking for what
should now be there, never for the absence of the placeholder.** A placeholder
often appears twice — once as the value to replace and once in a guard that must
survive — and an absence check fails on the guard every time.

## Three things that will bite

- **The template repository must have its *Template repository* setting on**, or
  `gh repo create --template` fails.
- **`git check-ignore -q` exits 0 for a negated pattern too**, and
  `git status --ignored` says "not ignored" for anything already in the index. To
  ask whether a file would be kept out, use `git check-ignore --no-index -v` and
  test whether the matched pattern starts with `!`. `build-team-template.py`
  refuses to finish if it wrote a file git would not take — that check exists
  because an unanchored `data/` in a template's `.gitignore` silently swallowed
  every example file a unit's tests needed.
- **Collect GitHub usernames before the first session**, through whatever the
  LMS offers that needs no plugin — one assignment, one submission per team, both
  names and both usernames. The repository has to exist when the session starts,
  because cloning it *is* the Git teaching. Creating a dozen repositories is not
  what to be doing in the first hour of a practical.
