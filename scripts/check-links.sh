#!/usr/bin/env bash
#
# Verify that every local link AND image in a rendered build resolves to a real
# file.
#
#   ./scripts/check-links.sh _site
#   ./scripts/check-links.sh _lms
#
# Catches three regressions that have already bitten once each:
#   - .qmd links surviving into output (the `default` project type used by the
#     LMS profile does not rewrite them the way a website project does)
#   - links pointing at pages that were excluded from the render
#   - IMAGES whose target no longer exists, after a figure is renamed, deleted
#     or moved between a session directory and shared/figures/
#
# The image case was found on 2026-08-06 and was silent in the worst way: a
# figure was promoted to shared/figures/ and one document still emitted
# src="figures/read-mapping.svg", pointing at a file that no longer existed,
# while this script reported "all local links resolve" -- because it only ever
# looked at href. A broken figure passes every other gate too, so nothing
# anywhere caught it. Hence: src is now checked exactly like href.
#
# External (http/https) links are not checked -- that needs network access and
# belongs in a scheduled job, not the build.
#
# <script> blocks are stripped before scanning. Minified JavaScript contains
# things that look exactly like local hrefs -- mermaid's bundle builds strings
# such as href="'+t+'" -- and the LMS build inlines every library, so a single
# diagram in a document was enough to fail the whole check on a link that does
# not exist. Only the document's own markup should be scanned. Stripping
# <script> also removes <script src="..."> tags, which is correct: those are
# Quarto's own bundled libraries, not authored references.
#
# Note the attribute regex excludes any value containing a colon. That is what
# skips http://, https://, mailto: and -- importantly for the LMS build --
# data: URIs, since `embed-resources` inlines every image as base64. It also
# means a value can never contain a colon, which is why "attr:value" below is
# an unambiguous encoding.
#
set -euo pipefail

dir="${1:-_site}"

if [[ ! -d "$dir" ]]; then
  echo "error: '$dir' does not exist -- render it first" >&2
  exit 1
fi

broken=0
checked=0

while IFS= read -r page; do
  page_dir=$(dirname "$page")

  # Local href and src only: skip absolute URLs, anchors, mailto:, data: etc.
  # Each entry arrives as "attr:value"; the value is colon-free by construction
  # (see the regex below), so splitting on the first colon is unambiguous.
  while IFS= read -r entry; do
    [[ -z "$entry" ]] && continue
    attr="${entry%%:*}"
    link="${entry#*:}"
    [[ -z "$link" ]] && continue
    checked=$((checked + 1))
    target="${link%%#*}"            # strip any fragment
    [[ -z "$target" ]] && continue  # pure in-page anchor

    # A .qmd link must never survive into a build. Two ways it happens, both
    # bad, and neither is caught by an existence test:
    #   - the LMS build does not rewrite .qmd -> .html (see publish.sh)
    #   - linking to a session held back from the render allowlist makes
    #     Quarto copy its raw source into the output as a resource, so the
    #     file DOES exist and students get served markdown
    if [[ "$target" == *.qmd ]]; then
      echo "QMD LINK: $page -> $link"
      echo "          (a held-back session, or an unrewritten LMS link)"
      broken=$((broken + 1))
      continue
    fi

    if [[ ! -e "$page_dir/$target" ]]; then
      if [[ "$attr" == "src" ]]; then
        echo "BROKEN IMAGE: $page -> $link"
        echo "              (renamed, deleted, or moved to/from shared/figures/?)"
      else
        echo "BROKEN: $page -> $link"
      fi
      broken=$((broken + 1))
    fi
  done < <(perl -0777 -pe 's{<script\b.*?</script>}{}gis' "$page" 2>/dev/null \
             | grep -ohE '(href|src)="[^":]*"' 2>/dev/null \
             | sed 's/^href="/href:/; s/^src="/src:/; s/"$//' \
             | grep -vE '^(href|src):#' || true)

done < <(find "$dir" -name '*.html')

echo "checked $checked local link(s) and image(s) in $dir"

if [[ "$broken" -gt 0 ]]; then
  echo "FAILED: $broken broken reference(s)" >&2
  exit 1
fi

echo "OK: all local links and images resolve"
