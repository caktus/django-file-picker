#!/usr/bin/env python
import os
import sys
from django.core.management import execute_manager

sys.path.pop(0)
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(PROJECT_ROOT))

settings_specified = any([arg.startswith('--settings=') for arg in sys.argv])
if not settings_specified and len(sys.argv) >= 2:
    print 'NOTICE: using default local_settings'
    sys.argv.append('--settings=sample_project.local_settings')

try:
    import sample_project.settings
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'local_settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

from django.core.management import execute_manager
if __name__ == "__main__":
    execute_manager(sample_project.settings)
