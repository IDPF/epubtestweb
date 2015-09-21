from urllib.parse import urlencode

from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
import os
from testsuite_app.models import ReadingSystemVersion, TestSuite, Test, Result, common, Evaluation
from testsuite import settings
from testsuite_app import helper_functions
from testsuite_app import permissions
from .view_helper import *

# confirm deleting a reading system
class ConfirmDeleteRSView(TemplateView):
    template_name = "confirm_delete.html"
    def get(self, request, *args, **kwargs):
        try:
            rs = ReadingSystemVersion.objects.get(id=kwargs['pk'])
        except ReadingSystemVersion.DoesNotExist:
            return render(request, "404.html", {})

        can_delete = permissions.user_can_delete_reading_system(request.user, rs)
        if can_delete == False:
            messages.add_message(request, messages.INFO, 'You do not have permission to delete that reading system.')
            return redirect("/manage/")
        
        rs_desc = "{0} {1} {2} {3}".format(rs.name, rs.version, rs.locale, rs.operating_system)
        return render(request, self.template_name,
            {"header": 'Confirm delete reading system',
            "warning": "You are about to delete '{0}'. Proceed?".format(rs_desc),
            "confirm_url": "/rs/{0}/".format(kwargs['pk']),
            "redirect_url": "/manage/"
            })

# confirm deleting an accessibility configuration
class ConfirmDeleteAccessibilityConfigurationView(TemplateView):
    template_name = "confirm_delete.html"
    def get(self, request, *args, **kwargs):
        try:
            rs = ReadingSystem.objects.get(id=kwargs['pk'])
        except ReadingSystem.DoesNotExist:
            return render(request, "404.html", {})

        try:
            rset = Evaluation.objects.get(id=kwargs['rset'])
        except Evaluation.DoesNotExist:
            return render(request, "404.html", {})

        can_delete = permissions.user_can_delete_accessibility_result_set(request.user, rset)
        if can_delete == False:
            messages.add_message(request, messages.INFO, 'You do not have permission to delete that accessibility evaluation.')
            return redirect("/manage/")
        
        metadata = rset.get_metadata()
        if metadata != None:
            rs_desc = "{0} for {1}".format(metadata.assistive_technology, rs.name)
        else:
            rs_desc = "Accessibility configuration for {0}".format(rs.name)

        return render(request, self.template_name,
            {"header": 'Confirm delete accessibility evaluation',
            "warning": "You are about to delete '{0}'. Proceed?".format(rs_desc),
            "confirm_url": "/rs/{0}/accessibility/{1}".format(kwargs['pk'], kwargs['rset']),
            "redirect_url": "/rs/{0}/eval/accessibility".format(kwargs['pk'])
            })

