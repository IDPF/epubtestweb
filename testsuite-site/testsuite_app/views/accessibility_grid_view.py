from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

from testsuite_app.models import *


class AccessibilityGridView(TemplateView):
    template_name = "accessibility_grid.html"

    def get(self, request, *args, **kwargs):
        testsuite = TestSuite.objects.get_most_recent_testsuite(common.TESTSUITE_TYPE_ACCESSIBILITY)
        categories = Category.objects.filter(testsuite = testsuite)
        testsuite.categories = categories
            
        reading_systems = ReadingSystem.objects.all()
        evaluations = []
        for reading_system in reading_systems:
            evals = reading_system.get_evaluations(testsuite)
            evaluations.extend(evals)    
        
        return render(request, self.template_name,{'evaluations': evaluations, 'testsuite': testsuite})