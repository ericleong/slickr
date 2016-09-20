#!/usr/bin/env python
from __future__ import division
from __future__ import print_function
import sys
import fileinput
import os

def parse_framestats(line, valid_only=False, logcat_headers=[], fd2=None):

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

        vsync = framestats[1]

        if len(logcat_headers) > 0 and fd2:
            if vsync in logcat:
                print(*[logcat[vsync][field] if field in logcat[vsync] else 0 for field in logcat_headers], sep="\t", file=fd2)
            else:
                print(*([0] * len(logcat_headers)), sep="\t", file=fd2)

    elif valid_only:
        raise ValueError("Invalid frame.")

    return start, handle_input, animations, traversals, draw, sync, gpu

# Globals

has_header = False
has_logcat_header = False

in_profile_section = False
in_activity = False
in_table = False
in_framestats = False
in_logcat = False

gfxinfo = []
framestats = []
logcat = {}
logcat_headers = []

num_cols = 0

# fd2 = os.fdopen(os.open("test", os.O_WRONLY | os.O_CREAT | os.O_APPEND))
# fd2 = open("app_data.txt", "w")
fd2 = sys.stderr

# Parse input

for line in fileinput.input():

    stripped_line = line.strip()

    if stripped_line == "Applications Graphics Acceleration Info:":
        in_logcat = False
    elif in_logcat:
        data = line[line.rfind(": ") + 2:].split("\t")

        try:
            time = int(data[0])
            field = data[1].strip()
            value = int(data[2].strip()) / 1000000

            if field not in logcat_headers:
                logcat_headers.append(field)

            if time in logcat:
                logcat[time][field] = value
            else:
                logcat[time] = {field: value}
        except IndexError:
            pass
        except ValueError:
            pass

    elif stripped_line == "--------- beginning of main":
        in_logcat = True
    elif in_profile_section:

        if stripped_line == "View hierarchy:":
            in_profile_section = False
            in_activity = False
            in_table = False

            if len(framestats) > 0: # only framestats

                if not has_header:
                    print("start", "input", "animations", "traversals", "draw", "sync", "gpu", sep="\t")
                    has_header = True

                if not has_logcat_header:
                    print(*logcat_headers, sep="\t", file=fd2)
                    has_logcat_header = True

                list(map(lambda frame: print(*frame, sep="\t"), list(map(lambda f: parse_framestats(f, False, logcat_headers, fd2), framestats))))

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
                        if not has_logcat_header:
                            print(*logcat_headers, sep="\t", file=fd2)
                            has_logcat_header = True

                        # ignore "gpu" and append "execute" and "process"
                        print(*(parse_framestats(cpu, True, logcat_headers, fd2)[:-2] + tuple(list(map(float, gfx.split("\t")))[-3:])), sep="\t")
                    except ValueError:
                        # only use gfx data if framestats is invalid
                        print(*([0, 0, 0, 0] + list(map(float, gfx.split("\t")))), sep="\t")
                        pass

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