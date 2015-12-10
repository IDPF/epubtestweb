from urllib.parse import urlencode

from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages

from testsuite_app.models import *
from testsuite_app.forms import *
from testsuite import settings


class ManageView(TemplateView):
    template_name = "manage.html"

    def get(self, request, *args, **kwargs):
        testsuite = TestSuite.objects.get_most_recent_testsuite(common.TESTSUITE_TYPE_DEFAULT)
        if len(request.user.first_name) > 0 or len(request.user.last_name) > 0:
            display_name = "{0} {1}".format(request.user.first_name, request.user.last_name)
            display_name = display_name.strip()
        reading_systems = ReadingSystem.objects.all()
        return render(request, self.template_name,
            {'reading_systems': reading_systems, "testsuite_date": testsuite.version_date})

