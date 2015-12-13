from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

from testsuite_app.models import *

class ArchiveGridView(TemplateView):
    template_name = "grid.html"

    def get(self, request, *args, **kwargs):

        try:
            testsuite = TestSuite.objects.get(testsuite_id=kwargs['testsuite_id'])
        except TestSuite.DoesNotExist:
            return render(request, "404.html", {})

        categories = Category.objects.filter(testsuite = testsuite)
        testsuite.categories = categories
        
        reading_systems = ReadingSystem.objects.all()
        evaluations = []
        for reading_system in reading_systems:
            evals = reading_system.get_evaluations(testsuite, is_archived = True)
            evaluations.extend(evals)    
        
        return render(request, self.template_name,{'evaluations': evaluations, 'testsuite': testsuite, "is_archive_view": True})