#!/usr/bin/env python3
"""Structural checks for a transcribed .tex (no compiler needed). Exits 1 on any problem.

usage: check_tex.py FILE [--pages 1-23] [--skip 15,16]
"""
import argparse, re, sys
from collections import Counter


def rng(s):
    out = set()
    for part in filter(None, (s or '').split(',')):
        a, _, b = part.partition('-')
        out.update(range(int(a), int(b or a) + 1))
    return out


def check(text, pages=(), skip=()):
    probs = []
    if '\x1b' in text:
        probs.append('ESC byte found (shell echo mangled a \\e...) -- rebuild with merge_tex.py')
    body = re.sub(r'(?<!\\)%.*', '', text)  # drop comments
    begins = Counter(re.findall(r'\\begin\{([^}]+)\}', body))
    ends = Counter(re.findall(r'\\end\{([^}]+)\}', body))
    for env in begins | ends:
        if begins[env] != ends[env]:
            probs.append(f'env {env}: {begins[env]} begin vs {ends[env]} end')
    stripped = re.sub(r'\\[{}]', '', body)
    if stripped.count('{') != stripped.count('}'):
        probs.append(f'brace diff {stripped.count("{") - stripped.count("}")}')
    for m in re.finditer(r'(?<!\\)\\\\[a-z]+', body):  # "\\tfrac" = linebreak + literal text; uppercase skipped ("NOT\\CONT" in a node is a real break)
        line = body.count('\n', 0, m.start()) + 1
        probs.append(f'line {line}: suspicious "{m.group()}" (meant a single backslash?)')
    if pages:
        found = {int(n) for n in re.findall(r'\\srcpage\{(\d+)\}', text)}
        want = set(pages) - set(skip)
        if want - found:
            probs.append(f'missing \\srcpage for pages {sorted(want - found)}')
        if found & set(skip):
            probs.append(f'\\srcpage present for skipped pages {sorted(found & set(skip))}')
    return probs


def demo():
    good = '\\begin{align*}a\\\\ b\\end{align*}\\srcpage{1}'
    assert check(good, [1, 2], [2]) == []
    bad = '\x1bnd{x} \\begin{center} {\\\\tfrac'
    p = check(bad, [1])
    assert len(p) == 5, p  # ESC, env, brace, \\tfrac, missing srcpage


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '--selftest':
        demo(); print('selftest ok'); sys.exit()
    ap = argparse.ArgumentParser()
    ap.add_argument('file'); ap.add_argument('--pages'); ap.add_argument('--skip')
    a = ap.parse_args()
    probs = check(open(a.file).read(), rng(a.pages), rng(a.skip))
    print('\n'.join(probs) or 'OK: no structural problems')
    sys.exit(1 if probs else 0)
