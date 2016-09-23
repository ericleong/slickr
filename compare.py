#!/usr/bin/env python
from __future__ import print_function
from collections import defaultdict
import os
import sys
import math
import fileinput
import matplotlib.pyplot as plt

totals = defaultdict(list)

for line in fileinput.input():

    try:
        values = map(float, line.split("\t"))
        totals[os.path.basename(fileinput.filename())].append(sum(values))
    except:
        if fileinput.isfirstline():
            headers = line.strip().split("\t")
            continue

if len(totals) > 0:

    time = [range(len(value)) for value in totals.values()]
    max_time = max(map(len, totals.values()))
    threshold = 16.67;

    # histogram of frame delays
    ax = plt.subplot(2, 1, 1)
    ax.hist(totals.values(), range(int(math.floor(min(map(min, totals.values())))), int(math.ceil(max(map(max, totals.values())))) + 1), label=totals.keys(), linewidth=0)
    ax.plot([threshold, threshold], [0, plt.axis()[3]], color="limegreen")
    plt.title("Frame Duration Distribution")
    plt.xlabel("Total Frame Time (ms)")
    plt.ylabel("Frequency")
    ax.legend()

    sorted_totals = {k: sorted(v, reverse=True) for k, v in totals.iteritems()}

    # sort by total frame time
    ax = plt.subplot(2, 1, 2)
    for x, (name, y) in zip(time, sorted_totals.iteritems()):
        ax.plot(x, y, label=name)

    # render duration curve
    ax.plot([0, max_time], [threshold, threshold], color="limegreen")
    plt.title("Duration Curve")
    plt.xlabel("Frame Number")
    plt.xlim([0, max_time])
    plt.ylabel("Render Time (ms)")
    ax.legend()

    plt.subplots_adjust(hspace=0.35)
    plt.show()
else:
    print("No profiling data found.", file=sys.stderr)