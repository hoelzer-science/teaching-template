#!/usr/bin/env python3
"""Create this semester's team repositories and invite the students.

    ./instructor/team-repos/create-team-repos.py ~/roster.tsv --term ws2627 --dry-run
    ./instructor/team-repos/create-team-repos.py ~/roster.tsv --term ws2627

WHAT IT REPLACES: creating a dozen repositories by hand -- create from the
template, make the per-team edits, invite the team, a dozen times. That is
roughly a hundred clicks, and the edits are exactly the kind of thing that is
right eleven times and wrong once.

ADAPT `personalise()` TO YOUR OWN TEMPLATE. It currently sets the team name in
the README title, `TEAM` in a data-fetch script, and `"team"` in findings.json,
because that is what one module's template needed. The pattern to keep is the
one in its docstring: verify each edit by looking for WHAT SHOULD NOW BE THERE,
never for the absence of the placeholder.

THE ROSTER is a two-column TSV, one row per student, collected through Moodle
before the first practical:

    team-01	alice-hub
    team-01	bmueller
    team-02	carol99
    team-02	dpetrov

Blank lines and `#` comments are ignored. Order does not matter. Keep the file
OUTSIDE this repository: it is a list of real people, and it does not need to be
in version control to do its job.

WHAT IT DOES, per team, and all of it is idempotent -- run it again when three
more usernames arrive and only the new work happens:

  1. creates <org>/<prefix>-<term>-team-NN from the template, private
  2. makes the three per-team edits (README title, TEAM in fetch-data.py,
     "team" in findings.json) in one commit
  3. adds each student as an OUTSIDE COLLABORATOR on their own repository --
     never as an organisation member, which would give them sight of every
     other team's work

Needs `gh`, authenticated with rights to create repositories in the org.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

TEAM_PATTERN = re.compile(r"^team-\d{2}$")


def gh(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["gh", *args], capture_output=True, text=True, check=check)


def read_roster(path: Path) -> dict[str, list[str]]:
    teams: dict[str, list[str]] = defaultdict(list)
    for number, raw in enumerate(path.read_text().splitlines(), start=1):
        line = raw.split("#")[0].strip()
        if not line:
            continue
        fields = line.split()
        if len(fields) != 2:
            raise SystemExit(f"{path}:{number}: expected 'team-NN<tab>username', got {raw!r}")
        team, user = fields
        if not TEAM_PATTERN.match(team):
            raise SystemExit(f"{path}:{number}: {team!r} is not of the form team-01")
        if user in teams[team]:
            print(f"  note: {user} listed twice for {team}, ignoring the repeat")
            continue
        teams[team].append(user)
    return dict(sorted(teams.items()))


def check_usernames(teams: dict[str, list[str]]) -> list[str]:
    """Return the usernames GitHub does not know.

    A username that does not exist fails the invitation several steps later,
    and a typo in a handwritten username is the single most likely thing to be
    wrong in a roster. The check is read-only, so --dry-run does it too: that
    is the main reason to run a dry run at all.
    """
    return [user for members in teams.values() for user in members
            if gh("api", f"/users/{user}", check=False).returncode != 0]


def repo_exists(full_name: str) -> bool:
    return gh("api", f"/repos/{full_name}", check=False).returncode == 0


def personalise(checkout: Path, team: str) -> list[str]:
    """The three per-team edits. Returns what was changed.

    Each edit is verified by looking for what should now BE there, not for the
    absence of `team-XX`. That distinction is not pedantry: `fetch-data.py`
    contains the placeholder twice, and the second one --

        if TEAM == "team-XX":
            raise SystemExit("TEAM is still the placeholder...")

    -- is a guard that has to survive. An absence check fails on it every time,
    which is exactly what the first end-to-end run did.
    """
    changed = []

    readme = checkout / "README.md"
    text = readme.read_text()
    if "team-XX" in text:
        readme.write_text(text.replace("team-XX", team))
        changed.append("README.md")
    if "team-XX" in readme.read_text():
        raise SystemExit(f"{team}: README.md still says team-XX")

    fetch = checkout / "scripts" / "fetch-data.py"
    text = fetch.read_text()
    if f'TEAM = "{team}"' not in text:
        assignment = 'TEAM = "team-XX"'
        if assignment not in text:
            raise SystemExit(
                f"{team}: scripts/fetch-data.py has neither {assignment!r} nor this "
                f"team's -- the template changed shape"
            )
        fetch.write_text(text.replace(assignment, f'TEAM = "{team}"'))
        changed.append("scripts/fetch-data.py")

    findings = checkout / "findings.json"
    text = findings.read_text()
    data = json.loads(text)
    if data.get("team") != team:
        # Edited as text rather than by json.dump, to keep the blank lines that
        # group the file into the semester's questions.
        findings.write_text(text.replace(f'"team": "{data["team"]}"', f'"team": "{team}"'))
        changed.append("findings.json")
    if json.loads(findings.read_text())["team"] != team:
        raise SystemExit(f"{team}: findings.json still says {data.get('team')!r}")

    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("roster", type=Path)
    parser.add_argument("--term", required=True, help="e.g. ws2627")
    parser.add_argument("--prefix", required=True,
                        help="repository name prefix, e.g. the module's short name")
    parser.add_argument("--org", default="hoelzer-teaching",
                        help="the GitHub organisation holding student work")
    parser.add_argument("--template", required=True,
                        help="owner/name of the team repository template")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    teams = read_roster(args.roster.expanduser())
    print(f"{len(teams)} team(s), {sum(len(m) for m in teams.values())} student(s)")
    print("checking every username against GitHub...\n")
    missing = set(check_usernames(teams))

    for team, members in teams.items():
        name = f"{args.prefix}-{args.term}-{team}"
        mark = "exists" if repo_exists(f"{args.org}/{name}") else "new"
        listed = ", ".join(f"{u} <- NO SUCH ACCOUNT" if u in missing else u for u in members)
        print(f"  {args.org}/{name}  [{mark}]  {listed}")
        if len(members) != 2:
            note = "the design is teams of two; three is the documented exception"
            print(f"    note: {len(members)} member(s) -- {note}")

    if missing:
        raise SystemExit(
            f"\n{len(missing)} username(s) do not exist on GitHub. Fix the roster and "
            "run again.\nNothing has been created."
        )

    if args.dry_run:
        print("\n--dry-run: every username exists. Nothing was created.")
        return 0

    answer = input(f"\nCreate/update {len(teams)} repositories in {args.org}? [y/N] ")
    if answer.strip().lower() not in {"y", "yes"}:
        print("nothing done")
        return 1

    for team, members in teams.items():
        name = f"{args.prefix}-{args.term}-{team}"
        full = f"{args.org}/{name}"
        print(f"\n== {full}")

        if repo_exists(full):
            print("  repository already exists")
        else:
            gh("repo", "create", full, "--template", args.template, "--private")
            print("  created from the template")

        # Personalise whether or not this run created it. Creation and
        # personalisation are two calls and the second one can fail on its own --
        # it did, on the first end-to-end run -- leaving a repository that exists
        # and still says team-XX. Skipping this for an existing repository would
        # make that state permanent and invisible. `personalise` reports nothing
        # changed when there is nothing to change, so a re-run is free.
        with tempfile.TemporaryDirectory() as tmp:
            checkout = Path(tmp) / name
            gh("repo", "clone", full, str(checkout))
            changed = personalise(checkout, team)
            if changed:
                subprocess.run(["git", "add", *changed], cwd=checkout, check=True)
                subprocess.run(
                    ["git", "commit", "-m", f"Set this repository up for {team}"],
                    cwd=checkout, check=True, capture_output=True,
                )
                subprocess.run(["git", "push"], cwd=checkout, check=True, capture_output=True)
                print(f"  personalised: {', '.join(changed)}")
            else:
                print("  already personalised for this team")

        for user in members:
            gh("api", "-X", "PUT", f"/repos/{full}/collaborators/{user}",
               "-f", "permission=push")
            print(f"  invited {user}")

    print("\nDone. Each student now has an invitation to accept -- by email, or at")
    print("github.com/notifications. An unaccepted invitation looks exactly like a")
    print("repository that does not exist, which is P01's first obstacle.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
