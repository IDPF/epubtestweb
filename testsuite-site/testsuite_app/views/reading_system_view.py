from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

from testsuite_app.models import *

class ReadingSystemView(TemplateView):
    def delete(self, request, *args, **kwargs):
        print("HELLO")
        try:
            reading_system = ReadingSystem.objects.get(id=kwargs['pk'])
        except ReadingSystem.DoesNotExist:
            print("not found")
            return render(request, "404.html", {})

        if permissions.user_can_edit_reading_system(request.user, reading_system) == False:
            messages.add_message(request, messages.INFO, 'You do not have permission to delete that reading system.')
            return redirect("/manage/")
        
        reading_system.delete_associated()
        reading_system.delete()
        messages.add_message(request, messages.INFO, "Reading system deleted")
        return HttpResponse(status=204)
    