#!/usr/bin/env python3
"""Merge preamble + body fragments into one .tex. Python on purpose: zsh `echo` turns `\\e` into ESC.

usage: merge_tex.py PREAMBLE OUT FRAG [FRAG ...]   (fragments are joined in the order given)
"""
import sys

if len(sys.argv) < 4:
    sys.exit(__doc__)
pre, out, frags = sys.argv[1], sys.argv[2], sys.argv[3:]
parts = [open(pre).read().rstrip() + '\n']
for f in frags:
    parts.append(f'\n% ===== {f.rsplit("/", 1)[-1]} =====\n' + open(f).read().rstrip() + '\n')
parts.append('\n\\end{document}\n')
open(out, 'w').write(''.join(parts))
print(f'wrote {out} from {len(frags)} fragments')
