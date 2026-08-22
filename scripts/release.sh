#!/usr/bin/env bash
#
# Show which sessions exist in the repository and which are actually published.
#
#   ./scripts/release.sh status
#
# Read-only. Releasing a session means uncommenting its lines in the render
# allowlist in _quarto.yml -- deliberately a manual edit, so that publishing
# is always an explicit act rather than a side effect of writing content.
#
set -euo pipefail

cd "$(dirname "$0")/.."

cmd="${1:-status}"

if [[ "$cmd" != "status" ]]; then
  echo "usage: $0 status" >&2
  exit 2
fi

# A session is released if an uncommented render entry references its
# directory. Comment markers are what distinguish held-back from live.
is_released() {
  local dir="$1"
  grep -qE "^[[:space:]]*-[[:space:]]*\"${dir}/" _quarto.yml
}

# ...and REACHABLE if something links to its index: the navbar in _quarto.yml,
# or the schedule.
#
# WHY THIS IS CHECKED. Releasing a session is three edits in three places -- the
# render allowlist, the navbar, and schedule.qmd -- and only the first one is
# what anybody remembers, because only the first one is what "release" sounds
# like. Miss the other two and the session is live, deployed, and reachable only
# by guessing its URL. Nothing fails: check-links.sh only rejects links that are
# BROKEN, never notices links that are ABSENT, so every gate stays green.
#
# The allowlist writes `lectures/NN-name/*.qmd` while a link writes
# `lectures/NN-name/index.qmd`, so matching on `index.qmd` cannot mistake the
# allowlist entry for a link.
is_linked() {
  local dir="$1"
  grep -q "${dir}/index.qmd" _quarto.yml || grep -q "${dir}/index.qmd" schedule.qmd
}

printf "%-34s %-11s %s\n" "SESSION" "STATUS" "REACHABLE"
printf "%-34s %-11s %s\n" "-------" "------" "---------"

found=0
unreachable=0
for dir in lectures/*/ practicals/*/ ; do
  [[ -d "$dir" ]] || continue
  dir="${dir%/}"
  found=1
  if is_released "$dir"; then
    if is_linked "$dir"; then
      printf "%-34s %-11s %s\n" "$dir" "released" "yes"
    else
      printf "%-34s %-11s %s\n" "$dir" "released" "** NO LINK **"
      unreachable=$((unreachable + 1))
    fi
  else
    printf "%-34s %-11s %s\n" "$dir" "held back" "-"
  fi
done

if [[ "$found" -eq 0 ]]; then
  echo "(no sessions found)"
  exit 0
fi

echo
echo "Releasing a session is THREE edits, and only the first is called release:"
echo "  1. uncomment its line in the render allowlist in _quarto.yml"
echo "  2. add it to the navbar in _quarto.yml -- for the FIRST practical this"
echo "     means re-creating the whole Practicals menu, which is removed while"
echo "     it would be empty, because Quarto rejects a menu with no entries"
echo "  3. link it from schedule.qmd"
echo "Then:  ./scripts/publish.sh site"

if [[ "$unreachable" -gt 0 ]]; then
  echo
  echo "WARNING: $unreachable released session(s) have no link to them. They are"
  echo "live and reachable only by guessing the URL. Nothing else will tell you:"
  echo "check-links.sh rejects links that are BROKEN, not links that are ABSENT."
fi

echo
echo "The reverse also matters: schedule.qmd must not link to a HELD-BACK"
echo "session -- the link would 404, and check-links.sh catches that in CI."
