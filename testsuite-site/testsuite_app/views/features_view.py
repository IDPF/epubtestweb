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

class FeaturesView(UpdateView):
    "All features, organized by category"
    template_name = "features.html"

    def get(self, request, *args, **kwargs):

        # TODO TEMPORARY
        #from testsuite_app.helper_functions import force_score_refresh
        #force_score_refresh()
        

        testsuites = TestSuite.objects.get_most_recent_testsuites()
        for testsuite in testsuites:
            categories = testsuite.get_categories()
            testsuite.categories = categories
            for category in categories:
                features = category.get_features()
                category.features = features 
        return render(request, self.template_name,{'testsuites': testsuites})