from urllib.parse import urlencode

from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
import os
from testsuite_app.models import *
from testsuite import settings
from testsuite_app import helper_functions
from testsuite_app import permissions
from .view_helper import *

class ConfirmDeleteReadingSystemView(TemplateView):
    template_name = "confirm_delete.html"
    def get(self, request, *args, **kwargs):
        try:
            reading_system = ReadingSystem.objects.get(id=kwargs['pk'])
        except ReadingSystem.DoesNotExist:
            return render(request, "404.html", {})

        if permissions.user_can_edit_reading_system(request.user, reading_system) == False:
            messages.add_message(request, messages.INFO, 'You do not have permission to delete that reading system.')
            return redirect("/manage/")
        
        rs_desc = "{0} {1} {2} {3}".format(reading_system.name, reading_system.version, \
            reading_system.operating_system, reading_system.operating_system_version)
        return render(request, self.template_name,
            {"header": 'Confirm delete reading system',
            "warning": "You are about to delete '{0}'. Proceed?".format(rs_desc),
            "confirm_url": "/rs/{}/".format(kwargs['pk']),
            "redirect_url": "/manage/"
            })


class ConfirmDeleteEvaluationView(TemplateView):
    template_name = "confirm_delete.html"
    def get(self, request, *args, **kwargs):
        try:
            evaluation = Evaluation.objects.get(id=kwargs['pk'])
        except Evaluation.DoesNotExist:
            return render(request, "404.html", {})

        can_delete = permissions.user_can_edit_evaluation(request.user, evaluation)
        if can_delete == False:
            messages.add_message(request, messages.INFO, 'You do not have permission to delete this evaluation.')
            return redirect("/manage/")

        reading_system = evaluation.reading_system
        rs_desc = "{0} {1} {2} {3}".format(reading_system.name, reading_system.version, \
            reading_system.operating_system, reading_system.operating_system_version)
        
        return render(request, self.template_name,
            {"header": 'Confirm delete evaluation',
            "warning": "You are about to delete an evaluation for '{}'. Proceed?".format(rs_desc),
            "confirm_url": "/evaluation/{}/".format(evaluation.id),
            "redirect_url": "/manage/"
            })

