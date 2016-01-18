import os,sys

apache_configuration = os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/home/djangoweb/epubtest.org/epubtestweb/env/local/lib/python3.4/site-packages')


sys.path.append(workspace)
sys.path.append('/home/djangoweb/epubtestweb/testsuite-site')
sys.path.append('/home/djangoweb/epubtestweb')
sys.path.append('/home/djangoweb')

os.environ['DJANGO_SETTINGS_MODULE'] = 'testsuite.settings'

# Activate your virtual env
activate_env=os.path.expanduser("/home/djangoweb/epubtest.org/epubtestweb/env/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


