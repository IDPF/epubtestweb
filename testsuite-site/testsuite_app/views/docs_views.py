from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
import os

class InstructionsForEvaluatorsView(UpdateView):
    template_name = "instructions_for_evaluators.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class InstructionsForAccessibilityEvaluatorsView(UpdateView):
    template_name = "instructions_for_accessibility_evaluators.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class CallForModeratorsView(UpdateView):
    template_name = "call_for_moderators.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)