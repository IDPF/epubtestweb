from urllib.parse import urlencode

from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse

from testsuite_app.models import *

from testsuite import settings

class TestsuiteView(TemplateView):
    "Testsuite download page"
    template_name = "testsuite.html"

    def get(self, request, *args, **kwargs):
        downloads = []
        testsuites = TestSuite.objects.order_by("-version_date")
        most_recent_update = None
        if testsuites.count() > 0:
            most_recent_update = testsuites[0].version_date
        for testsuite in testsuites:
            testsuite.epubs = testsuite.get_epubs()
        
        return render(request, self.template_name, {"testsuites": testsuites,
            "epub_downloads_url": settings.epub_downloads_url, "most_recent_update": most_recent_update})

