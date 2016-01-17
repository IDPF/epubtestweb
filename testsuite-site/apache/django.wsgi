import os,sys

apache_configuration = os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace)
sys.path.append('/home/djangoweb/epubtest.org-version1/epubtestweb/testsuite-site')
sys.path.append('/home/djangoweb/epubtest.org-version1/epubtestweb')
sys.path.append('/home/djangoweb')

os.environ['DJANGO_SETTINGS_MODULE'] = 'testsuite.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

