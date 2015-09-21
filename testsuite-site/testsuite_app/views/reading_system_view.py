from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
import os

from testsuite_app.models.category import Category
from testsuite_app.models.evaluation import Evaluation
from testsuite_app.models.testsuite import TestSuite
from testsuite_app.models.reading_system import ReadingSystemVersion
from testsuite_app.models.feature import Feature
from testsuite_app.models.test import Test
from testsuite_app.models import common

class ReadingSystemView(UpdateView):
    template_name = "reading_system.html"

    def get(self, request, *args, **kwargs):

        try:
            reading_system_version = ReadingSystemVersion.objects.get(id=kwargs['pk'])
        except ReadingSystemVersion.DoesNotExist:
            return render(request, "404.html", {})

        try:
            testsuite = TestSuite.objects.get(id=kwargs['testsuite_id'])
        except TestSuite.DoesNotExist:
            return render(request, "404.html", {})            
        
        evaluations = reading_system_version.get_evaluations(testsuite)
        categories = testsuite.get_categories()

        for category in categories:
            features = Feature.objects.filter(category = category)
            if features != None:
                category.features = features
                for feature in features:
                    tests = Test.objects.filter(feature = feature)
                    if tests != None:
                        feature.tests = tests

        return render(request, self.template_name,{'reading_system_version': reading_system_version, 
            'evaluations': evaluations, 'categories': categories, 'testsuite': testsuite})