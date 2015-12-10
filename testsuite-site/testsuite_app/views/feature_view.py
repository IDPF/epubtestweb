from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

from testsuite_app.models import *

class FeatureView(TemplateView):
    "A single feature"
    template_name = "feature.html"

    def get(self, request, *args, **kwargs):
        try:
            feature = Feature.objects.get(feature_id=kwargs['feature_id'])
        except Feature.DoesNotExist:
            return render(request, "404.html", {})

        tests = feature.get_tests()

        testsuite = feature.category.testsuite
        reading_systems = ReadingSystem.objects.all()
        evaluations = []
        for reading_system in reading_systems:
            evals = reading_system.get_evaluations(testsuite)
            evaluations.extend(evals)

        return render(request, self.template_name,{'evaluations': evaluations, 'feature': feature, 'tests': tests})