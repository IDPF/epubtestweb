from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from testsuite_app import permissions

from testsuite_app.models import *

class EvaluationView(TemplateView):
    template_name = "evaluation.html"

    def get(self, request, *args, **kwargs):

        try:
            evaluation = Evaluation.objects.get(id=kwargs['pk'])
        except Evaluation.DoesNotExist:
            return render(request, "404.html", {})

        if permissions.user_can_view_evaluation(request.user, evaluation) == False:
            return render(request, "404.html", {})
        
        categories = evaluation.testsuite.get_categories()

        for category in categories:
            features = Feature.objects.filter(category = category)
            if features != None:
                category.features = features
                for feature in category.features:
                    tests = Test.objects.filter(feature = feature)
                    if tests != None:
                        feature.tests = tests

        return render(request, self.template_name,{'evaluation': evaluation, 'categories': categories})

    def delete(self, request, *args, **kwargs):
        try:
            evaluation = Evaluation.objects.get(id=kwargs['pk'])
        except Evaluation.DoesNotExist:
            return render(request, "404.html", {})

        if permissions.user_can_edit_evaluation(request.user, reading_system) == False:
            messages.add_message(request, messages.INFO, 'You do not have permission to delete that evaluation.')
            return redirect("/manage/")
        
        evaluation.delete_associated()
        evaluation.delete()
        messages.add_message(request, messages.INFO, "Evaluation deleted")
        return HttpResponse(status=204)
    