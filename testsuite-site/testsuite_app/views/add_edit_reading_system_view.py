from urllib.parse import urlencode

from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from testsuite_app.models import *
from testsuite_app.forms import *
from testsuite_app import permissions

class AddEditReadingSystemView(TemplateView):
    template_name = "add_edit_reading_system.html"

    def get(self, request, *args, **kwargs):
        form = None
        title = ""
        action_url = ""
        if "pk" in kwargs.keys(): #kwargs.has_key('pk'):
            try:
                reading_system = ReadingSystem.objects.get(id=kwargs['pk'])
            except:
                return render(request, "404.html", {})
            can_edit = permissions.user_can_edit_reading_system(request.user, reading_system)
            if can_edit == False:
                messages.add_message(request, messages.INFO, 'You do not have permission to edit that reading system.')
                return redirect("/manage/")
            form = ReadingSystemForm(instance = reading_system)
            action_url = request.path #"/rs/{0}/edit/".format(rs.id)
            title = "Edit Reading System"
        else:
            form = ReadingSystemForm()
            # read the query string for initial values
            for fieldname in form.fields.keys():
                value = request.GET.get(fieldname, '')
                form.initial[fieldname] = value
            action_url = request.path #"/rs/new/"
            title = "Add Reading System"
        return render(request, self.template_name, {'reading_system_form': form,
            "title": title, "action_url": action_url})

    def post(self, request, *args, **kwargs):
        form = None
        if "pk" in kwargs.keys(): #kwargs.has_key('pk'):
            try:
                reading_system = ReadingSystem.objects.get(id=kwargs['pk'])
                form = ReadingSystemForm(request.POST, instance = reading_system)
            except ReadingSystem.DoesNotExist:
                return render(request, "404.html", {})
        else:
            form = ReadingSystemForm(request.POST)

        if form.is_valid():
            obj = form.save(commit = False)
            if hasattr(obj, 'user') == False:
                obj.user = request.user
            obj.save()
            return redirect(request.POST.get('next', '/manage/'))
        else:
            messages.add_message(request, messages.INFO, 'Please complete all required fields.')
            clean_data = form.clean()
            qstr = urlencode(clean_data)
            return redirect("{}?{}".format(request.path, qstr))
