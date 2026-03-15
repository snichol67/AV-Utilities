#!/usr/bin/env python3
import sys
import re

TIMESTAMP = re.compile(
    r"(\d{2}):(\d{2}):(\d{2}),(\d{3})"
)

def to_ms(h, m, s, ms):
    return (((int(h) * 60 + int(m)) * 60 + int(s)) * 1000 + int(ms))

def from_ms(total):
    if total < 0:
        total = 0
    ms = total % 1000
    total //= 1000
    s = total % 60
    total //= 60
    m = total % 60
    h = total // 60
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def shift_line(line, offset):
    def repl(match):
        t = to_ms(*match.groups())
        return from_ms(t + offset)
    return TIMESTAMP.sub(repl, line)

def main():
    if len(sys.argv) != 4:
        print("Usage: shift_srt.py input.srt output.srt offset_ms")
        sys.exit(1)

    infile, outfile, offset = sys.argv[1], sys.argv[2], int(sys.argv[3])

    with open(infile, "r", encoding="utf-8") as f:
        lines = f.readlines()

    with open(outfile, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(shift_line(line, offset))

if __name__ == "__main__":
    main()