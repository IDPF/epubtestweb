from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

from testsuite_app.models import *
from testsuite_app.forms import *
from testsuite_app import permissions
from testsuite import settings

class EditEvaluationSingleEpubView(TemplateView):
    template_name = "edit_evaluation_single_epub.html"

    def get(self, request, *args, **kwargs):
        try:
            evaluation = Evaluation.objects.get(id=kwargs['pk'])
        except Evaluation.DoesNotExist:
            return render(request, "404.html", {})

        try:
            epub = Epub.objects.get(epubid=kwargs['epub_id'])
        except Epub.DoesNotExist:
            return render(request, "404.html", {})


        results = evaluation.get_results_for_epub(epub)
        results_formset = ResultFormSet(instance = evaluation, queryset=results)
        
        action_url = request.path
        
        # calculate the url of the next section
        epubs = Epub.objects.filter(testsuite = evaluation.testsuite).order_by("epubid")
        next_epub = None
        next_url = ''
        for counter, epub_ in enumerate(epubs):
            if epub_.epubid == epub.epubid:
                if counter + 1 < len(epubs):
                    next_epub = epubs[counter+1]
                    break

        if next_epub != None:
            next_url = "/evaluation/{}/edit/section/{}/".format(evaluation.id, next_epub.epubid)

        return render(request, self.template_name,{
            "evaluation": evaluation, 
            "epub": epub, 
            "results": results, 
            "results_formset": results_formset,
            "action_url": action_url, 
            "next_url": next_url,
            "epub_downloads_url": settings.epub_downloads_url
        })

    def post(self, request, *args, **kwargs):
        try:
            evaluation = Evaluation.objects.get(id=kwargs['pk'])
        except Evaluation.DoesNotExist:
            return render(request, "404.html", {})

        if permissions.user_can_edit_evaluation(request.user, evaluation) == False:
            messages.add_message(request, messages.INFO, 'You do not have permission to edit this evaluation.')
            return redirect('/manage/')
        
        try:
            epub = Epub.objects.get(epubid=kwargs['epub_id'])
        except Epub.DoesNotExist:
            return render(request, "404.html", {})

        results = evaluation.get_results_for_epub(epub)
        results_formset = ResultFormSet(request.POST, instance = evaluation, queryset=results)
        
        
        if 'save_continue' in request.POST.keys() and 'next_url' in request.POST.keys():
            next_url = request.POST['next_url']
            return redirect(next_url)
        else:
            return redirect('/evaluation/{}/edit/'.format(evaluation.id))

