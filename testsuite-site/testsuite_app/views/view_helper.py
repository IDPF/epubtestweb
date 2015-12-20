from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse

from testsuite_app.models import *
from testsuite_app.forms import *
from testsuite import settings
from testsuite_app import permissions


def auth_and_login(request, onfail='/login/'):
    if request.POST:
        next = request.POST['next']
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None and user.is_active: #is_active means that the account is not disabled
            login(request, user)
            return redirect(next)
        else:
            return redirect(onfail)

def logout_user(request):
    logout(request)
    messages.add_message(request, messages.INFO, 'You have been logged out.')
    return redirect("/")

def publish_evaluation(request, *args, **kwargs):
    return set_evaluation_published_status(request, kwargs['pk'], True)

def unpublish_evaluation(request, *args, **kwargs):
    return set_evaluation_published_status(request, kwargs['pk'], False)

def archive_evaluation(request, *args, **kwargs):
    return set_evaluation_archived_status(request, kwargs['pk'], True)

def unarchive_evaluation(request, *args, **kwargs):
    return set_evaluation_archived_status(request, kwargs['pk'], False)


def set_evaluation_published_status(request, evaluation_id, is_published):
    try:
        evaluation = Evaluation.objects.get(id=evaluation_id)
    except Evaluation.DoesNotExist:
        return render(request, "404.html", {})

    if permissions.user_can_publish_evaluation(request.user, evaluation):
        evaluation.is_published = is_published
        evaluation.save()
        status = "unpublished"
        if is_published: 
            status = "published"
        messages.add_message(request, messages.INFO, "Evaluation {}.".format(status))
    else:
        messages.add_message(request, messages.WARNING, "You don't have permission to publish/unpublish this evaluation.")
    return redirect("/evaluation/all/") 


def set_evaluation_archived_status(request, evaluation_id, is_archived):
    try:
        evaluation = Evaluation.objects.get(id=evaluation_id)
    except Evaluation.DoesNotExist:
        return render(request, "404.html", {})

    return_url = "/manage/"
    if 'return' in request.GET:
        return_url = request.GET.get('return', '')    

    if permissions.user_can_edit_evaluation(request.user, evaluation):
        evaluation.is_archived = is_archived
        evaluation.save()
        status = "unarchived"
        if is_archived: 
            status = "archived"
        messages.add_message(request, messages.INFO, "Evaluation {}.".format(status))
    else:
        messages.add_message(request, messages.WARNING, "You don't have permission to archive/unarchive this evaluation.")
    return redirect(return_url) 


