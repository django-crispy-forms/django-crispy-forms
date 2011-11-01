"""
Backwards-compatible for django-crispy-forms versions previous to 0.9.0
Helpers.py was split into 3 different files in version 0.9.0: helper.py, layout.py and util.py
In order to keep former imports working this file is kept. 

This usage will be deprecated and will be removed for django-crispy-forms 1.1.0
"""

import warnings

warnings.warn("Importing from helpers is deprecated; import from helper or layout instead.", DeprecationWarning)

from helper import *
from layout import *
