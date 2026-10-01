# Interview question bank

Ask **all** of these every run, in rounds of up to 4 via AskUserQuestion. The user wants the full interview each time, so don't collapse it into a single "use defaults?" question.

Make every question concrete by quoting real items from *these* notes, found during the skim. Examples: "p3 writes Γ(−1/2), which should be Γ(1/2)", "p16 leaves ℱ[Λ] = blank", "p7 has a sketch of three curves". A generic question gets a generic answer.

Tag the option the user picked last time with "(last time)". Only add "(Recommended)" when you have a real reason specific to these notes.

## Round 1: Content fidelity
1. **Math slips.** Options:
   - Fix + flag *(last time)*
   - Verbatim
   - Verbatim + flag
   - Silently fix
2. **Hand sketches.** Options:
   - Simple TikZ/pgfplots *(last time)*
   - Placeholder box
   - One-line description
   - Omit
3. **Side/margin notes.** Options:
   - Inline remark *(last time)*
   - `\marginpar`
   - Footnotes
   - Drop minor ones
4. **Minimal level.** Options:
   - article + ams + amsthm envs *(last time)*
   - Bare article + amsmath
   - Body only (no preamble)

## Round 2: Edge cases
5. **Illegible/blurred pages.** Only ask if the skim found any; name the pages, and say whether each looks motion-blurred (unrecoverable) or just faint (an enhance may rescue it). Options:
   - Try enhance, else skip with % comment *(last time)*
   - Skip entirely
   - Visible placeholder
6. **Unfinished items** (blanks, trailing expressions). Quote them. Options:
   - Fill in + flag *(last time)*
   - Leave as-is
   - Leave + visible TODO

   Point out any blank that is *intentionally* blank, e.g. "( )(−1,−1) — not possible". Those stay as written.
7. **Crossed-out content.** Options:
   - Drop *(last time)*
   - Keep with `\sout`
8. **Notation inconsistencies** (e.g. α_k vs a_k). Options:
   - Keep as written *(last time)*
   - Normalize

## Round 3: Output & process
9. **Output location/name.** Options:
   - `<input dir>/<name>.tex` + `<input dir>/pages/` images *(last time)*
   - .tex there, images in scratchpad

   Crops always go in the scratchpad regardless.
10. **Pages per subagent.** State the page count and the proposed split.
    - Last time: 23 pages, 4 agents at about 5–6 pages each, taking about 5 min.
    - Offer: about 5 pages/agent; about 8 pages/agent (fewer agents); or no subagents (sequential, most consistent style).
11. **Flag style for corrections/additions.** Options:
    - Inline italic, no colour *(last time — user said "mark it inline but no colour")*
    - Footnote
    - `%` comment only
    - Coloured text
12. **Source page markers.** Options:
    - Footnote at each page start *(last time)*
    - `%` comments
    - None

## Round 4: Build
13. **Compile?** tectonic is installed at /opt/homebrew/bin/tectonic. Options:
    - Don't compile *(last time)*
    - Compile with tectonic and fix errors until it builds
14. **Title/author** for `\title`. Offer the filename-derived default, or "no title".

If an answer is free text ("Other"), read it literally and apply exactly what it says. Past examples:
- "mark it inline but no colour"
- "source page marker in the output but as a footnote"
