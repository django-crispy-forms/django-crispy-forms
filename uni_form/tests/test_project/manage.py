#!/usr/bin/env python
from os.path import join, abspath, dirname
import sys

PROJECT_ROOT = abspath(dirname(__file__))
PROJECT_ROOT = PROJECT_ROOT.replace('uni_form/tests/test_project','')



from django.core.management import execute_manager
from django.core.management import setup_environ, execute_from_command_line

try:
    import settings # Assumed to be in the same directory.
except ImportError:
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)
    
sys.path.insert(0, PROJECT_ROOT)    

for x in  sys.path:
    print >> sys.stderr, x

setup_environ(settings)

if __name__ == "__main__":
    execute_from_command_line()

"""
#!/usr/bin/env python
import sys

from os.path import abspath, dirname, join

try:
    import pinax
except ImportError:
    sys.stderr.write("Error: Can't import Pinax. Make sure you have it installed or use pinax-boot.py to properly create a virtual environment.")
    sys.exit(1)

from django.conf import settings
from django.core.management import setup_environ, execute_from_command_line

try:
    import settings as settings_mod # Assumed to be in the same directory.
except ImportError:
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

# setup the environment before we start accessing things in the settings.
setup_environ(settings_mod)

sys.path.insert(0, join(settings.PINAX_ROOT, "apps"))
sys.path.insert(0, join(settings.PROJECT_ROOT, "apps"))



if __name__ == "__main__":
    execute_from_command_line()
"""    