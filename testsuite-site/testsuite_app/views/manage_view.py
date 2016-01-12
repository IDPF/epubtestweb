from urllib.parse import urlencode

from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages

from testsuite_app.models import *


class ManageView(TemplateView):
    template_name = "manage.html"

    def get(self, request, *args, **kwargs):
        testsuites = TestSuite.objects.get_testsuites()
        reading_systems = ReadingSystem.objects.filter(user = request.user)
        evaluations = Evaluation.objects.filter(user = request.user)
        for evaluation in evaluations:
            if evaluation.has_flagged_results() == True:
                print("FLAG")
                evaluation.flagged = True
        return render(request, self.template_name,
            {'evaluations': evaluations, 'reading_systems': reading_systems, 'testsuites': testsuites})

