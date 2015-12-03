from urllib.parse import urlencode

from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
import os
from testsuite_app.models import ReadingSystem, TestSuite, Test, Result, common, Evaluation
from testsuite_app.forms import ResultFormSet, EvaluationMetadataForm
from testsuite import settings
from testsuite_app import helper_functions
from testsuite_app import permissions
from .view_helper import *

class EditResultSetView(UpdateView):
    "Edit reading system evaluation"
    template_name = "evaluation_form.html"

    def get(self, request, *args, **kwargs):
        try:
            rs = ReadingSystem.objects.get(id=kwargs['pk'])
        except ReadingSystem.DoesNotExist:
            return render(request, "404.html", {})

        result_set = rs.get_default_result_set()
        if permissions.user_can_edit_reading_system(request.user, rs):
            if result_set == None:
                result_set = Evaluation.objects.create_result_set(rs, TestSuite.objects.get_most_recent_testsuite(), rs.user)
        else:
            messages.add_message(request, messages.INFO, 'You do not have permission to create an accessibility evaluation.')
            return redirect("/manage/")

        
        action_url = "/rs/{0}/eval/".format(rs.id)
        testsuite = result_set.testsuite
        category_pages = []
        top_level_categories = testsuite.get_top_level_categories()
        
        # default to the first category
        cat = top_level_categories[0]

        cat_option = '-1'
        if kwargs.has_key('cat'):
            cat_option = kwargs['cat']

        for c in top_level_categories:
            # check if we are starting at a different category
            if c.id == int(cat_option):
                cat = c
            # collect category list data for other categories
            category_pages.append({"link": "{0}{1}".format(action_url, c.id), "name": c.name, "id": c.id})

        idx = 0
        next = ''
        for c in category_pages:
            if c['id'] == cat.id:
                if len(category_pages) > idx + 1:
                    next = category_pages[idx + 1]['link']
                    break
            idx += 1

        data = helper_functions.category_to_dict(cat)
        results_form = ResultFormSet(instance = result_set, queryset=result_set.get_results_for_category(cat))
        
        can_edit = permissions.user_can_edit_reading_system(request.user, rs)
        if can_edit == False:
            messages.add_message(request, messages.INFO, 'You do not have permission to edit that evaluation.')
            return redirect("/manage/")

        return render(request, self.template_name,
            {'result_set': result_set, 'results_form': results_form, 'data': data,
            'rs': rs, "action_url": action_url, "category_pages": category_pages, 'next': next})

    def post(self, request, *args, **kwargs):
        try:
            rs = ReadingSystem.objects.get(id=kwargs['pk'])
        except ReadingSystem.DoesNotExist:
            return render(request, "404.html", {})

        can_edit = permissions.user_can_edit_reading_system(request.user, rs)
        if can_edit == False:
            messages.add_message(request, messages.INFO, 'You do not have permission to edit that evaluation.')
            return redirect("/manage/")
        result_set = rs.get_default_result_set()
        formset = ResultFormSet(request.POST, instance=result_set)
        
        formset.save()
        result_set.save()
        
        # if we are auto-saving, don't redirect
        if not request.POST.has_key('auto') or request.POST['auto'] == "false":
            if 'save_continue' in request.POST and request.POST.has_key('next'):
                next = request.POST['next']
                print("Going to next section: {0}".format(next))
                # go to next section
                return redirect('{0}/'.format(next))
            else:
                # go back to the manage page
                return redirect('/manage/')
