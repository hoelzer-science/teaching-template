# Course design — <Module Name> (<MODULE.CODE>)

> **Copy this to `COURSE-STRUCTURE.md` and fill it in before writing any
> session.** It is the **design of record**: the plan, the cross-reference
> against the official module description, and *the reasoning behind every
> deviation*. The reasoning is the part that earns its keep — without it, every
> decision gets re-litigated a month later by someone who cannot remember why.
>
> **Change this file first when the plan changes**, before touching a session.
> And note it is the third place a two-file convention decays, because nothing
> in a session points back at it: before calling a session finished, grep this
> file for that session's own number and check what it was supposed to carry.

## How binding the module description is

Establish this early, in writing, because it governs everything below. Typically:

- **The `Qualifikationsziele` / learning outcomes are binding** — accreditation
  and exam fairness rest on them.
- **The formal frame is binding** — ECTS, contact hours, the examination format.
- **The content list usually is not.** It is a set of examples, not a checklist,
  and obsolete content can be dropped outright.

**Check anything you propose to drop against the outcomes first.** And if the
flexibility was granted verbally, get it in writing — otherwise the audit trail
for the whole design ends at "somebody said so".

## Philosophy

Two or three sentences on what this course is *for* and what makes it different
from a textbook reading of the same topics. Everything below should be traceable
to this.

## Hard constraints

The things no session may violate. Typically:

- **The examination format**, in detail — length, language, and *what it
  actually tests*. If it tests executing a procedure by hand, then worked
  examples must be sized like exam questions rather than like illustrations:
  short real inputs, arithmetic a student can reproduce with a pen. **Any
  session that introduces a procedure needs at least one such example.**
- **The language split**, if written material and teaching are in different
  languages. Students must never meet a term in the exam that they have only
  seen in the other language.
- **Contact hours**, and what a "session" actually means in the timetable.

## Cross-reference against the module description

A table: each item of the official content list, where it is taught, or why it
is not. **Deviations get a paragraph each**, not a row.

## What students already know

Find the programme's module catalogue and map it, session by session. Two rules
govern how it is used:

- **A cross-reference shortens a recap; it never replaces one.** Students forget
  fast, so the recap stays and gets more compact. Nothing is deleted merely
  because the catalogue lists it.
- **Name modules by title, never by code.** Titles survive catalogue revisions;
  a stale code on a slide is a confidently-wrong detail that costs credibility.

Three placements, each with a different job: a *"what this session assumes"*
block on the **index page** (the canonical list), one line on the **slides** so
it can be pointed at live, and inline prose in the **notes** at the point of use.

## Session plan

A table of sessions, and for each: what it covers, what it assumes, and what
depends on it. Then a section per session with the reasoning.

**Two things to record per session that are easy to leave out:**

- **What it deliberately does NOT cover**, and where that went instead. A session
  that is too long usually cannot be split into two — the question to ask first
  is *"does another session already want this?"*
- **Whether any history it teaches earns its place.** The test: *does this
  history explain something students still meet?* If not, drop it rather than
  teach it as a curiosity.

## Practical

The theme, the shape of a unit, and what varies per team. See
`CLAUDE-course.md`, "How a practical unit is built", for the model itself — this
section is where *this* course's instance of it is decided: the case study, the
per-team data, the tools, and the timetable against the lecture.

## Relationship to other modules

What this course feeds, and what feeds it. If it advertises a follow-on module,
decide **where** that is said and record it here — a convention that lives only
in the plan decays exactly like one that lives in two files.

## Open items

**Nothing below should be written into teaching material until resolved.** Move
items out of this section as they are settled, with the answer and the date.
