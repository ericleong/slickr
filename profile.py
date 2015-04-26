#!/usr/bin/env python
import sys
import fileinput

in_profile_section = False
in_activity = False
in_table = False

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
                elif "visibility=0" in stripped_line: # Choose the activity that is visible
                    in_activity = True
            elif in_activity:
                if in_table and stripped_line.count('\t') == 3 and 'Draw' not in stripped_line:
                    print stripped_line
                elif 'Draw' in stripped_line:
                    # print stripped_line
                    in_table = True

    elif stripped_line == "Profile data in ms:":
        in_profile_section = True