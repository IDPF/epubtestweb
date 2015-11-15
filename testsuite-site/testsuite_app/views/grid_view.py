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
from testsuite_app.models.reading_system import ReadingSystemVersion, ReadingSystem
from testsuite_app.models import common

class GridView(UpdateView):
    template_name = "grid.html"

    def get(self, request, *args, **kwargs):
        testsuite = TestSuite.objects.get_most_recent_testsuite(common.TESTSUITE_TYPE_DEFAULT)
        categories = Category.objects.filter(testsuite = testsuite)
        testsuite.categories = categories
        
        reading_systems = ReadingSystem.objects.all()
        reading_systems_ = []
        for reading_system in reading_systems:
            # make sure there's an evaluation for this testsuite
            reading_system_version = reading_system.get_most_recent_version_with_evaluation(testsuite)
            if reading_system_version != None:
                reading_systems_.append(reading_system)
        
        return render(request, self.template_name,{'reading_systems': reading_systems_, 'testsuite': testsuite})