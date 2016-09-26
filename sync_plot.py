#!/usr/bin/env python
from __future__ import print_function
import sys
import math
import fileinput
import matplotlib.pyplot as plt

files = {}

for line in fileinput.input():

    if fileinput.filename() not in files:
        files[fileinput.filename()] = {"totals": [], "details": [], "headers": []}

    try:
        split_row = line.strip().split("\t")

        if len(files[fileinput.filename()]["headers"]) == 0:
            if len(split_row) == 3:
                files[fileinput.filename()]["headers"] = ["Draw", "Execute", "Process"]
            elif len(split_row) == 4: # Prepare only exists on Lollipop and above
                files[fileinput.filename()]["headers"] = ["Draw", "Prepare", "Execute", "Process"]
            else:
                files[fileinput.filename()]["headers"] = split_row

        if len(split_row) > len(files[fileinput.filename()]["headers"]):
            split_row = split_row[:len(files[fileinput.filename()]["headers"])]

        values = list(map(float, split_row))

        files[fileinput.filename()]["totals"].append(sum(values))

        for i, val in enumerate(values):
            if val < 0:
                print("line", fileinput.filelineno(), "col", i, ":", val, "< 0", file=sys.stderr)
                val = 0

            try:
                files[fileinput.filename()]["details"][i].append(val)
            except:
                files[fileinput.filename()]["details"].append([val])
    except ValueError:
        if fileinput.isfirstline():
            files[fileinput.filename()]["headers"] = line.strip().split("\t")
        else:
            print("Unexpected parse error.", file=sys.stderr)

file_index = 0
axes = []
max_ymax = 0

for filename in files:
    data = files[filename]

    headers = data["headers"]
    details = data["details"]
    totals = data["totals"]

    colors = ["cornflowerblue", "purple", "orangered", "orange", "yellowgreen", "lightseagreen", "mediumpurple", "orchid", "crimson", "silver"]
    if len(headers) == 3:
        colors = ["cornflowerblue", "orangered", "orange"]
    elif len(colors) > len(headers):
        colors = colors[:len(headers)]

    if len(totals) > 0 and len(details) > 0:

        title = filename
        time = range(len(totals))
        threshold = 16.67;

        gfx = "Draw" in headers
        framestats = "draw" in headers

        # frame series
        ax = plt.subplot2grid((len(files), 1), (file_index, 0))
        for i, (detail, column, color) in enumerate(zip(details, headers, colors)):
            ax.bar(time, detail, label=column, color=color, linewidth=0, bottom=[0] * len(detail) if i == 0 else list(map(sum, zip(*details[:i]))), width=1.0)
        ax.plot([0, len(totals)], [threshold, threshold], color="limegreen")
        plt.title(title + " Frame Series")
        plt.xlabel("Frame Number")
        plt.xlim([0, len(totals)])
        plt.ylabel("Time (ms)")

        _, ymax = ax.get_ylim()

        if ymax > max_ymax:
            max_ymax = ymax

        axes.append(ax)

        ax.legend(ncol=len(headers), columnspacing=0.5, handletextpad=0.5, borderpad=0.5)

    else:
        print("No profiling data found.", file=sys.stderr)

    file_index += 1

for ax in axes:
    ax.set_ylim([0, max_ymax])

plt.subplots_adjust(hspace=0.35)
plt.show()
