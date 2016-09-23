#!/usr/bin/env python
from __future__ import division
from __future__ import print_function
import sys
import fileinput

def parse_framestats(line, valid_only=False):

    # http://developer.android.com/preview/testing/performance.html#fs-data-format

    # Strip trailing comma
    framestats = list(map(int, line[:len(line) - 1].split(",")))

    # Default values. This keeps the data aligned with gfxinfo.
    start = 0
    handle_input = 0
    animations = 0
    traversals = 0
    draw = 0
    sync = 0
    gpu = 0

    if framestats[0] == 0 and len(framestats) == 14:

        # HANDLE_INPUT_START - INTENDED_VSYNC
        start = (framestats[5] - framestats[1]) / 1000000

        # ANIMATION_START - HANDLE_INPUT_START
        handle_input = (framestats[6] - framestats[5]) / 1000000

        # PERFORM_TRAVERSALS_START - ANIMATION_START
        animations = (framestats[7] - framestats[6]) / 1000000

        # DRAW_START - PERFORM_TRAVERSALS_START
        traversals = (framestats[8] - framestats[7]) / 1000000

        # SYNC_START - DRAW_START
        draw = (framestats[10] - framestats[8]) / 1000000

        # ISSUE_DRAW_COMMANDS_START - SYNC_START
        sync = (framestats[11] - framestats[10]) / 1000000

        # FRAME_COMPLETED - ISSUE_DRAW_COMMANDS_START
        gpu = (framestats[13] - framestats[11]) / 1000000

    elif valid_only:

        raise ValueError("Invalid frame.")

    return start, handle_input, animations, traversals, draw, sync, gpu

# Globals

has_header = False

in_profile_section = False
in_activity = False
in_table = False
in_framestats = False

gfxinfo = []
framestats = []

num_cols = 0

# Parse input

for line in fileinput.input():

    stripped_line = line.strip()

    if in_profile_section:

        if stripped_line == "View hierarchy:":
            in_profile_section = False
            in_activity = False
            in_table = False

            if len(gfxinfo) == 0 and len(framestats) > 0: # only framestats

                if not has_header:
                    print("start", "input", "animations", "traversals", "draw", "sync", "gpu", sep="\t")

                    has_header = True

                map(lambda frame: print(*frame, sep="\t"), map(parse_framestats, framestats))

            elif len(gfxinfo) > 0 and len(framestats) == 0: # only gfxinfo

                if not has_header:
                    # https://io2015codelabs.appspot.com/codelabs/android-performance-profile-gpu-rendering#5
                    if gfxinfo[0].count("\t") == 2:
                        print("draw", "execute", "process", sep="\t")
                    elif gfxinfo[0].count("\t") == 3: # Prepare only exists on Lollipop and above
                        print("draw", "prepare", "execute", "process", sep="\t")

                    has_header = True

                map(print, gfxinfo)

            elif len(gfxinfo) > 0 and len(gfxinfo) == len(framestats): # both

                if not has_header:
                    print("start", "input", "animations", "traversals", "draw", "sync", "execute", "process", sep="\t")

                    has_header = True

                for gfx, cpu in zip(gfxinfo, framestats):
                    try:
                        # ignore "gpu" and append "execute" and "process"
                        print(*(parse_framestats(cpu, True)[:-2] + tuple(list(map(float, gfx.split("\t")))[-3:])), sep="\t")
                    except ValueError:
                        # only use gfx data if framestats is invalid
                        print(*([0, 0, 0, 0] + map(float, gfx.split("\t"))), sep="\t")

            gfxinfo = []
            framestats = []

        else:
            if stripped_line.count("/") == 2:
                if in_activity:
                    in_activity = False
                elif "visibility=0" in stripped_line or "visibility" not in stripped_line:
                    # Choose the activity that is visible or all activities
                    in_activity = True
            elif in_activity:
                table_cols = stripped_line.count("\t")

                if in_table and table_cols == num_cols and "Execute" not in stripped_line:
                    gfxinfo.append(stripped_line)
                elif "Execute" in stripped_line:
                    in_table = True
                    num_cols = table_cols
                elif stripped_line == "---PROFILEDATA---":
                    in_framestats = not in_framestats
                elif in_framestats and "Flags" not in stripped_line:
                    framestats.append(stripped_line)

    elif stripped_line == "Profile data in ms:":
        in_profile_section = True