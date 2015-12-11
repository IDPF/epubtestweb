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
from testsuite_app.forms import *
from testsuite import settings
from testsuite_app import helper_functions
from testsuite_app import permissions
from .view_helper import *


class EditAccessibilityConfigurationsView(TemplateView):
    "Lists evaluated configurations for a single reading system"
    template_name = "accessibility_configurations.html"

    def get(self, request, *args, **kwargs):
        try:
            rs = ReadingSystem.objects.get(id=kwargs['pk'])
        except ReadingSystem.DoesNotExist:
            return render(request, "404.html", {})

        can_view = permissions.user_can_view_reading_system(request.user, rs, 'rs')
        if can_view == False:
            messages.add_message(request, messages.INFO, 'You do not have permission to view that reading system.')
            return redirect("/")

        result_sets = rs.get_accessibility_result_sets()

        return render(request, self.template_name, {'rs': rs, 'result_sets': result_sets, 'edit': True})


class AccessibilityReadingSystemView(TemplateView):
    "Details for a single reading system's accessibility evaluation"
    template_name = "reading_system_accessibility.html"

    def get(self, request, *args, **kwargs):
        try:
            rs = ReadingSystem.objects.get(id=kwargs['pk'])
        except ReadingSystem.DoesNotExist:
            return render(request, "404.html", {})

        try:
            rset = Evaluation.objects.get(id=kwargs['rset'])
        except Evaluation.DoesNotExist:
            return render(request, "404.html", {})

        can_view = permissions.user_can_view_accessibility_result_set(request.user, rset)
        if can_view == False:
            messages.add_message(request, messages.INFO, 'You do not have permission to view that accessibility evaluation.')
            return redirect("/manage".format(rs.id))

        ts = TestSuite.objects.get_most_recent_testsuite_of_type(common.TESTSUITE_TYPE_ACCESSIBILITY)
        data = helper_functions.testsuite_to_dict(ts)
        return render(request, self.template_name, {'rs': rs, 'data': data, 'result_set': rset})

    def delete(self, request, *args, **kwargs):
        print("DELETING ACCESSIBILITY CONFIG")
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
        
        rset.delete_associated()
        rset.delete()
        messages.add_message(request, messages.INFO, "Accessibility evaluation deleted")
        return HttpResponse(status=204)

