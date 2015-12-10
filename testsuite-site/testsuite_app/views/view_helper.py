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

def set_evaluation_visibility(request, *args, **kwargs):
    try:
        rs = ReadingSystem.objects.get(id=kwargs['pk'])
    except ReadingSystem.DoesNotExist:
        return render(request, "404.html", {})

    try:
        rset = Evaluation.objects.get(id=kwargs['rset'])
    except Evaluation.DoesNotExist:
        return render(request, "404.html", {})

    visibility = request.GET.get('set', common.VISIBILITY_MEMBERS_ONLY)
    if visibility != common.VISIBILITY_MEMBERS_ONLY and \
        visibility != common.VISIBILITY_PUBLIC and \
        visibility != common.VISIBILITY_OWNER_ONLY:
        messages.add_message(request, messages.WARNING, 'Visibility option {0} not recognized.'.format(visibility))
        return redirect('/manage/')

    can_set_vis = permissions.user_can_change_result_set_visibility(request.user, rset, visibility)

    if can_set_vis == True:
        rset.visibility = visibility
        rset.save()
    else:
        messages.add_message(request, messages.WARNING, "You don't have permission to change the visibility for this item.")    

    return redirect("/rs/{0}/eval/accessibility/".format(rs.id))

def archive_evaluation(request, *args, **kwargs):
    return set_evaluation_status(kwargs['pk'], common.EVALUATION_STATUS_TYPE_ARCHIVED)

def unarchive_evaluation(request, *args, **kwargs):
    return set_evaluation_status(kwargs['pk'], common.EVALUATION_STATUS_TYPE_CURRENT)

def set_evaluation_status(evaluation_id, status):
    try:
        evaluation = Evaluation.objects.get(id=evaluation_id)
    except Evaluation.DoesNotExist:
        return render(request, "404.html", {})

    evaluation.status = status
    evaluation.save()
    return redirect('/manage/') 

