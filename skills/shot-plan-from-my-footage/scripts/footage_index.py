#!/usr/bin/env python3
"""Index your own footage so a shot plan can name real clips.

    python3 footage_index.py <folder> [<folder> ...] [--out footage.json] [--thumbs footage-thumbs]

For every video under the folders: path, length, width x height, orientation and date, written to footage.json, plus a
thumbnail strip (five frames across the clip) in footage-thumbs/ so Claude can see what is in it. Needs ffmpeg and ffprobe.
Nothing leaves your machine.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

VIDEO = {'.mov', '.mp4', '.m4v', '.mkv', '.avi', '.mts'}


def probe(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                        'stream=width,height:stream_side_data=rotation:format=duration:format_tags=creation_time', '-of', 'json', str(path)],
                       capture_output=True, text=True, timeout=60)
    try:
        d = json.loads(r.stdout)
        s = d['streams'][0]
        w, h = s['width'], s['height']
        rot = abs(int(float((s.get('side_data_list') or [{}])[0].get('rotation', 0) or 0)))
        if rot in (90, 270):
            w, h = h, w
        return {'seconds': round(float(d['format']['duration']), 1), 'width': w, 'height': h,
                'orientation': 'vertical' if h > w else 'horizontal' if w > h else 'square',
                'date': (d['format'].get('tags') or {}).get('creation_time', '')[:10]}
    except (ValueError, KeyError, IndexError, TypeError):
        return None


def strip(path, seconds, out):
    """Five frames across the clip, side by side."""
    if out.exists():
        return
    step = max(seconds / 5, 0.1)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(path), '-vf', f'fps=1/{step:.3f},scale=200:-2,tile=5x1', '-frames:v', '1', '-q:v', '5', str(out)],
                   capture_output=True, timeout=300)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('folders', nargs='+')
    ap.add_argument('--out', default='footage.json')
    ap.add_argument('--thumbs', default='footage-thumbs')
    a = ap.parse_args()
    thumbs = Path(a.thumbs)
    thumbs.mkdir(exist_ok=True)
    clips = []
    for folder in a.folders:
        for p in sorted(Path(folder).expanduser().rglob('*')):
            if p.suffix.lower() not in VIDEO or p.name.startswith('.'):
                continue
            info = probe(p)
            if not info:
                continue
            thumb = thumbs / (hashlib.sha1(str(p).encode()).hexdigest()[:12] + '.jpg')
            strip(p, info['seconds'], thumb)
            clips.append({'file': str(p), 'name': p.name, **info, 'thumbs': str(thumb)})
    Path(a.out).write_text(json.dumps(clips, indent=1))
    print(f'{len(clips)} clips -> {a.out} (thumbnail strips in {thumbs}/)')


if __name__ == '__main__':
    main()
