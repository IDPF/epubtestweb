from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

from testsuite_app.models import *

class AddEvaluationView(TemplateView):
    template_name = "add_evaluation.html"

    def get(self, request, *args, **kwargs):
        testsuites = TestSuite.objects.get_testsuites()

        # put the user's own reading systems first in the list, followed by an alphabetical list of all others
        my_reading_systems = ReadingSystem.objects.filter(user = request.user).extra(select={'lower_name':'lower(name)'}).order_by('lower_name')
        other_reading_systems = ReadingSystem.objects.exclude(user = request.user).extra(select={'lower_name':'lower(name)'}).order_by('lower_name')
        # it would be nice to use the queryset join operator here but it alphabetizes the final list and doesn't maintain
        # separation by user
        reading_systems = []
        for rs in my_reading_systems:
            reading_systems.append(rs)
        for rs in other_reading_systems:
            reading_systems.append(rs)

        return render(request, self.template_name,{"testsuites": testsuites, "reading_systems": reading_systems, "users": UserProfile.objects.all(),
            "action_url": request.path})


    def post(self, request, *args, **kwargs):
        reading_system_id = request.POST.getlist('reading_system', [])[0] #getlist is a method of django's QueryDict object
        testsuite_id = request.POST.getlist('testsuite', [])[0] #getlist is a method of django's QueryDict object
        user_id = ""
        print(request.POST.getlist('user', []))
        
        # default to the current user, if no other user was assigned (if they aren't admin, they don't see the assignment field)
        if len(request.POST.getlist('user')) == 0:
            print("Using request user")
            user_id = request.user.id
        else:
            user_id = request.POST.getlist('user', [])[0]


        try:
            reading_system = ReadingSystem.objects.get(id=reading_system_id)
        except ReadingSystem.DoesNotExist:
            messages.add_message(request, messages.INFO, 'Invalid reading system (ID={})'.format(reading_system_id))
            return redirect(request.path)

        try:
            testsuite = TestSuite.objects.get(id=testsuite_id)
        except TestSuite.DoesNotExist:
            messages.add_message(request, messages.INFO, 'Invalid testsuite (ID={})'.format(testsuite_id))
            return redirect(request.path)

        try:
            assigned_user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            messages.add_message(request, messages.INFO, 'Invalid user (ID={})'.format(user_id))
            return redirect(request.path)

        if testsuite.allow_many_evaluations == False and \
         Evaluation.objects.filter(reading_system=reading_system, testsuite=testsuite).exists():
             messages.add_message(request, messages.INFO, 'An evaluation already exists for this testsuite and reading system combination, and only one is allowed.')
             return redirect(request.path)

        print("Evaluation added for user {}{} (ID={})".format(assigned_user.first_name, assigned_user.last_name, assigned_user.id))
        evaluation = Evaluation.objects.create_evaluation(reading_system, testsuite, assigned_user)

        return redirect("/evaluation/{}/edit".format(evaluation.id))
