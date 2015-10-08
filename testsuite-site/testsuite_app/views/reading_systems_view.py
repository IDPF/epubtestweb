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

class ReadingSystemsView(UpdateView):
    template_name = "reading_systems.html"

    def get(self, request, *args, **kwargs):
        testsuites = TestSuite.objects.get_most_recent_testsuites()
        for testsuite in testsuites:
            categories = Category.objects.filter(testsuite = testsuite)
            testsuite.categories = categories
            
        reading_systems = ReadingSystem.objects.all()
        reading_systems_ = []
        for reading_system in reading_systems:
            if reading_system.has_any_evaluations() == True:
                reading_systems_.append(reading_system)    
        
        return render(request, self.template_name,{'reading_systems': reading_systems_, 'testsuite': testsuite})