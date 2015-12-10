from urllib.parse import urlencode

from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper

from testsuite_app.models import *


class TestsuiteView(TemplateView):
    "Testsuite download page"
    template_name = "testsuite.html"

    def get(self, request, *args, **kwargs):
        downloads = []
        # from testsuite_app.models.epub import Epub
        # epubs = Epub.objects.all()
        # for epub in epubs:
        #     dl = {"label": epub.title, "link": "{0}{1}".format(settings.EPUB_URL, os.path.basename(epub.source))}
        #     downloads.append(dl)
        # dl = {"label": "All Testsuite Documents (zip)", "link": "{0}TestSuiteDocuments.zip".format(settings.EPUB_URL)}
        # downloads.append(dl)
        return render(request, self.template_name, {'downloads': downloads})

