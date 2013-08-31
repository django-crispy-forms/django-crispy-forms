#!/usr/bin/env python

import os
import sys

cmds = [
    'python runtests_bootstrap.py',
    'python runtests_bootstrap3.py',
    'python runtests_uniform.py',
]

for cmd in cmds:
    retval = os.system(cmd)
    if retval:
        sys.exit(1)
