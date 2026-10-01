# Transcriber agent prompt template

Fill in every `{...}` and send one copy per page chunk to a `general-purpose` agent. Launch all chunks in a single message so they run in parallel.

The `{KNOWN_ISSUES}` block is the most valuable part. From your skim, list what you already spotted on those pages:
- suspected slips,
- blanks,
- sketches,
- faint margin notes.

Tell the agent to verify each one rather than trust it.

---

You are transcribing handwritten {SUBJECT} notes into LaTeX. Your pages: {PAGE_LIST}.

Images (already contrast-boosted):
- Full page: {PAGES_DIR}/p-NN.png
- Half crops for detail (top/bottom 55%, overlapping): {CROPS_DIR}/p-NN-top.png and p-NN-bot.png

For EACH page, Read the full page AND both crops. Handwriting is small, and faint pencil margin notes are easy to miss in the full view. Every line, arrow, bracket annotation and side note must end up in the output.

{SKIPPED_PAGES_LINE}  (e.g. "Page 15 is confirmed illegible: put only `% p.15: illegible in source, skipped` there, with no \srcpage.")

Write a BODY-ONLY fragment (no preamble, no \begin{document}) to {FRAG_PATH}. Don't compile and don't create other files.

Context: {CONTEXT_FROM_PREVIOUS_CHUNK}, e.g. "the previous chunk ends inside \section{Fourier series}, so continue at \subsection level."

CONVENTIONS (these macros and environments exist in the preamble):
{CONVENTIONS}

Build `{CONVENTIONS}` from the interview answers. The standard lines are:
- Environments: theorem, definition, example, remark. Use \section/\subsection following the notes' own headings.
- Put `\srcpage{N}` at the start of each page's content. It goes in running text: never inside a `\section{}` argument, and never inside align*/equation*. If a page starts with a display, add a two- or three-word lead-in line to hang it on.
- Math slips: write the correct version, then `\corr{notes had ...}`. Inside math, wrap it as `\text{\corr{...}}`.
- Unfinished items: fill them in with `\added{...}`, again wrapped in `\text{}` inside math. Blanks the notes mean to be blank stay as written.
- Side notes: an inline parenthetical, or a short `\textit{Note:} ...` line right after the related line.
- Crossed-out content: drop it.
- Notation: keep it exactly as written.
- Sketches: small TikZ figures (width about 5 cm, in a center env). Use plain `\draw plot`, no exotic libraries.
- Tables: use tabular. A correction inside a table cell goes on its own line right below the table, naming the row. Tiny margin sketches beside rows become inline mini TikZ in an extra column.
- A page that starts inside a theorem or example: put `\srcpage{N}` on the first text line inside that environment.
- Use align*/equation* for displays, and one-line `%` comments only.

WHAT COUNTS AS A SLIP. Only flag genuine mathematical errors: a wrong sign, a wrong factor or exponent, a wrong result, a wrong variable, a missing term that changes the value. Verify each one by computing it yourself.

Do NOT use `\corr` for any of these:
- the notes relabelling something (e.g. "f̂(ω)·F(ω)" meaning "f̂, i.e. F");
- a standard derivation device (e.g. a zero-extension before letting L→∞);
- a convention choice (a normalisation factor the notes say they are ignoring);
- informal but correct phrasing.

Those get a short `\textit{Note:}` at most. Over-flagging buries the real corrections the user needs to see.

Grey areas, settled:
- **A normalisation factor** dropped in one line of a derivation that otherwise carries it is a slip (`\corr`). One the notes deliberately omit ("scaling factor ignored") gets a Note.
- **A wrong constant inside a stated convention** is a slip. For example, "general form $e^{iB\omega t}$, B=1 is our form", when the notes' form is $e^{-i\omega t}$.
- **A false prose claim about the math** is a slip. For example, "from sim: does not converge" for a series that converges. Keep the original wording visible in the `\corr`.
- **Indexing differences** are a Note, not a slip. For example, a coefficient written for odd frequencies 2k+1 rather than for k.

Also:
- Ignore show-through: faint mirrored text bleeding from the back of the page.
- For overwritten characters (e.g. "1∓iω"), choose the stroke that's consistent with the surrounding math and list it under uncertain readings.

KNOWN ISSUES TO VERIFY (from the coordinator's skim; don't trust them blindly):
{KNOWN_ISSUES}

When done, reply with a short summary:
- pages covered;
- every `\corr` and `\added`, one line each;
- every uncertain reading, quoting the ambiguous bit and your chosen reading.
