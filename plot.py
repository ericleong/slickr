#!/usr/bin/env python
from __future__ import print_function
import sys
import math
import fileinput
import matplotlib.pyplot as plt

totals = []
details = []
headers = ["Draw", "Prepare", "Process", "Execute"]

for line in fileinput.input():

    try:
        values = map(float, line.split("\t"))
    except:
        if fileinput.isfirstline():
            headers = line.strip().split("\t")
            continue

    totals.append(sum(values))

    for i, val in enumerate(values):
        try:
            details[i].append(val)
        except:
            details.append([val])

if len(totals) > 0 and len(details) > 0:

    # Draw, Prepare, Process, Execute
    colors = ["cornflowerblue", "purple", "orangered", "orange"]
    time = range(len(totals))
    threshold = 16.67;

    # histogram of frame delays
    plt.subplot2grid((3, 2), (0, 0))
    plt.hist(totals, range(int(math.floor(min(totals))), int(math.ceil(max(totals))) + 1), color="limegreen")
    plt.title("Distribution of Frame Rendering Times")
    plt.xlabel("Total Render Time (ms)")
    plt.ylabel("Frequency")

    # histogram of each component of gfxinfo
    ax = plt.subplot2grid((3, 2), (0, 1))
    plt.hist(details, range(int(math.floor(min(min(details)))), int(math.ceil(max(max(details)))) + 1), label=headers, color=colors)
    plt.title("Distribution of Rendering Times")
    plt.xlabel("Render Time (ms)")
    plt.ylabel("Frequency")
    ax.legend()

    # time series
    ax = plt.subplot2grid((3, 2), (1, 0), colspan=2)
    for i, (detail, column, color) in enumerate(zip(details, headers, colors)):
        ax.bar(time, detail, label=column, color=color, linewidth=0, bottom=[0] * len(detail) if i == 0 else map(sum, zip(*details[:i])), width=1.0)
    ax.plot([0, len(totals)], [threshold, threshold], color="limegreen")
    plt.title("Render Time Series")
    plt.xlabel("Frame Number")
    plt.xlim([0, len(totals)])
    plt.ylabel("Render Time (ms)")
    ax.legend()

    # sort by total frame time
    duration_curves = [list(l) for l in zip(*sorted(zip(*details), key=sum, reverse=True))]

    ax = plt.subplot2grid((3, 2), (2, 0), colspan=2)
    for i, (detail, column, color) in enumerate(zip(duration_curves, headers, colors)):
        ax.bar(time, detail, label=column, color=color, linewidth=0, bottom=[0] * len(detail) if i == 0 else map(sum, zip(*duration_curves[:i])), width=1.0)
    ax.plot([0, len(totals)], [threshold, threshold], color="limegreen")
    plt.title("Render Duration Curve")
    plt.xlabel("Frame Number")
    plt.xlim([0, len(totals)])
    plt.ylabel("Render Time (ms)")
    ax.legend()

    plt.show()
else:
    print("No profiling data found.", file=sys.stderr)