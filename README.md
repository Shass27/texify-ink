# texify-ink

A Claude Code skill that turns handwritten notes (a scanned or photographed
PDF, or a folder of notebook photos, HEIC included) into minimal, clean LaTeX,
page by page, without missing content.

## Install

```bash
git clone https://github.com/Shass27/texify-ink ~/.claude/skills/handwritten-to-latex
```

The folder name matches the skill name (`handwritten-to-latex`) in `SKILL.md`.
Needs `python3` with Pillow, `pdftoppm` (poppler), and optionally `tectonic`
to compile.

## Usage

Ask Claude Code in plain words, e.g. "convert my notes pdf to latex" or "type
up these notebook pages", and point it at the PDF or photo folder. The skill
asks a full multiple-choice interview (output location, how to flag fixes,
how to split work, whether to compile), then does the transcription.

## How it works

1. **Skim** every page first, noting slips, blanks, sketches, crossed-out text
   and illegible pages.
2. **Interview** you with MCQs that quote real items from your notes.
3. **Prep images** with `scripts/prep_pages.py`: 400 DPI render, contrast
   boost, plus top/bottom crops so faint margin notes stay readable.
4. **Transcribe** page by page (optionally in parallel subagents). Math slips
   are fixed but flagged (`\corr`), additions are marked (`\added`), sketches
   are redrawn in TikZ, and each page gets a source-page marker.
5. **Merge and check** with `merge_tex.py` and `check_tex.py`, then a coverage
   pass against the page images.
6. **Compile** with `tectonic` if you said yes, and get a short report.

Nothing is invented or quietly reworded; blanks you left blank stay blank.

## Workflows with stem-notes

texify-ink *transcribes* what is on the page. [stem-notes](https://github.com/Shass27/stem-notes)
*builds* formula sheets, worked solutions and summaries from source material.
They chain well:

1. **Transcribe, then enrich**: run texify-ink on your handwritten notes, then
   hand the `.tex`/PDF to stem-notes for a formula sheet or summary notes.
2. **Handwritten solutions + problem sheet**: transcribe your worked solutions
   with texify-ink, then have stem-notes solve the problem sheet and flag
   where your solutions differ.
3. **Slides + handwritten merge**: run stem-notes on the lecture slides and
   texify-ink on your handwritten annotations, then combine both into one
   revision pack.
4. **Book skill loop**: build a knowledge skill for the course textbook with
   [book-to-skill](https://github.com/virgiliojr94/book-to-skill), then
   cross-check your transcribed notes against it (`/my-book <topic>`). That
   tool is the work of [virgiliojr94](https://github.com/virgiliojr94); credit
   for it belongs to them, not to texify-ink.

## License

MIT, see `LICENSE`.
