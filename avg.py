#!/usr/bin/env python
from __future__ import print_function
from collections import defaultdict
import os
import sys
import fileinput

# Calculate average separately for separate files
files = defaultdict(lambda: {"duration": 0, "lines": 0})

for line in fileinput.input():
    try:
        # If this fails, no entry is created
        duration = sum(map(float, line.split("\t")))

        f = files[os.path.basename(fileinput.filename())]
        f["duration"] += duration
        f["lines"] += 1
    except:
        pass

if len(files) > 0:
    for name, result in files.iteritems():
        print(name, result["duration"] / result["lines"])
else:
    print("No profiling data found.", file=sys.stderr)