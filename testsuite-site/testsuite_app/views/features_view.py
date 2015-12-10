from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

from testsuite_app.models import *

class FeaturesView(TemplateView):
    "All features, organized by category"
    template_name = "features.html"

    def get(self, request, *args, **kwargs):

        testsuites = TestSuite.objects.get_most_recent_testsuites()
        for testsuite in testsuites:
            categories = testsuite.get_categories()
            testsuite.categories = categories
            for category in categories:
                features = category.get_features()
                category.features = features 
        return render(request, self.template_name,{'testsuites': testsuites})