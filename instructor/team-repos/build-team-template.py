#!/usr/bin/env python3
"""Sync the mechanical half of the team repository template.

    ./instructor/team-repos/build-team-template.py ~/git/<module>-team-template
    ./instructor/team-repos/build-team-template.py ~/git/... --dry-run

WHAT THIS EXISTS FOR. A template is *copied*, not linked: once thirteen team
repositories have been created from it, a fix does not propagate. So everything
that can be derived from this repository is derived from it, once, immediately
before the repositories are created -- rather than pasted across by hand and
left to drift.

WHAT IT SYNCS -- which, as of 2026-08-22, is EVERYTHING in the template except
its lock file:

    scripts/fetch-data.py         <- instructor/team-repos/fetch-data.py
    pixi.toml                     <- instructor/team-repos/team-template/pixi.toml
    README.md                     <- instructor/team-repos/team-template/README.md
    findings.json                 <- instructor/team-repos/team-template/findings.json
    .gitignore                    <- instructor/team-repos/team-template/gitignore
    practicals/NN-name/starter/   <- practicals/NN-name/starter/
    practicals/NN-name/data/      <- practicals/NN-name/data/

SO THE TEMPLATE REPOSITORY IS A BUILD ARTEFACT. Nothing is authored there any
more, and an edit made there is reverted by the next run -- reported first, but
reverted. Make every change here.

Why all five moved, in the order the reasons appeared: fetch-data.py and
pixi.toml so there is one version rather than a command pasted into two pages;
README.md because it carries a section per unit mirroring the "What to commit"
table on five pages that live here; and findings.json and .gitignore because a
change to the course changes them too -- findings.json holds the eight keys P06
checks for, and the .gitignore has to know about every file the units produce.
A convention kept in two REPOSITORIES decays faster than one kept in two files,
because no grep spans them and no gate sees both.

.gitignore is stored here as `gitignore`, without the leading dot, so this
repository's own ignore rules need no exception for it.

pixi.lock is the one thing still made in the template, by `pixi lock` -- it is
derived from pixi.toml, so it cannot be authored anywhere. This script checks
that it is not stale rather than regenerating it.

Reference solutions are NEVER copied. That is asserted, not assumed -- a
solution reaching a student repository is the one failure here that cannot be
taken back.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# Every unit whose Compute layer ships to students. P01 is included: it is the
# session in which the repository is cloned, and its exercise reads the capture
# file the same session produced.
UNITS = [
    "01-alignment",
]

FORBIDDEN = ("solution", "TRUTH.json", "panel-contents.tsv")


def is_ignored(repo: Path, path: Path) -> bool:
    """Would .gitignore keep this file out of the repository?

    Two ways to get this wrong, both met while writing it:

    - `git check-ignore -q` exits 0 for a NEGATED pattern too, so a naive check
      calls a deliberately protected file ignored. `-v` prints the pattern that
      matched, and a negation is shown with its leading `!`, which is the only
      unambiguous signal.
    - `git status --ignored` answers "no" for any file already in the index,
      because a tracked file is never ignored. That makes the check pass on a
      second run and fail only on the first, which is the worst kind of check.
      `--no-index` answers from the patterns alone.
    """
    result = subprocess.run(
        ["git", "-C", str(repo), "check-ignore", "--no-index", "-v", "--",
         str(path.relative_to(repo))],
        capture_output=True, text=True, check=False,
    )
    if result.returncode != 0:          # no pattern matched at all
        return False
    for line in result.stdout.splitlines():
        _source, _lineno, rest = line.split(":", 2)
        pattern = rest.split("\t", 1)[0]
        return not pattern.startswith("!")
    return False


def copy(source: Path, target: Path, dry_run: bool, actions: list[str],
         written: list[Path] | None = None) -> None:
    if any(part in str(source) for part in FORBIDDEN):
        raise SystemExit(f"refusing to copy {source}: matches {FORBIDDEN}")
    if written is not None:
        written.append(target)
    if target.exists() and target.read_bytes() == source.read_bytes():
        return

    verb = "would write" if dry_run else "wrote"
    actions.append(f"{verb} {target}")
    # Overwriting something that was already there and DIFFERENT is the one case
    # worth saying out loud: it is what a hand edit made in the template
    # repository looks like from here, moments before it disappears. Most of the
    # synced files carry a maintainer comment saying "edit this in the course
    # repository" -- but findings.json is JSON and cannot, so for that one this
    # report is the only warning there is.
    if target.exists():
        actions.append("    ^ the template's version differed and is being "
                       "replaced; if that was a hand edit, make it in the "
                       "course repository instead")
    if not dry_run:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("template", type=Path,
                        help="a checkout of the team repository template")
    parser.add_argument("--dry-run", action="store_true",
                        help="say what would change, change nothing")
    args = parser.parse_args()

    template = args.template.expanduser().resolve()
    if not (template / ".git").is_dir():
        raise SystemExit(f"{template} is not a git checkout")

    actions: list[str] = []
    written: list[Path] = []

    copy(ROOT / "instructor/team-repos/fetch-data.py",
         template / "scripts/fetch-data.py", args.dry_run, actions, written)
    copy(ROOT / "instructor/team-repos/team-template/pixi.toml",
         template / "pixi.toml", args.dry_run, actions, written)
    copy(ROOT / "instructor/team-repos/team-template/README.md",
         template / "README.md", args.dry_run, actions, written)
    copy(ROOT / "instructor/team-repos/team-template/findings.json",
         template / "findings.json", args.dry_run, actions, written)
    copy(ROOT / "instructor/team-repos/team-template/gitignore",
         template / ".gitignore", args.dry_run, actions, written)

    for unit in UNITS:
        source = ROOT / "practicals" / unit
        if not source.is_dir():
            raise SystemExit(f"no such unit: {source}")
        for kind in ("starter", "data"):
            if not (source / kind).is_dir():
                continue
            for item in sorted((source / kind).iterdir()):
                if item.is_dir() or item.name.startswith("."):
                    continue
                copy(item, template / "practicals" / unit / kind / item.name,
                     args.dry_run, actions, written)

    # The one thing that must never happen, checked rather than trusted.
    leaked = [p for p in template.rglob("*")
              if p.is_file() and ".git/" not in str(p)
              and any(bad in str(p) for bad in FORBIDDEN)]
    if leaked:
        print("FAIL: solution or answer-key material is in the template:", file=sys.stderr)
        for path in leaked:
            print(f"  {path}", file=sys.stderr)
        return 1

    # The second thing that must never happen, and it DID on the first real run
    # (2026-08-21): the template's .gitignore had a bare `data/`, which matches a
    # directory of that name at ANY depth, so all eleven example files under
    # practicals/*/data/ were silently uncommittable. Nothing would have failed
    # here or on push -- it would have surfaced as every unit's tests dying on a
    # student's fresh clone with a missing file.
    #
    # A file this script wrote and git will not take is a failure of this script.
    if not args.dry_run:
        swallowed = [p for p in written if is_ignored(template, p)]
        if swallowed:
            print("FAIL: .gitignore would swallow files this script just wrote:",
                  file=sys.stderr)
            for path in swallowed:
                print(f"  {path.relative_to(template)}", file=sys.stderr)
            print("\nFix the template's .gitignore, then run again.", file=sys.stderr)
            return 1

    for action in actions:
        print(action)
    if not actions:
        print("nothing to do -- the template is already in step")

    # Nothing can check whether the README's prose is still true, but it can
    # check that a section exists at all, which is what goes missing when a unit
    # is added. Watch the SOURCE, since that is where it would be introduced.
    readme = (ROOT / "instructor/team-repos/team-template/README.md").read_text()
    absent = [unit for unit in UNITS if f"## P{unit.split('-')[0]} " not in readme]
    if absent:
        print("\n  WARNING: the team README has no section for:", ", ".join(absent))
        print("  Each unit's section names the artefacts that unit expects committed.")

    # pixi.lock is the only file in the template not authored here, because it is
    # derived from pixi.toml. That makes it the one that can go stale: change the
    # toml, sync, forget to lock, push, and every team installs an environment
    # that does not match its own manifest. `pixi lock --check` exits non-zero
    # when the lock would change, which is exactly the question.
    if shutil.which("pixi") is None:
        print("\n  NOTE: pixi is not on PATH, so pixi.lock was not checked.")
    else:
        stale = subprocess.run(["pixi", "lock", "--check"], cwd=template,
                               capture_output=True, text=True).returncode != 0
        if stale:
            print("\n  WARNING: pixi.lock does not match pixi.toml.")
            print("  Run `pixi lock` in the template before committing, or teams")
            print("  install an environment their own manifest does not describe.")

    print("\nNothing in the template is authored there any more. Every file comes")
    print("from this repository except pixi.lock, which `pixi lock` derives from")
    print("pixi.toml. Make changes here, then sync.")

    if not args.dry_run and actions:
        print("\nThen, in the template checkout:")
        print("  pixi lock          # only if the warning above asked for it")
        print("  git add -A && git commit && git push")
        print("\nA team repository created BEFORE this push does not get any of it.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
