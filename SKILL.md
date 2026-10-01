---
name: handwritten-to-latex
description: Faithfully transcribe handwritten notes (a scanned/photographed PDF, or a folder of notebook photos incl. HEIC) into minimal, clean LaTeX, page by page, without missing content, with math slips fixed and flagged, sketches redrawn in TikZ, and source-page markers. Use this whenever the user wants handwritten, scanned or photographed lecture/class/notebook notes converted, typed up, digitized or transcribed into LaTeX/.tex, even if they just say "convert my notes pdf to latex", "type up these notebook pages" or drop a notes PDF asking for a latex version. Not for summaries, cheat sheets or formula sheets built from slides/books (use stem-notes for that): this skill transcribes what's on the page.
---

# Handwritten notes → LaTeX

The goal is a transcription the user can trust. Every line, arrow and margin note that's on the page must be in the .tex. Real slips get fixed but stay visible, and nothing gets invented or quietly reworded. The user values completeness and being asked over being guessed for.

Scripts live next to this file. Call them as `python3 <skill-dir>/scripts/...`, and use the session scratchpad for intermediates.

## 1. Skim everything first

Before asking anything, look at every page. For a PDF, use Read with `pages` in chunks of 20 or fewer. For photos, Read each image. While skimming, note:
- the topics and heading structure;
- suspected math slips, with the exact page and expression;
- blanks and unfinished lines, and whether any look intentionally blank;
- sketches and tables;
- crossed-out content, and overwritten characters (e.g. "1∓iω"). An overwrite isn't a strikeout: decide which stroke is final;
- blurred or illegible pages. Tell motion blur (smeared strokes) apart from faint or low-contrast ink, because only the faint kind can be rescued;
- show-through from the back of the page (faint mirrored text), which must be ignored;
- notation inconsistencies.

This inventory feeds both the interview questions and the agents' known-issues lists. Questions that quote real examples from the notes get far better answers than generic ones.

## 2. Full MCQ interview

Read `references/interview.md` and ask **every** question in it, in rounds of up to 4 with AskUserQuestion. The user explicitly wants the full interview each run, even though last time's answers are marked as "(last time)". Quote concrete items from the skim in the questions. Free-text answers override the options; apply them literally.

## 3. Prep images

```bash
python3 <skill-dir>/scripts/prep_pages.py "<input.pdf | photo_dir>" <pages_dir> <scratch>/crops [--pages 3-7]
```

`<pages_dir>` is the output location from the interview. Crops always go in the scratchpad. Use `--pages` for partial jobs or re-runs; real page numbers are kept.

This renders PDFs at 400 DPI with `pdftoppm`. Photos are EXIF-rotated, and HEIC files are converted with `sips`. Each page gets a mild contrast boost (autocontrast plus 1.3×) and is written as `p-NN.png`, along with top and bottom 55% crops. The crops matter because the Read tool downsamples a full 400-DPI page, and faint pencil margin notes vanish at that size.

**Illegible pages.**
- **Faint or low-contrast pages:** run `prep_pages.py --strong N <pages_dir>` once (grayscale, heavy contrast, sharpen), then Read `p-NN-strong.png` yourself. If it's readable, transcribe from it.
- **Motion-blurred pages** (smeared strokes, a photo of the notebook in motion): enhancement can't restore detail that isn't there, so skip on the skim's evidence alone.
- **If a page is still unreadable:** the .tex gets only `% p.N: illegible in source, skipped`, with no `\srcpage`. Say so in the final report and suggest re-photographing that page.

One strong attempt is enough; repeated passes waste time.

## 4. Transcribe

Split the pages the way the user chose in the interview. For parallel runs:
- Fill in `references/agent_prompt.md` for each chunk.
- Launch all general-purpose agents in one message.
- Each agent writes `<scratch>/frag_<X>.tex`.

Give each chunk:
- its **context**, meaning which section the previous chunk ends inside;
- its **known issues** from your skim.

If the user chose no subagents, transcribe sequentially yourself. The CONVENTIONS and WHAT COUNTS AS A SLIP sections of `references/agent_prompt.md` are the house rules for *any* transcriber, you included, so read them first.

Meanwhile, copy `assets/preamble.tex` to the scratchpad and adapt it to the interview answers:
- the flag-macro bodies (inline italic, footnote, or hidden);
- dropping tikz/pgfplots if figures aren't being drawn;
- the title;
- body-only output if chosen.

The default macro bodies already match last time's answers (inline italic flags, footnote page markers). Keep `pgfplots` only if a figure actually uses `axis`.

## 5. Merge, check, review

```bash
python3 <skill-dir>/scripts/merge_tex.py <scratch>/preamble.tex <out>.tex <scratch>/frag_A.tex <scratch>/frag_B.tex ...
python3 <skill-dir>/scripts/check_tex.py <out>.tex --pages 1-<N> --skip <illegible pages>
```

Always merge with the script and never with shell `echo`/heredocs. zsh's `echo` turns the `\e` of `\end{document}` into an ESC byte, and that silently broke a past run.

Then do your own coverage pass. This is the step that catches what agents miss. If you transcribed everything yourself, shorten it to spot checks of the dense pages and every `\corr`; re-reading what you just wrote has little value. For agent output, do it in full:
- Read the merged .tex in full, section by section, against the page images. Look for missing lines, margin notes and sketches, and for odd readings.
- Re-examine every `\corr` that looks like it might not be a real slip. Agents tend to over-flag. Relabelling, standard derivation devices and stated conventions should be demoted to a `\textit{Note:}`, because a pile of pedantic corrections buries the real ones.
- Open the crop image yourself for any disputed reading before accepting or overriding an agent's choice.
- Re-run `check_tex.py` after your edits.

## 6. Compile (only if the user said yes)

```bash
cd <out dir> && tectonic <out>.tex
```

Fix errors and rebuild until it compiles cleanly. If the user said not to compile, don't.

## 7. Report

Keep it short:
- output paths;
- pages covered and skipped, with the reason;
- counts of `\corr` and `\added`;
- the handful of most important corrections;
- uncertain readings worth a look, each with its page number;
- which checks ran, and whether the file was compiled.

## Conventions worth knowing (why they exist)

- **`\corr`/`\added` inside math go in `\text{...}`.** The macros are text-mode, so used bare they break inside align*.
- **`\srcpage` never goes in a `\section{}` argument or a display.** A footnote in a moving argument or an align* either errors out or disappears. Hang it on a short lead-in line instead.
- **Blanks the notes mean to be blank stay blank.** An example is "( )(−1,−1)+( )(1,1): not possible". Filling those in contradicts the notes.
- **Notation stays as written unless the user asked to normalise.** The user reads this side by side with the original.
- **A correction inside a table cell** goes on its own line right below the table, naming the row, so the table stays readable.
- **A page that starts inside a theorem or example** gets its `\srcpage` on the first text line inside the environment, which is fine there.
- **Tiny margin sketches next to table rows** become inline mini TikZ in an extra column. Bigger sketches are about 5 cm figures in a centered block.
