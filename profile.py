#!/usr/bin/env python
from __future__ import print_function
import sys
import fileinput

in_profile_section = False
in_activity = False
in_table = False
num_cols = 0

for line in fileinput.input():

    stripped_line = line.strip()

    if in_profile_section:

        if stripped_line == "View hierarchy:":
            in_profile_section = False
            in_activity = False
            in_table = False
        else:
            if stripped_line.count("/") == 2:
                if in_activity:
                    in_activity = False
                elif "visibility=0" in stripped_line or "visibility" not in stripped_line:
                    # Choose the activity that is visible or all activities
                    in_activity = True
            elif in_activity:
                table_cols = stripped_line.count("\t")

                if in_table and table_cols == num_cols and "Draw" not in stripped_line:
                    print(stripped_line)
                elif "Draw" in stripped_line:
                    in_table = True
                    num_cols = table_cols

    elif stripped_line == "Profile data in ms:":
        in_profile_section = True