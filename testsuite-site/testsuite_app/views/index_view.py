from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

class IndexView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)