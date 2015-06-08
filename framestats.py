#!/usr/bin/env python
from __future__ import division
from __future__ import print_function
import sys
import fileinput

has_header = False

in_profile_section = False
in_activity = False
in_framestats = False

for line in fileinput.input():

    stripped_line = line.strip()

    if in_profile_section:

        if stripped_line == "View hierarchy:":
            in_profile_section = False
            in_activity = False
        else:
            if stripped_line.count("/") == 2:
                if in_activity:
                    in_activity = False
                elif "visibility=0" in stripped_line or "visibility" not in stripped_line:
                    # Choose the activity that is visible or all activities
                    in_activity = True
            elif in_activity:
                table_cols = stripped_line.count("\t")

                if stripped_line == "---PROFILEDATA---":
                    in_framestats = not in_framestats
                elif in_framestats:
                    if not has_header:
                        print("start", "input", "animations", "traversals", "draw", "sync", "gpu", sep="\t")
                        has_header = True

                    # http://developer.android.com/preview/testing/performance.html#fs-data-format
                    framestats = stripped_line.split(",")

                    # HANDLE_INPUT_START - INTENDED_VSYNC
                    start = (int(framestats[5]) - int(framestats[1])) / 1000000

                    # ANIMATION_START - HANDLE_INPUT_START
                    handle_input = (int(framestats[6]) - int(framestats[5])) / 1000000

                    # PERFORM_TRAVERSALS_START - ANIMATION_START
                    animations = (int(framestats[7]) - int(framestats[6])) / 1000000

                    # DRAW_START - PERFORM_TRAVERSALS_START
                    traversals = (int(framestats[8]) - int(framestats[7])) / 1000000

                    # SYNC_START - DRAW_START
                    draw = (int(framestats[9]) - int(framestats[8])) / 1000000

                    # ISSUE_DRAW_COMMANDS_START - DRAW_START
                    sync = (int(framestats[10]) - int(framestats[9])) / 1000000

                    # FRAME_COMPLETED - ISSUE_DRAW_COMMANDS_START
                    gpu_work = (int(framestats[12]) - int(framestats[10])) / 1000000

                    print(start, handle_input, animations, traversals, draw, sync, gpu_work, sep="\t")

    elif stripped_line == "Profile data in ms:":
        in_profile_section = True