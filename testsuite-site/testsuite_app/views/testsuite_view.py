from urllib.parse import urlencode

from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper

from testsuite_app.models import *

from testsuite import settings

class TestsuiteView(TemplateView):
    "Testsuite download page"
    template_name = "testsuite.html"

    def get(self, request, *args, **kwargs):
        downloads = []
        epubs = Epub.objects.all()
        return render(request, self.template_name, {"epubs": epubs, "epub_downloads_url": settings.epub_downloads_url})

