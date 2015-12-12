from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

from testsuite_app.models import *

class AddEvaluationView(TemplateView):
    template_name = "add_evaluation.html"

    def get(self, request, *args, **kwargs):
        testsuites = TestSuite.objects.get_most_recent_testsuites()

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

        
        return render(request, self.template_name,{"testsuites": testsuites, "reading_systems": reading_systems,
            "action_url": request.path})


    def post(self, request, *args, **kwargs):
        print(request.path)
        reading_system_id = request.POST.getlist('reading_system', [])[0] #getlist is a method of django's QueryDict object
        testsuite_id = request.POST.getlist('testsuite', [])[0] #getlist is a method of django's QueryDict object

        try:
            reading_system = ReadingSystem.objects.get(id=reading_system_id)
        except ReadingSystem.DoesNotExist:
            messages.add_message(request, messages.INFO, 'Invalid reading system (ID={})'.format(reading_system_id))
            return redirect(request.path)    

        try:
            testsuite = TestSuite.objects.get(id=testsuite_id)
        except TestSuite.DoesNotExist:
            messages.add_message(request, messages.INFO, 'Invalid testsuite (ID={})'.format(reading_system_id))
            return redirect(request.path)    

        evaluation = Evaluation.objects.create_evaluation(reading_system, testsuite, request.user)

        return redirect("/evaluation/{}/edit".format(evaluation.id))
    


    