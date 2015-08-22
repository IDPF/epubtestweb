from urllib import urlencode

from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
import os
from testsuite.models import ReadingSystem, TestSuite, Test, Result, common, Evaluation, ATMetadata
from testsuite.forms import ReadingSystemForm, ResultFormSet, ResultSetMetadataForm
from testsuite import settings
from testsuite import helper_functions
from testsuite import permissions
from view_helper import *

class EditAccessibilityResultSetView(UpdateView):
    "Edit reading system accessibility evaluation; create if does not exist"
    template_name = "accessibility_evaluation_form.html"

    def get(self, request, *args, **kwargs):
        try:
            rs = ReadingSystem.objects.get(id=kwargs['pk'])
        except ReadingSystem.DoesNotExist:
            return render(request, "404.html", {})

        testsuite = TestSuite.objects.get_most_recent_testsuite_of_type(common.TESTSUITE_TYPE_ACCESSIBILITY)
        create_flag = False
        if kwargs.has_key('rset'):
            try:
                rset = Evaluation.objects.get(id=kwargs['rset'])
            except Evaluation.DoesNotExist:
                return render(request, "404.html", {})
        else:
            if permissions.user_can_create_accessibility_result_set(request.user, rs):
                create_flag = True
                rset = Evaluation.objects.create_result_set(rs, testsuite, request.user)
                # add dummy metadata
                rset.add_metadata("", common.INPUT_TYPE_KEYBOARD, False, False)
                m = rset.get_metadata()
                print "meta {0}".format(m)
            else:
                messages.add_message(request, messages.INFO, 'You do not have permission to create an accessibility evaluation.')
                return redirect("/manage/")

        action_url = "/rs/{0}/eval/accessibility/{1}".format(rs.id, rset.id)
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
        next = "/rs/{0}/eval/accessibility/".format(rs.id)

        data = helper_functions.category_to_dict(cat)
        result_set = rs.get_result_set_by_id(rset.id)
        results_form = ResultFormSet(instance = result_set, queryset=result_set.get_results_for_category(cat))
        at_type_form = ResultSetMetadataForm(instance = result_set.get_metadata())

        if create_flag == False:
            can_edit = permissions.user_can_edit_accessibility_result_set(request.user, result_set)
            if can_edit == False:
                messages.add_message(request, messages.INFO, 'You do not have permission to edit that evaluation.')
                return redirect("/manage/")

        return render(request, self.template_name,
            {'results_form': results_form, 'data': data,
            'rs': rs, "action_url": action_url, "category_pages": category_pages, 'next': next, 'result_set': result_set,
            'result_set_metadata_form': at_type_form.as_ul()})

    def post(self, request, *args, **kwargs):
        try:
            rs = ReadingSystem.objects.get(id=kwargs['pk'])
        except ReadingSystem.DoesNotExist:
            return render(request, "404.html", {})

        try:
            rset = Evaluation.objects.get(id=kwargs['rset'])
        except Evaluation.DoesNotExist:
            return render(request, "404.html", {})

        can_edit = permissions.user_can_edit_accessibility_result_set(request.user, rset)
        if can_edit == False:
            messages.add_message(request, messages.INFO, 'You do not have permission to edit that evaluation.')
            return redirect("/manage/")
        result_set = rset 
        formset = ResultFormSet(request.POST, instance=result_set)

        metadata = result_set.get_metadata()
        print metadata
        result_set_meta_form = EvaluationMetadataForm(request.POST, instance = result_set.get_metadata())
        
        formset.save()
        result_set.save()
        result_set_meta_form.save()

        return redirect("/rs/{0}/eval/accessibility/".format(rs.id))


