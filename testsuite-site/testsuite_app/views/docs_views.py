from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

class InstructionsForEvaluatorsView(TemplateView):
    template_name = "instructions_for_evaluators.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class InstructionsForAccessibilityEvaluatorsView(TemplateView):
    template_name = "instructions_for_accessibility_evaluators.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class CallForModeratorsView(TemplateView):
    template_name = "call_for_moderators.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)