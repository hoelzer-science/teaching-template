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

## The three scripts

| | |
|---|---|
| `build-team-template.py` | writes the template repository from this one, so it is a **build artefact** and nothing is authored there |
| `create-team-repos.py` | a roster becomes one private repository per team, personalised, with the students invited |
| `pair-teams.py` | opens read access **between** teams for one session, and revokes it — only needed if your practical has a peer review |

All three are idempotent and all three have a read-only `--dry-run`.

```bash
./instructor/team-repos/build-team-template.py ~/git/<module>-team-template --dry-run
./instructor/team-repos/create-team-repos.py ~/roster.tsv \
    --term ws2627 --prefix <module> --template <org>/<module>-team-template --dry-run
./instructor/team-repos/pair-teams.py --term ws2627 --prefix <module> \
    --roster ~/roster.tsv --grant team-01,team-02 team-03,team-04 --dry-run
```

### If your practical has a cross-review, read this before writing it

**The access model above forbids it, and no CI gate will tell you.** A session
that asks each team to read another team's repository and file an issue on it is
a perfectly good exercise — and outside collaborators reach exactly one
repository, so students cannot open the other repo at all. The page and the
access model then contradict each other with every gate green, because the claim
is about *GitHub permissions* rather than about the rendered site. In the module
this came from, two designs of record disagreed for two weeks before anyone
noticed.

`pair-teams.py --grant` opens it for the session and `--revoke` closes it again.
Three things about it are deliberate:

- **Groups of two or three, not pairs.** Three is the answer to an odd number of
  teams: each is reviewed by the two others, so nobody is left out.
- **`pull`, not `push`.** A reviewer must not be able to write to what they
  review, and read is enough to open an issue.
- **`--revoke` is self-healing.** It removes every collaborator who is not on
  that team, so it does not need to remember the pairing, is safe to run twice,
  and verifies afterwards that none is left.

**Do not reach for making the repositories public instead.** Changing visibility
needs `admin`, so it is your action on every repository rather than the students'
own, and a blanket flip is not opt-in. Whether they go public *afterwards*, at
each team's choice, is a separate and much better question — a finished analysis
is a real portfolio piece, and for a cohort that does not otherwise write code in
public it may be the most useful thing they leave with.

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
