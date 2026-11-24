#!/usr/bin/env python3
"""Lay a reel out so Claude can watch it frame by frame.

    python3 breakdown.py <instagram reel link | local video file> [--out reels/<name>]

Writes into the output folder:
    reel.mp4            the video (downloaded with yt-dlp when you give a link; public reels only, no login)
    sheets/sheet_NN.jpg contact sheets over the whole reel: four frames a second, one second per row
    stills/tNNNN.NN.jpg a larger frame at the start and just after every cut
    transcript.json     what is said, with times (needs whisper-cli or the openai-whisper CLI; skipped without one)
    facts.json          length, cut times, who made it, its caption, likes

Needs ffmpeg and ffprobe. yt-dlp for links. Nothing is uploaded anywhere.
"""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

COLS = ROWS = 4
MAX_SHEETS = 32
MAX_STILLS = 12
CODE = re.compile(r'(?:^|/)(?:reel|reels|p|tv)/([A-Za-z0-9_-]{5,30})(?=[/?#]|$)')


def run(cmd, timeout=600):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except FileNotFoundError:
        sys.exit(f'{Path(cmd[0]).name} is not installed. Install it first (macOS: brew install {Path(cmd[0]).name}).')


def plan_sheets(duration):
    """Contact sheets that cover the whole reel: four frames a second and a second per row, thinner only when it runs long."""
    for fps in (4, 2, 1, 0.5, 0.25):
        seconds = COLS * ROWS / fps
        count = max(1, -(-duration // seconds))
        if count <= MAX_SHEETS:
            break
    return [{'index': i + 1, 'start': i * seconds, 'seconds': seconds, 'fps': fps} for i in range(int(count))]


def still_times(cuts, duration):
    """The opening, then just after each cut has landed; at most MAX_STILLS, spread evenly."""
    times = [0.2] + [round(c + 0.15, 2) for c in sorted(cuts) if 0.3 < c + 0.15 < duration - 0.1]
    if len(times) > MAX_STILLS:
        step = (len(times) - 1) / (MAX_STILLS - 1)
        times = [times[round(i * step)] for i in range(MAX_STILLS)]
    return times


def fetch(source, out):
    """The reel as out/reel.mp4, and what is known about it."""
    out.mkdir(parents=True, exist_ok=True)
    video = out / 'reel.mp4'
    local = Path(source).expanduser()
    if local.exists():
        if local.resolve() != video.resolve():
            shutil.copyfile(local, video)
        return {'source': str(local)}
    code = CODE.search(source.split('?')[0])
    if not code:
        sys.exit('That is neither a video file nor an Instagram reel link.')
    url = f'https://www.instagram.com/reel/{code.group(1)}/'
    if not video.exists():
        done = run(['yt-dlp', '--no-playlist', '--no-warnings', '-q', '-o', str(out / 'reel.%(ext)s'), '--write-info-json',
                    '-f', 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/b', '--merge-output-format', 'mp4', url], timeout=300)
        if done.returncode != 0 or not video.exists():
            why = ((done.stderr or done.stdout or '').strip().splitlines() or ['no reason given'])[-1]
            sys.exit(f'The reel could not be downloaded (private, a photo post, or removed?): {why[:200]}')
    meta = out / 'reel.info.json'
    info = json.loads(meta.read_text()) if meta.exists() else {}
    return {'source': url, 'author': info.get('channel') or info.get('uploader_id') or info.get('uploader'),
            'caption': (info.get('description') or '').strip(), 'likes': info.get('like_count')}


def transcribe(out, video):
    """What is said, with times; [] when there is no transcriber or no speech (the frames still carry the reel)."""
    wav = out / 'audio.wav'
    if run(['ffmpeg', '-v', 'error', '-y', '-i', str(video), '-vn', '-ar', '16000', '-ac', '1', str(wav)]).returncode != 0:
        return []
    try:
        model = os.environ.get('WHISPER_MODEL', str(Path.home() / '.whisper-models' / 'ggml-small.en.bin'))
        if shutil.which('whisper-cli') and Path(model).exists():
            if run(['whisper-cli', '-m', model, '-f', str(wav), '-oj', '-of', str(out / 'whisper'), '-np'], 900).returncode == 0:
                lines = json.loads((out / 'whisper.json').read_text()).get('transcription', [])
                return [{'start': l['offsets']['from'] / 1000, 'end': l['offsets']['to'] / 1000, 'text': l['text'].strip()} for l in lines if l['text'].strip()]
        if shutil.which('whisper'):
            if run(['whisper', str(wav), '--model', 'small', '--output_format', 'json', '--output_dir', str(out)], 1800).returncode == 0:
                segs = json.loads((out / 'audio.json').read_text()).get('segments', [])
                return [{'start': s['start'], 'end': s['end'], 'text': s['text'].strip()} for s in segs if s['text'].strip()]
        print('No transcriber found (whisper-cli or whisper): the breakdown goes on from the frames alone.', file=sys.stderr)
        return []
    finally:
        wav.unlink(missing_ok=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('source', help='an Instagram reel link or a video file')
    ap.add_argument('--out', help='output folder (default: reels/<reel code or file name>)')
    a = ap.parse_args()
    m = CODE.search(a.source.split('?')[0])
    out = Path(a.out or f'reels/{m.group(1) if m else Path(a.source).stem}')
    facts = fetch(a.source, out)
    video = out / 'reel.mp4'
    probe = run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=codec_type', '-of', 'json', str(video)], 60)
    try:
        info = json.loads(probe.stdout)
        duration = round(float(info['format']['duration']), 2)
    except (ValueError, KeyError):
        sys.exit('That file is not a video ffmpeg can read.')
    kinds = [s.get('codec_type') for s in info.get('streams', [])]
    (out / 'sheets').mkdir(exist_ok=True)
    (out / 'stills').mkdir(exist_ok=True)
    cell = 'scale=270:480:force_original_aspect_ratio=decrease,pad=270:480:(ow-iw)/2:(oh-ih)/2:white'
    sheets = []
    for s in plan_sheets(duration):
        path = out / 'sheets' / f'sheet_{s["index"]:02d}.jpg'
        run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{s["start"]:g}', '-t', f'{s["seconds"]:g}', '-i', str(video),
             '-vf', f'fps={s["fps"]:g},{cell},tile={COLS}x{ROWS}:padding=6:margin=6:color=white', '-frames:v', '1', '-q:v', '4', str(path)])
        if path.exists():
            sheets.append({'file': f'sheets/{path.name}', 'from_s': s['start'], 'to_s': min(s['start'] + s['seconds'], duration), 'frames_per_second': s['fps']})
    found = run(['ffmpeg', '-hide_banner', '-i', str(video), '-vf', "select='gt(scene,0.3)',showinfo", '-an', '-f', 'null', '-'])
    cuts = [round(float(t), 2) for t in re.findall(r'pts_time:([0-9.]+)', found.stderr or '')]
    stills = []
    for t in still_times(cuts, duration):
        path = out / 'stills' / f't{t:07.2f}.jpg'
        run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:g}', '-i', str(video), '-frames:v', '1', '-vf', 'scale=540:-2', '-q:v', '3', str(path)], 120)
        if path.exists():
            stills.append({'file': f'stills/{path.name}', 't': t})
    transcript = transcribe(out, video) if 'audio' in kinds else []
    (out / 'transcript.json').write_text(json.dumps(transcript, indent=1))
    facts.update(duration_s=duration, cuts_s=cuts, sheets=sheets, stills=stills, spoken_lines=len(transcript))
    (out / 'facts.json').write_text(json.dumps(facts, indent=1))
    print(f'{out}: {duration} s, {len(cuts)} cuts, {len(sheets)} sheets, {len(stills)} stills, {len(transcript)} spoken lines')


if __name__ == '__main__':
    main()
