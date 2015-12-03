from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
import os

from testsuite_app.models.testsuite import TestSuite
from testsuite_app.models.category import Category
from testsuite_app.models.feature import Feature
from testsuite_app.models.test import Test
from testsuite_app.models import common
from testsuite_app.models.reading_system import ReadingSystem
from testsuite_app.models.evaluation import Evaluation

class FeatureView(UpdateView):
    "A single feature"
    template_name = "feature.html"

    def get(self, request, *args, **kwargs):
        print(kwargs['pk'])
        try:
            feature = Feature.objects.get(id=kwargs['feature_id'])
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