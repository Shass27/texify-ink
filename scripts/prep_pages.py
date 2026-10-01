#!/usr/bin/env python3
"""Render handwritten notes (PDF or photo folder) to contrast-boosted page PNGs + half crops.

usage: prep_pages.py INPUT PAGES_DIR CROPS_DIR [--dpi 400] [--contrast 1.3] [--pages 3-7]
       prep_pages.py --strong N PAGES_DIR      (re-process an already-prepped page; faint/low-contrast pages only)
"""
import argparse, glob, os, re, shutil, subprocess, sys, tempfile
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

PHOTO_EXT = ('.jpg', '.jpeg', '.png', '.heic', '.heif', '.tif', '.tiff')


def mild(im, contrast):
    return ImageEnhance.Contrast(ImageOps.autocontrast(im, cutoff=1)).enhance(contrast)


def strong(im):
    # grayscale first: sharpening colour channels separately posterizes into colour noise
    g = ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=2)
    return ImageEnhance.Contrast(g).enhance(1.8).filter(ImageFilter.UnsharpMask(3, 150, 3))


def write_crops(im, n, crops_dir):
    w, h = im.size  # top/bottom 55% with 10% overlap so no line is cut in both
    im.crop((0, 0, w, int(h * 0.55))).save(f'{crops_dir}/p-{n:02d}-top.png')
    im.crop((0, int(h * 0.45), w, h)).save(f'{crops_dir}/p-{n:02d}-bot.png')


def raw_pages(src, dpi, tmp, first=None, last=None):
    """Return [(page_no, path)] of unprocessed page images."""
    if src.lower().endswith('.pdf'):
        cmd = ['pdftoppm', '-r', str(dpi), '-png']
        if first:
            cmd += ['-f', str(first), '-l', str(last)]
        subprocess.run(cmd + [src, f'{tmp}/r'], check=True)
        files = sorted(glob.glob(f'{tmp}/r-*.png'))
        return [(int(re.search(r'-(\d+)\.png$', f).group(1)), f) for f in files]  # keep real PDF page numbers
    files = sorted(f for f in glob.glob(f'{src}/*') if f.lower().endswith(PHOTO_EXT))
    for i, f in enumerate(files):
        if f.lower().endswith(('.heic', '.heif')):  # Pillow can't read HEIC without extra deps; sips ships with macOS
            out = f'{tmp}/h-{i:03d}.png'
            subprocess.run(['sips', '-s', 'format', 'png', f, '--out', out], check=True, capture_output=True)
            files[i] = out
    pages = list(enumerate(files, 1))
    return [p for p in pages if not first or first <= p[0] <= last]


def main():
    if '--strong' in sys.argv:
        ap = argparse.ArgumentParser(); ap.add_argument('--strong', type=int, required=True); ap.add_argument('pages_dir')
        a = ap.parse_args()
        out = f'{a.pages_dir}/p-{a.strong:02d}-strong.png'  # never overwrites the original page
        strong(Image.open(f'{a.pages_dir}/p-{a.strong:02d}.png').convert('RGB')).save(out)
        print(out); return

    ap = argparse.ArgumentParser()
    ap.add_argument('input'); ap.add_argument('pages_dir'); ap.add_argument('crops_dir')
    ap.add_argument('--dpi', type=int, default=400)
    ap.add_argument('--contrast', type=float, default=1.3)
    ap.add_argument('--pages', help='page range like 3-7 (default: all)')
    a = ap.parse_args()
    first = last = None
    if a.pages:
        first, _, last = a.pages.partition('-'); first, last = int(first), int(last or first)
    os.makedirs(a.pages_dir, exist_ok=True); os.makedirs(a.crops_dir, exist_ok=True)

    tmp = tempfile.mkdtemp()
    try:
        pages = raw_pages(a.input, a.dpi, tmp, first, last)
        if not pages:
            sys.exit(f'no pages found in {a.input}')
        for n, f in pages:
            im = mild(ImageOps.exif_transpose(Image.open(f)).convert('RGB'), a.contrast)
            im.save(f'{a.pages_dir}/p-{n:02d}.png')
            write_crops(im, n, a.crops_dir)
        print(f'{len(pages)} pages -> {a.pages_dir}, {2 * len(pages)} crops -> {a.crops_dir}')
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    main()
