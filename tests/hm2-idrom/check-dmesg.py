#!/usr/bin/env python3

#
# Here's the kind of output we're looking for:
# 
# [87900.133189] hm2: loading Mesa HostMot2 driver version 0.14
# [87900.157678] hm2_test: loading HostMot2 test driver
# [87900.157715] hm2: no firmware specified in config modparam!  the board had better have firmware configured already, or this won't work
# [87900.157724] hm2/hm2_test.0: invalid cookie, got 0x00000000, expected 0x55AACAFE
# [87900.157726] hm2/hm2_test.0: FPGA failed to initialize, or unexpected firmware?
# [87900.157731] hm2_test.0: hm2_test fails HM2 registration
# [87900.236858] hm2: unloading

import os
import sys
import re
import hal

hm2_test_load = 'loading HostMot2 test driver'
hm2_test_unload = 'hm2_test.0: hm2_test fails HM2 registration'

sought_error = sys.argv[1]
if sought_error == None:
    print("supply an error message on the command line!")
    sys.exit(1)


# is this how you do enum in python?
LOOKING_FOR_LOAD, LOOKING_FOR_ERROR = list(range(2))

if hal.is_kernelspace:
    dmesg = os.popen('dmesg')
else:
    dmesg = open("halrun-stderr")

output = ""

state = LOOKING_FOR_LOAD
result = 1
while 1:
    line = dmesg.readline()
    output += line
    if line == "": break  # eof

    if state == LOOKING_FOR_LOAD:
        if line.find(hm2_test_load) < 0: continue
        state = LOOKING_FOR_ERROR
        result = 1  # assume it's the wrong error for now
        continue

    if state == LOOKING_FOR_ERROR:
        if re.search(sought_error, line) != None:
            result = 0
            state = LOOKING_FOR_LOAD
            continue;

        if line.find(hm2_test_unload) >= 0:
            state = LOOKING_FOR_LOAD


if (result == 0):
    print(sought_error)
else:
    print("test pattern %s did not produce error '%s'" % (os.getenv("TEST_PATTERN"), sought_error))
    print("actual output:")
    print(output)

sys.exit(result)

