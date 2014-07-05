from urllib import urlencode

from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
import os
from testsuite_app.models import ReadingSystem, TestSuite, Test, Result, common, ResultSet
from testsuite_app.forms import ReadingSystemForm, ResultFormSet, ResultSetMetadataForm
from testsuite import settings
from testsuite_app import helper_functions
from testsuite_app import permissions
from view_helper import *

class CompareResultsView(TemplateView):
    "Compare results form page"
    template_name = "compare_form.html"
    
    def get(self, request, *args, **kwargs):
        testsuite = TestSuite.objects.get_most_recent_testsuite()
        data = helper_functions.testsuite_to_dict(testsuite)
        action_url = "/compare/"
        return render(request, self.template_name, 
            {"data": data, "action_url": action_url})

    def post(self, request, *args, **kwargs):
        view_option = request.GET.get('view', 'simple')
        test_ids = request.POST.getlist('test-selected', []) #getlist is a method of django's QueryDict object
        tests = Test.objects.filter(pk__in = test_ids)
        reading_systems = ReadingSystem.objects.filter(visibility = common.VISIBILITY_PUBLIC)
        test_arrays = []
        list_max = 13
        # split the tests up into arrays of 13 for display purposes
        if tests.count() <= list_max:
            test_arrays.append(tests)
        else:
            start = 0
            end = list_max
            for n in range(0, tests.count() / list_max):
                arr = tests[start:end]
                start += list_max
                end += list_max
                test_arrays.append(arr)

            if tests.count() % list_max != 0:
                mod = (tests.count() % list_max)
                start = tests.count()-mod
                arr = tests[start:tests.count()]
                test_arrays.append(arr)

        return render(request, "compare_results.html", 
            {'test_arrays': test_arrays, 'reading_systems': reading_systems, "view_option": view_option})

