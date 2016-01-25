import os,sys
import site
from django.core.wsgi import get_wsgi_application

apache_configuration = os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/home/djangoweb/epubtest.org/epubtestweb/env/local/lib/python3.4/site-packages')

sys.path.append(workspace)
sys.path.append('/home/djangoweb/epubtest.org/epubtestweb/testsuite-site')
sys.path.append('/home/djangoweb/epubtest.org/epubtestweb')
sys.path.append('/home/djangoweb')

os.environ['DJANGO_SETTINGS_MODULE'] = 'testsuite.settings'

# Activate your virtual env
activate_env=os.path.expanduser("/home/djangoweb/epubtest.org/epubtestweb/env/bin/activate_this.py")
globals = dict( __file__ = activate_env )
exec( open(activate_env).read(), globals )
#execfile(activate_env, dict(__file__=activate_env))



application = get_wsgi_application()


