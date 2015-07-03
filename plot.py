#!/usr/bin/env python
from __future__ import print_function
import sys
import math
import fileinput
import matplotlib.pyplot as plt

files = set()

totals = []
details = []
headers = []

colors = ["cornflowerblue", "purple", "orangered", "orange", "yellowgreen", "lightseagreen", "mediumpurple", "orchid", "crimson", "silver"]

for line in fileinput.input():

    files.add(fileinput.filename())

    try:
        values = map(float, line.split("\t"))

        if len(headers) == 0:
            if len(values) == 3:
                headers = ["Draw", "Execute", "Process"]
            elif len(values) == 4: # Prepare only exists on Lollipop and above
                headers = ["Draw", "Prepare", "Execute", "Process"]
            else:
                headers = map(str, range(len(values)))

        totals.append(sum(values))

        for i, val in enumerate(values):
            try:
                details[i].append(val)
            except:
                details.append([val])
    except ValueError:
        if fileinput.isfirstline():
            headers = line.strip().split("\t")
        else:
            print("Unexpected parse error.", file=sys.stderr)

if len(headers) == 3:
    colors = ["cornflowerblue", "orangered", "orange"]
elif len(colors) > len(headers):
    colors = colors[:len(headers)]

if len(totals) > 0 and len(details) > 0:

    title = ", ".join(files)
    time = range(len(totals))
    threshold = 16.67;

    # histogram of frame delays
    plt.subplot2grid((3, 2), (0, 0))
    plt.hist([i for i in totals if i > 0], range(0, int(math.ceil(max(totals))) + 1), color="limegreen")
    plt.plot([threshold, threshold], [0, plt.axis()[3]], color="limegreen")
    plt.title("Frame Duration Distribution")
    plt.xlabel("Total Frame Time (ms)")
    plt.ylabel("Frequency")

    # histogram of each component of gfxinfo
    ax = plt.subplot2grid((3, 2), (0, 1))
    plt.hist([i for i in details if i > 0], range(0, int(math.ceil(max(map(max, details)))) + 1), label=headers, color=colors, linewidth=0)
    plt.plot([threshold, threshold], [0, plt.axis()[3]], color="limegreen")
    plt.title("Component Distribution")
    plt.xlabel("Time (ms)")
    plt.ylabel("Frequency")
    ax.legend()

    # frame series
    ax = plt.subplot2grid((3, 2), (1, 0), colspan=2)
    for i, (detail, column, color) in enumerate(zip(details, headers, colors)):
        ax.bar(time, detail, label=column, color=color, linewidth=0, bottom=[0] * len(detail) if i == 0 else map(sum, zip(*details[:i])), width=1.0)
    ax.plot([0, len(totals)], [threshold, threshold], color="limegreen")
    plt.title(title + " Frame Series")
    plt.xlabel("Frame Number")
    plt.xlim([0, len(totals)])
    plt.ylabel("Time (ms)")
    ax.legend()

    # sort by total frame time
    duration_curves = [list(l) for l in zip(*sorted(zip(*details), key=sum, reverse=True))]

    ax = plt.subplot2grid((3, 2), (2, 0), colspan=2)
    for i, (detail, column, color) in enumerate(zip(duration_curves, headers, colors)):
        ax.bar(time, detail, label=column, color=color, linewidth=0, bottom=[0] * len(detail) if i == 0 else map(sum, zip(*duration_curves[:i])), width=1.0)
    ax.plot([0, len(totals)], [threshold, threshold], color="limegreen")
    plt.title(title + " Duration Curve")
    plt.xlabel("Frame Number")
    plt.xlim([0, len(totals)])
    plt.ylabel("Time (ms)")
    ax.legend()

    plt.subplots_adjust(hspace=0.35)
    plt.show()
else:
    print("No profiling data found.", file=sys.stderr)