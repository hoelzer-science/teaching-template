#!/usr/bin/env python3
"""Open and close read access between team repositories, for one session.

    ./instructor/team-repos/pair-teams.py --term ws2627 --prefix <module> \
        --roster ~/roster.tsv --grant team-01,team-02 team-03,team-04
    ./instructor/team-repos/pair-teams.py ... --grant ... --dry-run
    ./instructor/team-repos/pair-teams.py --term ws2627 --prefix <module> \
        --roster ~/roster.tsv --revoke

WHAT THIS EXISTS FOR, AND THE TRAP IT CLOSES. `create-team-repos.py` adds
students as OUTSIDE COLLABORATORS on their own repository, so a student can
reach exactly one repo. That is deliberate and it is what stops a later group
reading an earlier group's answers -- see this directory's README.

It also silently forbids something a practical may well want: a **peer review**,
in which each team reads another team's repository and files an issue on it.
A session can be written asking for exactly that, and the page and the access
model then contradict each other with **every CI gate green**, because the claim
is about GitHub permissions rather than about the rendered site. That happened in
the module this came from, and it survived two weeks. If your practical has a
cross-review, this script is how it works.

WHY NOT JUST MAKE THE REPOSITORIES PUBLIC FOR THE DAY. Two reasons that outlast
any one module. Changing visibility needs `admin`, so it is the instructor's
action on every repository rather than the students' own; and publishing named
coursework should be opt-in rather than a blanket flip. Access that is granted
and revoked leaves nothing behind. (Whether the repositories go public *later*,
at the students' choice, is a separate and much better question -- a finished
analysis is a real portfolio piece.)

GROUPS, NOT PAIRS. Each --grant argument is a comma-separated group of two or
three teams, and every team in a group gets read access to every other team's
repository in it. Two is the normal case. Three is the answer to an odd number of
teams: each team in a three-group is reviewed by the two others, so nobody is
left out and nobody goes unreviewed. The pairing is a decision made in the room
from who actually turned up, so this script is TOLD the groups rather than
computing them -- and it takes only the teams present, which is what keeps the
pairing inside one group when a session runs twice.

READ, NOT WRITE. The grant is `pull`. A reviewer must not be able to push to the
repository they are reviewing, and read is enough to open an issue.

REVOKE IS SELF-HEALING and does not need to remember the pairing. Given the
roster, it removes every collaborator on a team's repository who is not a member
of that team -- so it undoes a grant nobody wrote down, is safe to run twice, and
verifies afterwards that none is left. That last part matters: a failed DELETE is
the only outcome here that leaves access open past the session.

Needs `gh`, authenticated with admin rights on the org's repositories.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

TEAM_PATTERN = re.compile(r"^team-\d{2}$")


def gh(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["gh", *args], capture_output=True, text=True, check=check)


def read_roster(path: Path) -> dict[str, list[str]]:
    """The same two-column TSV `create-team-repos.py` reads.

    Kept as a second copy of ten lines rather than an import, because both
    scripts are run by hand from a path and neither has a package around it. If
    the roster format changes, it changes in both.
    """
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
        if user not in teams[team]:
            teams[team].append(user)
    return dict(sorted(teams.items()))


def parse_groups(specs: list[str], teams: dict[str, list[str]]) -> list[list[str]]:
    """Turn `team-01,team-02` arguments into validated groups.

    Every failure here is cheap to make in the room and expensive to notice: a
    typo'd team name silently grants nobody anything, and a team listed in two
    groups reads two repositories while somebody reads none.
    """
    groups = []
    seen: dict[str, int] = {}
    for index, spec in enumerate(specs, start=1):
        group = [t.strip() for t in spec.split(",") if t.strip()]
        if not 2 <= len(group) <= 3:
            raise SystemExit(f"group {index}: {spec!r} has {len(group)} team(s); want 2 or 3")
        for team in group:
            if not TEAM_PATTERN.match(team):
                raise SystemExit(f"group {index}: {team!r} is not of the form team-01")
            if team not in teams:
                raise SystemExit(f"group {index}: {team} is not in the roster")
            if team in seen:
                raise SystemExit(f"{team} is in group {seen[team]} and group {index}")
            seen[team] = index
        groups.append(group)

    # Expected, and not a warning: the roster covers every team while a session
    # holds only some of them, so running this for one group leaves the rest
    # ungrouped. It is printed anyway, because the one case it catches -- a team
    # present in the room and missing from the pairing -- looks exactly the same
    # from here and is only visible to whoever is standing in front of them.
    unpaired = sorted(set(teams) - set(seen))
    if unpaired:
        print(f"  not in a group: {', '.join(unpaired)}")
        print("  (expected for teams not in this session -- check none of them is in the room)")
    return groups


def repo_of(org: str, prefix: str, term: str, team: str) -> str:
    return f"{org}/{prefix}-{term}-{team}"


def collaborators(full: str) -> list[str]:
    """Direct collaborators only.

    `affiliation=direct` excludes organisation owners, who reach every repository
    through the org and must never be removed by a revoke.
    """
    result = gh("api", f"/repos/{full}/collaborators?affiliation=direct&per_page=100",
                "--jq", ".[].login", check=False)
    if result.returncode != 0:
        raise SystemExit(f"{full}: cannot list collaborators -- does it exist?")
    return [line for line in result.stdout.splitlines() if line]


def grant(groups: list[list[str]], teams: dict[str, list[str]], args) -> None:
    for group in groups:
        print(f"\n== {' <-> '.join(group)}")
        for reviewed in group:
            full = repo_of(args.org, args.prefix, args.term, reviewed)
            for reviewer in group:
                if reviewer == reviewed:
                    continue
                for user in teams[reviewer]:
                    if args.dry_run:
                        print(f"  would grant {user} ({reviewer}) read on {reviewed}")
                        continue
                    gh("api", "-X", "PUT", f"/repos/{full}/collaborators/{user}",
                       "-f", f"permission={args.permission}")
                    print(f"  granted {user} ({reviewer}) {args.permission} on {reviewed}")


def revoke(teams: dict[str, list[str]], args) -> None:
    for team, members in teams.items():
        full = repo_of(args.org, args.prefix, args.term, team)
        extra = [u for u in collaborators(full) if u not in members]
        if not extra:
            print(f"  {team}: nothing to revoke")
            continue
        for user in extra:
            if args.dry_run:
                print(f"  would remove {user} from {team}")
                continue
            gh("api", "-X", "DELETE", f"/repos/{full}/collaborators/{user}")
            print(f"  removed {user} from {team}")

    if args.dry_run:
        return
    left = {team: [u for u in collaborators(repo_of(args.org, args.prefix, args.term, team))
                   if u not in members]
            for team, members in teams.items()}
    still = {t: u for t, u in left.items() if u}
    if still:
        raise SystemExit(f"\nSTILL HAVE ACCESS: {still}")
    print("\nVerified: every repository has only its own team on it.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--term", required=True, help="e.g. ws2627")
    parser.add_argument("--prefix", required=True,
                        help="repository name prefix, the same one create-team-repos.py used")
    parser.add_argument("--org", default="hoelzer-teaching",
                        help="the GitHub organisation holding the team repositories")
    parser.add_argument("--roster", type=Path, required=True,
                        help="the same two-column TSV create-team-repos.py reads")
    parser.add_argument("--grant", nargs="+", metavar="TEAM,TEAM[,TEAM]",
                        help="groups to open for the session")
    parser.add_argument("--revoke", action="store_true",
                        help="remove every collaborator who is not on their own team")
    parser.add_argument("--permission", default="pull",
                        help="pull (read) is enough to open an issue; change only if it is not")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if bool(args.grant) == args.revoke:
        raise SystemExit("give exactly one of --grant and --revoke")

    teams = read_roster(args.roster.expanduser())
    print(f"{len(teams)} team(s), {sum(len(m) for m in teams.values())} student(s)")

    if args.revoke:
        revoke(teams, args)
    else:
        grant(parse_groups(args.grant, teams), teams, args)
        if not args.dry_run:
            print("\nDone. REVOKE AFTER THE SESSION:")
            print(f"  {sys.argv[0]} --term {args.term} --prefix {args.prefix} "
                  f"--roster {args.roster} --revoke")
    return 0


if __name__ == "__main__":
    sys.exit(main())
