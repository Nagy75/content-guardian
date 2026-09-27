import argparse
import json
import re
import subprocess
from pathlib import Path

TIME = re.compile(r'^(\d{1,2}:\d{2}(?::\d{2})?)-(\d{1,2}:\d{2}(?::\d{2})?)$')

def parse_time(value: str) -> float:
    parts = [int(x) for x in value.split(':')]
    if len(parts) == 2: return parts[0] * 60 + parts[1]
    if len(parts) == 3: return parts[0] * 3600 + parts[1] * 60 + parts[2]
    raise ValueError(f'Invalid time: {value}')

def parse_interval(value: str):
    match = TIME.match(value.strip())
    if not match: raise ValueError(f'Expected START-END, got {value}')
    start, end = map(parse_time, match.groups())
    if end <= start: raise ValueError(f'End must be after start: {value}')
    return start, end

def load_config(path: str | None, skips: list[str]):
    config = json.loads(Path(path).read_text()) if path else {}
    intervals = [parse_interval(x) for x in config.get('skipIntervals', []) + skips]
    return config.get('blockedWords', []), intervals

def build_filter(input_file, output_file, intervals):
    # Remove manually reviewed intervals by selecting the complementary segments.
    if not intervals:
        return ['ffmpeg', '-y', '-i', input_file, '-c', 'copy', output_file]
    intervals = sorted(intervals)
    pieces = []
    cursor = 0.0
    for start, end in intervals:
        if start > cursor: pieces.append((cursor, start))
        cursor = max(cursor, end)
    # The final segment is intentionally open-ended; FFmpeg accepts it as the last portion.
    pieces.append((cursor, None))
    streams = []
    for i, (start, end) in enumerate(pieces):
        streams += ['-ss', str(start), '-i', input_file]
    filters = []
    for i, (_, end) in enumerate(pieces):
        filters.append(f'[{i}:v:0]trim=start=0' + (f':end={end}' if end is not None else '') + f',setpts=PTS-STARTPTS[v{i}]')
        filters.append(f'[{i}:a:0]atrim=start=0' + (f':end={end}' if end is not None else '') + f',asetpts=PTS-STARTPTS[a{i}]')
    concat = ''.join(f'[v{i}][a{i}]' for i in range(len(pieces)))
    filters.append(f'{concat}concat=n={len(pieces)}:v=1:a=1[v][a]')
    return ['ffmpeg', '-y', *streams, '-filter_complex', ';'.join(filters), '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-c:a', 'aac', output_file]

def main():
    parser = argparse.ArgumentParser(description='Create a filtered copy of a video.')
    parser.add_argument('input'); parser.add_argument('--output', required=True)
    parser.add_argument('--words', help='JSON config containing blockedWords and skipIntervals')
    parser.add_argument('--skip', action='append', default=[], help='START-END interval to remove')
    args = parser.parse_args()
    _, intervals = load_config(args.words, args.skip)
    command = build_filter(args.input, args.output, intervals)
    subprocess.run(command, check=True)
    print(f'Created {args.output}')

if __name__ == '__main__': main()
