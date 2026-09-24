# Style guide for student-facing text

**Who reads this material:** Bachelor students who speak German as their first
language and read English as a second language. They read the material in
English, but they are taught and examined in German. They must understand the
biology and the methods. They must not also have to decode the English.

**What this guide covers:** lecture notes, slides, session pages, practicals and
course pages. Speaker notes get a light pass only (see *Speaker notes* below).
Maintainer comments, scripts and `instructor/` files are not covered.

The base is **George Orwell's six rules** (*Politics and the English Language*,
1946). Where Orwell and the other rules disagree, Orwell wins. Some rules from
**ASD-STE100 Simplified Technical English** are added where they help. STE was
made for maintenance manuals, so apply it strictly to instructions and more
loosely to explanations.

---

## 1. Orwell's six rules, and what they mean here

1. **Never use a metaphor, simile or other figure of speech that you are used
   to seeing in print.**
   Say the plain thing. A second-language reader takes an idiom literally.

   | Not | But |
   |---|---|
   | this clause *does the heavy lifting* | this clause is the important part |
   | the method *earns its keep* | the method is useful because … |
   | we *pick this up* in Lecture 5 | Lecture 5 explains this |
   | a *red flag* | a warning sign, or: this suggests an error |

   A comparison that *explains* something is allowed ("a FASTQ file is like a
   FASTA file with a quality line added"). A figure of speech that only
   decorates is not.

2. **Never use a long word where a short one will do.**

   | Not | But |
   |---|---|
   | utilise | use |
   | approximately | about |
   | subsequently | then, later |
   | in order to | to |
   | contrived | invented, artificial |
   | a curiosity | interesting but unimportant |

3. **If it is possible to cut a word out, always cut it out.**
   Cut words that carry no meaning. **Add words that do carry meaning.** These
   do not conflict:

   - *Cut:* intensifiers and fillers — *actually, really, genuinely,
     deliberately, exactly, precisely, simply, just, quite, clearly, of course,
     obviously, worth noting that*. If a sentence reads the same without the
     word, remove it.
   - *Add:* a definition the reader does not have yet, the subject of a
     sentence, a step in an argument that was skipped, or the name of the thing
     that *this* or *it* refers to. A short sentence that the reader cannot
     follow is not efficient — it moves the work to the reader.

4. **Never use the passive where you can use the active.**
   Say who does what. *"The reads are mapped to the reference"* → *"The mapper
   places each read on the reference."* Passive is fine when the actor is
   unknown or unimportant (*"The genome was sequenced in 2012"*).

5. **Never use a foreign phrase, a scientific word or a jargon word if you can
   think of an everyday English equivalent.**
   **This rule has one exception, and it is important: the technical terms of
   the subject stay.** Students must learn *alignment*, *coverage*, *contig*,
   *reverse complement* — they are the content, they appear in the exam, and
   they appear in every tool. Keep them, define them on first use, and give the
   German term (see section 3). What goes is jargon that is *not* the subject:
   *i.e.*, *e.g.*, *cf.*, *vice versa*, *a priori*, *per se*, and
   computer-science or academic slang the reader was never taught.

6. **Break any of these rules sooner than say anything outright barbarous.**
   A sentence that follows every rule and reads badly is still bad. Rewrite it.

## 2. From Simplified Technical English

Apply these strictly in practicals and instructions, and as a target in
explanations.

- **One sentence, one idea. One instruction, one sentence.**
  Target length: **at most 20 words** for an instruction, **at most 25 words**
  for an explanation. Longer is allowed when a sentence cannot be split without
  losing its meaning — but then check it again.
- **Give instructions in the imperative.** *"Run `fastp`."*, not *"You will
  now want to run `fastp`."* or *"`fastp` should be run."*
- **Put a condition before the instruction.** *"If the command fails, run it
  again."*, not *"Run it again if the command fails."* The reader then knows
  whether the instruction applies before reading it.
- **Use one word for one meaning, and one meaning for one word.** If a thing is
  a *read* in one paragraph, do not call it a *fragment* in the next. Choose the
  term, then keep it.
- **Prefer a single verb to a phrasal verb.** *find out* → *find*; *set up* →
  *install* or *configure*; *carry on* → *continue*; *come up* → *appear*.
  Phrasal verbs have many meanings, and German readers often learn only one of
  them.
- **Keep articles and small words.** *"Open the file"*, not *"Open file"*. STE
  keeps *the*, *a* and *that* because they make the grammar clear.
- **Use a numbered list for steps that happen in order**, and a bullet list for
  items that do not.
- **Write a warning before the step it applies to**, not after it.

## 3. Rules specific to teaching

- **Define every technical term where it first appears**, in the same sentence
  or the next one. After that, use the term without explanation.
- **Give the German term in parentheses on first use**, in the notes:
  *sequencing (dt. Sequenzierung)*. Slides stay without these.
- **Refer to other sessions by name and number**, not by position: *"Lecture 4
  (Quality control)"*, not *"as we saw above"* or *"later"*.
- **Do not refer back with a pronoun across a paragraph break.** Repeat the
  noun.
- **A slide may be in telegraphic style** — fragments and short phrases are
  normal there. It must still be clear to a student who reads it alone a week
  later.
- **Say what a number means.** *"Q30"* → *"Q30, which means one wrong base in
  1,000"*.
- **No rhetorical questions that the text does not answer**, and no irony. A
  second-language reader may take them literally.

## 4. Words and phrases to avoid

This list is not complete. Use it as a check, not as a replacement for reading
the sentence.

| Avoid | Why | Use instead |
|---|---|---|
| *genuinely, actually, really, deliberately, exactly, precisely* | intensifier; usually carries no meaning | remove it |
| *worth* + noun or *-ing* (*worth knowing*, *worth five minutes*) | idiom | *important*, *useful*, or say why |
| *i.e., e.g., cf., vs.* | Latin abbreviations | *that is*, *for example*, *compare*, *against* |
| *the room* (for the students) | idiom | *the class*, *you* |
| *land, sink in* (for understanding) | metaphor | *be understood* |
| *hence, thus, thereby, whereby* | formal and old | *so*, *therefore*, *in this way* |
| *the former / the latter* | the reader must look back | repeat the noun |
| *it is not that X — it is that Y* | the reader meets the wrong idea first | say Y |
| *quietly, silently* (for software) | personifies the program | *without a warning*, *without an error message* |
| double negatives (*not uncommon*) | hard to parse | *common*, *frequent* |

## 5. What a language edit must not change

A language edit changes **how** something is said, never **what** is said.

- **Keep, unchanged:** technical terms, German glosses, numbers, units,
  commands, code, file names, accessions, citations, figure files, `fig-alt`
  meaning, and headings that other pages link to (heading text makes the anchor).
- **Keep the order of sections.** Slides and notes share the same order; an edit
  in one must not break that.
- **Keep the marker "do this one by hand"** and every statement about what is
  or is not examinable.
- **If a simpler sentence would say something slightly different, do not
  choose.** Mark it for the lecturer to decide. Rewording is exactly the place
  where a correct claim can become a wrong one.

## Speaker notes

Speaker notes are read only by the lecturer, but they are in the page source.
Give them a light pass: fix idioms and sentences that are hard to read, and do
not rewrite the rest.

## Checking a text

Read each sentence and ask:

1. Could a student who learned English at school understand it on the first
   reading?
2. Can I remove a word without losing meaning? Then remove it.
3. Is a word missing that the reader needs? Then add it.
4. Is it active, and is it clear who does what?
5. Is every technical term defined, here or earlier?
