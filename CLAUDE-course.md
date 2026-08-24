# CLAUDE.md — course-<module>

<!--
THIS IS THE MODULE VERSION. In a repo created from teaching-template, run:

    git rm CLAUDE.md && git mv CLAUDE-course.md CLAUDE.md

then replace every <module> / <MODULE> placeholder below. Do this as the first
commit in a new module, before anything else: the template's own CLAUDE.md
states that the repository is public and must not contain real course values,
which is correct upstream and dangerously wrong in a module.
-->

Permanent onboarding for this repository. Changes only when project knowledge
changes. Current working state lives in `NEXT.md`; session history in
`docs/sessions/`.

> This repository was created from **teaching-template** with "Use this
> template", so it has an *unrelated* git history starting from a single initial
> commit. `README.md` came with it and is the authoritative documentation for
> the infrastructure — layout, Cloudflare walkthrough, release allowlist and
> eight hard-won gotchas. Read it first; this file does not repeat it.

## Starting a new course

**Read this first if the repository is still mostly placeholders.** It is the
order that worked once, end to end, and the reasoning for it.

### 0. Set up the scaffolding, before writing anything

```bash
cp COURSE-STRUCTURE.template.md COURSE-STRUCTURE.md   # the design of record
cp NEXT.template.md NEXT.md                            # current state, gitignored
```

Fill in `_course.yml`. Delete `instructor/team-repos/` if the practical has no
teams. Then follow "Setting up hosting for a module" in `README.md`.

**"Use this template" copies files, not labels.** The `retrospective` label
that `.github/ISSUE_TEMPLATE/session-retrospective.md` applies has to be
created once per new repository:

```bash
gh label create retrospective \
  --description "Post-lecture or post-practical debrief, from the session-retrospective issue template" \
  --color "5319E7"
```

### 1. Settle the frame before settling the content

In this order, because each answer constrains the next:

1. **How binding is the module description?** Usually: outcomes and the formal
   frame are, the content list is not. **Get it in writing** — if the
   flexibility was granted verbally, the audit trail for the whole design ends
   at "somebody said so".
2. **What does the examination actually test?** Definitions, or executing a
   procedure by hand, or both. This decides how worked examples are *sized*, and
   it is much cheaper to know now than to rewrite twelve sessions later.
3. **What have the students already been taught?** Find the programme's module
   catalogue and map it. This is not optional politeness: it changes what needs
   teaching from scratch and what needs a two-minute recap.
4. **What is the programming baseline**, if any practical carries code.

Write the answers into `COURSE-STRUCTURE.md` as you get them. **They are the
design of record from that moment on.**

### 2. Draft ahead of review, and expect the review to be the rate limiter

The division of labour that works: **the instructor decides what is taught and
vouches for every domain claim; the session drafts, structures and builds.** In
practice it is a loop — a skeleton for slides and notes, then correction against
domain knowledge, then figures.

**Draft first and let it be corrected, rather than waiting for complete input.**
And the queue should run with drafting well ahead of review, because the review
loop is slower than the drafting: several rounds per session is normal.

**Material from the instructor arrives through `instructor/incoming/<session>/`,
with a `notes.md`.** Structure that file the same way every time:

1. **what is already verified and needs no check** — this is not padding, it is
   what keeps the question list short and shows exactly where mechanical
   checking stops;
2. the numbered questions that genuinely need a human;
3. figures wanted;
4. length.

Answers come back inline; the next session applies them and appends a placement
log to the same file. **Create the drop folder and its `notes.md` as the last
step of drafting** — do not wait to be asked.

### 3. Sessions before practicals, and practicals in dependency order

Write the lectures first, then the practical units against what the *earlier*
cohort has actually seen. The setup unit — environment, version control, data —
is written **last** even though it is taught **first**: it is the one that
depends on everything else existing.

### 4. Release is a separate gate, and stays closed by default

Content being finished months early and published week by week is exactly what
the allowlist in `_quarto.yml` is for. Nothing is published by writing it.

### The order in one line

> frame → design of record → sessions, drafting ahead of review → practicals in
> dependency order → setup unit last → release week by week

## Project overview

The <MODULE> module: <lecture and practical, audience>. A Quarto site deployed
to **course-<module>.hoelzer.science**, password-protected for enrolled
students.

This is **the course itself**, not the skeleton. Course content lives here;
reusable infrastructure belongs upstream in the template.

## This repository is PRIVATE — and that is load-bearing

Unlike the hub and the template, this repo is private, and things depend on it
staying that way:

- **Solutions and instructor material are excluded at build time, not access
  controlled.** `_quarto.yml` keeps `instructor/**` and `**/solution/**` out of
  `_site/`, and CI fails if either leaks — but the files are still *in the
  repository*. Making this repo public would publish every solution.
- **`_course.yml` holds the real course values** — institution, module code,
  term. That is correct *here*; the public template ships placeholders. Never
  backport that file upstream.
- Exams belong in a **separate** repository, not this one.

The rendered site is protected separately, by HTTP basic auth in
`cloudflare/_worker.js`, which fails closed.

## Relation to the other repositories

```
teaching-hub          public    front door                    teaching.hoelzer.science
teaching-template     public    the skeleton this came from   teaching-template.hoelzer.science (401)
course-<module>       private   this repo                     course-<module>.hoelzer.science (401)
<shared-prerequisite> public    material every module needs   (e.g. linux.hoelzer.science)
```

The `course-` prefix marks a password-protected enrolled module; public sites
take bare labels. Repo name, Pages project name and subdomain label are
identical.

## Syncing with the template

**Cherry-pick only** — never merge or rebase. The histories are unrelated by
construction, so there is no common ancestor.

- **module → template** is the common direction: an infrastructure fix made
  while teaching, backported so future modules inherit it.
- **template → module** for improvements made upstream.

```bash
# from inside the template repo
git remote add course-<module> ~/git/course-<module>
git fetch course-<module>
git log course-<module>/main --oneline
git cherry-pick <sha>
```

**Keep infrastructure commits separate from content commits.** This is what
makes the above work: a commit touching only `scripts/`, `.github/`, `styles/`
or `guide.qmd` cherry-picks cleanly, while one mixing a script fix with three
lecture slides drags course content upstream. See README, "The discipline that
makes this painless", for the full table.

**Never backport:** `_course.yml`, schedule entries, session lists in the render
allowlist, and anything under `lectures/` or `practicals/`.

## Common commands

```bash
pixi install            # environment, incl. bioconda CLI tools
pixi run preview        # live-reloading site (released sessions only)
pixi run draft-preview  # live-reloading, INCLUDING unreleased sessions
pixi run draft          # one-off build of everything, into _draft/
pixi run lint           # ruff over everything
pixi run test           # practical solutions against their tests
pixi run check          # links + output guards
pixi run status         # which sessions are published, which are held back
```

**`pixi run check` is not the CI gate.** `.github/workflows/validate.yml` runs
**`lint`, `test`, `site`, `lms`, `status`, `check-links` and `check-output`**, in
that order, stopping at the first failure. Running only `check` misses a `ruff`
error in a script that never touches the rendered site — which is exactly how a
push fails. Before pushing:

```bash
pixi run lint && pixi run test && pixi run site && pixi run lms && pixi run check
```

**To look at a session that is not released yet, use `pixi run draft-preview`.**
Do *not* reach for `quarto render lectures/NN-name/slides.qmd`: naming a
held-back file makes Quarto render it as a **standalone document**, not as part
of the project, so project-root-absolute includes such as
`{{< include /shared/partials/… >}}` fail outright and `_course.yml` metadata
never applies. `_draft/` is gitignored and cannot be published, so drafting is
safe — but `pixi run status` remains the only answer to what is actually live.

## Development workflow

1. Edit, `pixi run preview`, then the full pre-push gate above — not `check`
   alone.
2. Push to `main`: CI validates, then deploys.
3. **Releasing a session is a separate gate** from deploying. Only sessions
   listed in `project.render` in `_quarto.yml` exist on the site at all; adding
   one to the allowlist is what publishes it.

   **It is three edits, though, and only the first is called release:** the
   allowlist, the **navbar** in the same file, and the link in `schedule.qmd`.
   Miss the last two and the session is live and reachable only by guessing its
   URL — with nothing failing, because `check-links.sh` rejects links that are
   *broken* and never notices links that are *absent*. `pixi run status` has a
   **REACHABLE** column for exactly this.

   The **first practical** is the awkward one: the Practicals menu is removed
   from the navbar while it would be empty, because Quarto rejects a menu with
   no entries, so releasing P01 means re-creating the whole menu rather than
   adding one line.

## Authoring content

Distilled from one module taught end to end. Everything here is a rule that cost
something to learn; the module-specific instances live in that module's own
`CLAUDE.md`.

**Every `.qmd` that executes Python needs `jupyter: python3` in its front
matter.** Quarto resolves the kernel itself and does not reliably prefer the
project environment — it can pick a kernelspec belonging to an unrelated
virtualenv, and every document importing a third-party package then dies with
`ModuleNotFoundError`. The pin **does not cascade from `_quarto.yml`**, and
`QUARTO_PYTHON` does not fix it either: that governs how Quarto *finds* Jupyter,
not which kernelspec it picks.

**The symptom is much worse than the cause.** The render **aborts** at the first
failing document, so the output is left **partial** — and `check-links.sh` then
reports "broken" links that are really files never built, which reads as a
content error. **If a link check reports far fewer links than usual, suspect an
aborted render before suspecting the content.** Know your normal count.

**`_freeze/` caches rendered *prose*, not just code output, and can serve a stale
page.** A one-paragraph edit can be present in the source, absent from the
output, and **stay absent across full rebuilds**, while other edits to the same
file in the same minute render fine. The cached text is in
`_freeze/<doc>/execute-results/html.json` under `result.markdown` — note that a
top-level `markdown` key also exists and is always empty, which will mislead a
check written against it. `rm -rf _freeze` fixes it. **A build reporting success
does not prove your edit is in the output: after editing a `.qmd`, grep the
rendered HTML for a distinctive phrase you just wrote.**

**An executed block can read a data file from the session's own `data/`
directory by relative path.** Quarto executes with the *document's* directory as
the working directory. Prefer that to pasting data into the document: a literal
copied from a database is a classic silent error, and a file cannot disagree
with itself.

### Slides, notes and the shape of a session

- **Slides are sparse, notes are complete.** Separate files sharing
  `shared/partials/` — do not generate one from the other.
- **They differ in depth, not in order.** The two share a spine: a section that
  moves in one moves in the other.
- **A slide should contain at most one `::: {.notes}` block.** Two is almost
  always a bad split — a slide inserted by anchoring on a line that merely
  *looks* like the end of one, orphaning everything after it. One `grep` across
  `lectures/*/slides.qmd` finds every case.
- **Everything a slide names must already exist at that point in the deck.**
  Check forward references *within* a session, not only between sessions. Moving
  content is when this bites, because the prose was correct where it used to be.
- **Budget length while drafting, not afterwards.** A 90-minute slot holds
  roughly **30–35 content slides** — about 2 min for an ordinary slide, 3–4 for
  one carrying a worked example, plus any video and the polls. **Aim at ~25 while
  figures are still to come**: an incoming drop reliably adds slides, and it is
  much cheaper to leave room than to cut later. Count with `grep -c '^## '`.
- **A `.center` figure slide has a text budget, and overflow is silent.** An
  image at `height="480"` leaves room for a short title and *one* line of body
  text; two lines need the image at ~430 or less. Speaker notes cost nothing.
  Overflow is a browser-layout question and cannot be checked from a terminal.
- **A session that is too long cannot always be split.** The question to ask
  first is not "where do I cut this in half" but **"does another session already
  want this?"**

### Things that rot

- **Student-facing text must survive a semester rollover.** No group counts, no
  week numbers, no dates hard-coded in a `.qmd` — those belong in `_course.yml`
  or in the LMS. Write "the practical may run in more than one group depending
  on numbers", not "two groups of twelve".
- **A session whose CONTENT varies every year should have a page and nothing
  else** — an `index.qmd`, no slides, no notes. Its content changes annually; its
  *purpose* does not, and only the purpose is written down. The single varying
  line lives in `_course.yml`.
- **A convention that lives in two files decays silently**, because nothing
  checks that the two agree. Changing or adding one means touching both, and
  `grep -c` across the session set is the check. **The third place this happens
  is the design-of-record document**, and it is the easiest to miss because
  nothing in a session points back at it.
- **A claim about another session is as checkable as an accession — so grep it,
  never recall it.** This category *looks* unverifiable but is not: the answer is
  in the repository.
- **Renaming a shared vocabulary item has a blast radius that includes prose
  mirrors of it.** Grep the old label across every session directory *before*
  renaming. And **when a naming choice has a reason, write the reason next to the
  name** — it is what stops the choice being re-litigated.
- **A page that names a path is claiming the reader has that path, and no gate
  checks it.** Every gate checks the rendered site; an instruction like
  `cd exercises/NN/starter` is a claim about the *student's machine*. Ask "where
  does the reader get this from?"
- **When a step becomes automatic, the sentence that asked for it is part of the
  change.** Obsolete instructions survive every check, because nothing connects a
  change in process to the prose describing the old process.

### Figures

- **Every figure needs a caption *and* a `fig-alt`. Exception, and it is
  silent:** Quarto drops `fig-alt` on a ` ```{mermaid} ` block — the caption
  renders, the alt text never reaches the output, and nothing warns you. Give
  mermaid diagrams a text equivalent in visible prose instead. Do not reach for a
  visually-hidden span: Bootstrap's `.visually-hidden` exists on the website but
  not in revealjs, and partials are included in both.
- **Figures live per session.** One moves to `shared/figures/` only when it
  genuinely appears in more than one — the same rule as `shared/partials/`, where
  *shared* means *reused by design* rather than *put somewhere central*.
  **Promoting a GENERATED figure means repointing its generator**, or the next
  routine regeneration silently recreates the per-session copy and the two drift.
- **Rerunning a figure generator produces a large but empty diff**, because
  matplotlib stamps a fresh date and randomises every element id. **Do not
  regenerate unless a figure actually changed**, and when several were rebuilt
  together, find out which: rasterise both versions and `magick compare`. The
  pixel *count* is misleading — new element ids shift anti-aliasing everywhere —
  so the difference image is what settles it. Revert the ones that only churned.
- **When a figure's claim depends on which inputs were chosen, assert the claim
  in the generator**, so a later change to the input set fails loudly instead of
  quietly contradicting the slide. **Write computed numbers into the label rather
  than typing them**, for the same reason.
- **A figure that restates a canonical source should PARSE it, not repeat it.**
- **Incoming images get optimised on placement**, to WebP at ≤2560 px:
  `magick <in> -resize 2560x\> -strip -quality 88 <out>.webp`. But **an SVG is
  not automatically the light option and the rule must not be applied blindly**:
  check what is *inside* the file with `grep -c base64` and
  `gzip -9 -c f.svg | wc -c`. A vector SVG full of `<text>` gzips small and
  rasterising costs crispness for nothing; an SVG that is a wrapper around
  embedded PNGs rasterises to less than half its gzipped size. **Run the
  comparison at equal resolution, or it lies.**
- **A `.pptx` is a zip**, so an incoming deck needs no PowerPoint:
  `ppt/media/` has the images, `ppt/slides/slideN.xml` the text,
  `ppt/notesSlides/` the **speaker notes**, and `ppt/slides/_rels/` maps each
  image to its slide. Worth doing properly rather than asking for exports: a
  figure arrives *with the argument it was serving*, and the speaker notes say
  *why* it is there, which is the part that cannot be reconstructed.
- **Your own figure is not automatically better than a borrowed one — look at it
  before committing to it.** Generating one is cheap; shipping a bad one is not.
- **Attribution is at the point of use, best effort** — a source line in the
  caption when the source is known. **But a licence that names a condition
  overrides "best effort"**: CC BY and CC BY-SA *require* attribution. And the
  relaxation is about *bookkeeping*, not about what may be reproduced — it holds
  only while the site is behind auth and the repository is private.

### Partials

- **Maintainer comments inside partials reach the rendered HTML.** Pandoc passes
  `<!-- -->` straight through, so anything in a partial's header ships in the
  page source. Nothing sensitive belongs there. **Worse than it looks:** a Quarto
  shortcode written *inside* such a comment is still **expanded** before the
  comment is passed through — so documenting a metadata field in
  `{{< meta … >}}` syntax prints its actual value into the visible page source.
  In comments, name fields in prose only.
- **Use project-root-absolute include paths in partials** (`/shared/…`). Quarto
  resolves `{{< include >}}` relative to the *including* document, so a relative
  path breaks as soon as a second document at a different depth includes it.

### Verification

- **Prefer content whose correctness is testable.** Where a claim can be turned
  into a runnable example, do that. **The strongest form of this is to execute
  the page**: a sibling project extracts every `bash` block from its pages *and
  its slide deck* and runs them in order, in one shell, in a scratch directory —
  and it caught two real bugs that reading could not, a GNU/BSD command
  incompatibility and a CI-only failure. Prose about what a tool does cannot be
  checked mechanically; a command can.
  - **Budget the exclusions per page, not globally.** Some pages genuinely
    cannot run in CI — one that installs software, say. A single flat cap forces
    either a dishonest page or a meaningless limit; a per-page budget with a
    comment saying what on *that* page cannot execute makes raising a number a
    decision to justify in the same commit.
  - **Say what the test tests, and let the page imply no more.** Output blocks
    are usually *not* verified: an exact comparison fails on correct-but-machine-
    specific things — home paths, column widths, locale sort order — and
    loosening it until it passes leaves an assertion that asserts nothing.
  - **A block passing in isolation does not prove it composes with what follows
    it.** If blocks share a shell, a `cd` that never returns silently moves every
    later relative path. The general form: **an example added to the middle of a
    sequence is a change to everything after it.**
- **A development machine tolerating something is not evidence that CI will.**
  Apple's git silently invents an identity when `user.name` is unset and only
  warns; Ubuntu's hard-fails. An example passed locally and failed on its first
  real CI run for exactly that. Reproduce the isolated conditions locally
  (`env -i HOME=… bash -c '…'`) before trusting a fix.
- **Identifiers are checkable, so check them rather than recalling them.** One
  `curl` against a public API settles what memory only guesses.
- **An external resource that reissues its records needs a PINNED version** if
  you ship numbers computed from it.
- **An executed block is evidence about its own input, and nothing more.** A
  generalisation written beside a green code cell borrows authority from the
  computation next to it and is an ordinary unverifiable claim. State what the
  computation computed; flag anything beyond it.
- **A filter's null result is evidence about the filter as much as about the
  data.** Plot it before believing a summary statistic about it — a picture costs
  minutes.
- **When a second tool is cheap, run it as an independent check** rather than for
  decoration. Two instruments agreeing is worth far more than one measured
  number, and the disagreement is where the interesting part is.
- **A tool that installs is not a tool that works, and package metadata lies.**
  Establish availability by **solving, per platform** — never by reading a
  `platforms` field, which reflects only the newest version's builds — and **run
  the tool end to end before relying on it**. `--version` proves nothing, and the
  interesting failures appear minutes into a real run.
- **The version a tool reports is not necessarily the version you installed.**
  When it matters, read it from the lock file, not from `--version`.
- **Anything about an interactive web interface cannot be checked from a
  terminal** and must be tested by hand before it ships. When a claim cannot be
  executed, mark it as needing a human test rather than writing it as fact.

## How a practical unit is built

The model that survived a semester. `practicals/01-alignment/` is the worked
example; its comments say why each piece is shaped the way it is.

**Two different things get called "group". Name them apart**, in the material and
in conversation:

- a **cohort** — the students attending on alternating weeks. A *scheduling*
  construct.
- a **team** — the two or three who work together on their own data. The
  *working* unit.

**Teams of two, three by exception.** The university's recommendation for a
computer-room course, and the reason is the machine: at one keyboard, three means
one person watching.

### Cohort-independence: three rules

If the practical runs twice on alternating weeks, everything must hold for both:

1. **Never reference time, only session numbers.** No "last week's lecture" — it
   is true for one cohort and false for the other. Write "L4 covered this".
2. **State the prerequisites explicitly** in each unit, against the state of the
   **earlier** cohort — the minimum, never the average.
3. **No shared mutable state.** Pre-staged material is read-only and installed
   once; everything a team writes lives in the team's own repository. Then
   "runs twice" needs no reset ritual.

Per-team data is not only for variety: it is what makes running the same session
twice **safe**, because the later cohort cannot read the earlier one's answers.

### Shape of a session

**Five slides, then the terminal** — where we are, today's question in the case
study's terms, what you will produce, what this assumes, logistics. About five
minutes. The rest of the introduction is a **live demonstration**, not slides.

### The three layers

Every unit has the same three, and this is what keeps a tool-driven practical
anchored to something verifiable:

| Layer | What it is | Where it is checked |
|---|---|---|
| **Do** | run the tools on the data | the artefacts exist |
| **Compute** | a small programming task | **`pixi run test`** |
| **Interrogate** | a question whose answer needs *looking* | the write-up |

- **The Compute layer is started in the session and finished outside it**, said
  through `shared/partials/compute-layer.qmd` — identical wording in every unit,
  because students meet it once per session and it must read as one rule. **The
  heading carries the timing too**, because a student reading top to bottom reads
  headings, not callouts.
- **Do not reorder Compute and Interrogate to put the overflowing part last.** It
  is tempting, and the data dependency usually forbids it: Interrogate is
  routinely answered with numbers Compute produces. Check before assuming either
  way. What Interrogate must get *in the session* is being **read** — it says what
  to look at while the data is still on screen.
- **The Interrogate layer needs obstacles to exist.** If obstacles are an assessed
  part of the write-up, a unit that runs smoothly gives students nothing to
  report. **Design at least one place per unit where the obvious approach is
  ambiguous, fails, or depends on a parameter choice.**
- **Every unit ends with tools and further reading** — the manual or repository
  **first**, the paper second. Manual first is the whole point: *always check the
  tool's manual* is the transferable habit. Say when a tool has no paper. Use
  DOIs, not journal URLs — `check-links.sh` verifies only *local* links, so a
  rotted URL is not caught by CI.
- **Name the artefacts each unit expects committed**, with full paths, so "look at
  the repository" has something concrete to look at.

### State the assessment in the FIRST session, and build it into the repository

Two of the things typically assessed **cannot be reconstructed at the end**: a
record of obstacles (nobody remembers in January which parameter they guessed in
November) and a screenshot of something interesting (recovering it means
re-running the analysis). Telling students in the closing session what they should
have been collecting since the first is not an assessment, it is a trap.

**Implement it structurally, not as an instruction.** Prose in the first session
is forgotten by the third; a file with empty headings sitting in the repository is
not. See `instructor/team-repos/README.md`.

## Known constraints

- **Verify auth by hand after any hosting change**, on a **direct asset URL that
  actually exists** — a *released* session's `slides.html`, not a held-back one —
  and not just the landing page. If the landing page prompts but the asset loads,
  the worker is not intercepting assets and the course is effectively public.
  Check the `*.pages.dev` fallback URL too. A **401 means the worker read the
  credentials**; a 503 means they are unset and it is failing closed.
- **That check proves auth, and nothing else.** The worker fails closed, so it
  returns 401 for *every* path, including ones that do not exist. A 401 on a
  held-back session therefore says nothing about whether it was published — it is
  what you would see either way. To check what was actually deployed, inspect the
  bytes CI deployed: `gh run download <run-id>` and list the result.
- `COURSE_USER` / `COURSE_PASSWORD` are **Cloudflare Pages** environment
  variables read by the worker at runtime — not GitHub secrets. Putting them in
  the wrong place is the most common setup mistake. Preview deployments use a
  separate environment; if unset, previews return 503, the safe default.
- GitHub side: secrets `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`; variable
  `CLOUDFLARE_PROJECT_NAME` = `course-<module>`.
- **bioconda has no Windows builds.** Students on Windows need WSL2; set it up
  together in the first practical.
- `pixi run lms` prints an EXCEPTION about `slides.html` not being
  self-contained. This is **expected** (README gotcha #4: chalkboard is
  incompatible with `embed-resources`), exit code is 0, and CI passes.
- README's "Gotchas discovered while building this" is not optional reading —
  most of those failures are silent, including one where linking to a held-back
  session serves students the raw `.qmd`.

## Audience

**Replace this section with the real one.** It is the single thing that most
changes how material is written, and a wrong guess here is expensive — the
placeholder below is a shape, not an answer.

Say who the students are, at what level, and in which programme. Then two things
that are worth establishing rather than assuming:

- **What they were already taught.** Find the programme's module catalogue and
  write the mapping down. Students routinely say they do not know something they
  were in fact taught, so **naming the module is worth doing** — *"you met this
  in <module>"* both places the material and tells them they already own it.
  Name modules by **title, never by module code**: titles survive catalogue
  revisions, and a stale code on a slide is exactly the kind of
  confidently-wrong detail that costs credibility.
  **A cross-reference shortens a recap; it never replaces one.** Students forget
  fast, so the recap stays and gets more compact.
- **What the programming baseline actually is**, if any practical carries a
  coding task. This sets the difficulty of everything you write, so take it from
  the catalogue rather than from impressions.

**Assume no command line experience** unless you have evidence otherwise. A
Linux/bash crash course is a prerequisite for the practicals; it lives in its own
public repository and is **linked**, not copied — see "Relation to the other
repositories" above.

**Concrete examples from the students' own field land better than abstract
`foo`/`bar`.**

**If the course is taught in one language and written in another, say so and be
consistent.** Glossing each key term in the other language on first use, in the
*notes* only, keeps the slides clean and means students never meet a term in the
exam that they have only ever seen in the other language.

## Things future sessions should always know

- Read `README.md`, then `COURSE-STRUCTURE.md`, then `NEXT.md`, then the newest
  file in `docs/sessions/`. If the first three are still templates, start at
  "Starting a new course" above. **Then check `gh issue list`** for open
  `retrospective`-labelled issues — the instructor files one per lecture or
  practical, right after teaching it, from the
  `.github/ISSUE_TEMPLATE/session-retrospective.md` template. These are
  concrete, closeable, session-specific action items in a way `NEXT.md` prose
  is not: pick one up the way you would a bug report, fix it, and close the
  issue rather than folding it back into `NEXT.md`.
- **The scaffolds:** `COURSE-STRUCTURE.template.md`, `NEXT.template.md` and
  `docs/SESSION-TEMPLATE.md`. Copy, do not read-and-improvise — the headings are
  the parts that were learned.
- **Keep a design-of-record document** — the session plan, the cross-reference
  against the official module description, and the reasoning behind every
  deviation. Change it *first* when the plan changes. It is also the third place
  a two-file convention decays, so grep it for a session's own number before
  calling that session finished.
- `NEXT.md` and `docs/sessions/` are gitignored, inherited from the template's
  convention. Here that is habit rather than necessity, since this repo is
  private — but keep it, so one rule holds across all the teaching repos.
- `gh` is authenticated as `hoelzer`; `wrangler` via OAuth. Cloudflare account
  ID `6398bee0e2141168cd3fccf8cfbfe6ee`.
