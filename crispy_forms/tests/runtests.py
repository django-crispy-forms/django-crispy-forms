#!/usr/bin/env python

import os
import sys
import django

if django.VERSION < (1,6):
    cmds = [
        'python runtests_bootstrap_legacy.py',
        'python runtests_bootstrap3_legacy.py',
        'python runtests_uniform_legacy.py',
    ]
else:
    cmds = [
        'python runtests_bootstrap.py',
        'python runtests_bootstrap3.py',
        'python runtests_uniform.py',
    ]

for cmd in cmds:
    retval = os.system(cmd)
    if retval:
        sys.exit(1)
