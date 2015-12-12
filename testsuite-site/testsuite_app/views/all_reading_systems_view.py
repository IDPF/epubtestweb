from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

from testsuite_app.models import *

class AllReadingSystemsView(TemplateView):
    template_name = "all_reading_systems.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser == False:
            return render(request, "404.html", {})
        
        reading_systems = ReadingSystem.objects.all()
        return render(request, self.template_name,{"reading_systems": reading_systems})