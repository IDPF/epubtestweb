from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
import os

class IndexView(UpdateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)