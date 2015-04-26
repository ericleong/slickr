#!/usr/bin/env python
from __future__ import print_function
import sys
import fileinput

total_duration = 0
num_lines = 0

for line in fileinput.input():
    try:
        total_duration += sum(map(float, line.split('\t')))
        num_lines += 1
    except:
        pass

if num_lines > 0:
    print(total_duration / num_lines)
else:
    print("No profiling data found.", file=sys.stderr)