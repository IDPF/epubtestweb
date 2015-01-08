from urllib import urlencode

from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
import os
from testsuite_app.models import ReadingSystem, TestSuite, Test, Result, common, ResultSet
from testsuite_app.forms import ReadingSystemForm, ResultFormSet, ResultSetMetadataForm
from testsuite import settings
from testsuite_app import helper_functions
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

def export_data_all(request):
    import export_data
    from lxml import etree
    xmldoc = export_data.export_all_current_reading_systems(request.user)
    xmldoc_str = etree.tostring(xmldoc, pretty_print=True)
    response = HttpResponse(mimetype='application/xml')
    response['Content-Disposition'] = 'attachment; filename="export.xml"'
    response.write(xmldoc_str)
    return response

def export_data_single(request, *args, **kwargs):
    import export_data
    from lxml import etree
    try:
        rs = ReadingSystem.objects.get(id=kwargs['pk'])
    except ReadingSystem.DoesNotExist:
        return render(request, "404.html", {})
    
    can_view = permissions.user_can_view_reading_system(request.user, rs, 'rs')
    if can_view == False:
        return render(request, "404.html", {})
    xmldoc = export_data.export_single_reading_system(rs, request.user)
    xmldoc_str = etree.tostring(xmldoc, pretty_print=True)
    response = HttpResponse(mimetype='application/xml')
    response['Content-Disposition'] = 'attachment; filename="export_{0}_{1}_{2}.xml"'.format\
        (rs.name, rs.version, rs.operating_system)
    response.write(xmldoc_str)
    return response

def set_rs_visibility(request, *args, **kwargs):
    try:
        rs = ReadingSystem.objects.get(id=kwargs['pk'])
    except ReadingSystem.DoesNotExist:
        return render(request, "404.html", {})

    visibility = request.GET.get('set', common.VISIBILITY_MEMBERS_ONLY)
    if visibility != common.VISIBILITY_MEMBERS_ONLY and \
        visibility != common.VISIBILITY_PUBLIC and \
        visibility != common.VISIBILITY_OWNER_ONLY:
        messages.add_message(request, messages.WARNING, 'Visibility option {0} not recognized.'.format(visibility))
        return redirect('/manage/')

    can_set_vis = permissions.user_can_change_reading_system_visibility(request.user, rs, visibility)

    if can_set_vis == True:
        rs.set_visibility(visibility)
        rs.save()
    else:
        messages.add_message(request, messages.WARNING, "You don't have permission to change the visibility for this item.")    

    return redirect("/manage/")


def set_accessibility_visibility(request, *args, **kwargs):
    try:
        rs = ReadingSystem.objects.get(id=kwargs['pk'])
    except ReadingSystem.DoesNotExist:
        return render(request, "404.html", {})

    try:
        rset = ResultSet.objects.get(id=kwargs['rset'])
    except ResultSet.DoesNotExist:
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

def archive_rs(request, *args, **kwargs):
    return set_rs_status(kwargs['pk'], common.READING_SYSTEM_STATUS_TYPE_ARCHIVED)

def unarchive_rs(request, *args, **kwargs):
    return set_rs_status(kwargs['pk'], common.READING_SYSTEM_STATUS_TYPE_CURRENT)

def set_rs_status(rsid, rs_status):
    try:
        rs = ReadingSystem.objects.get(id=rsid)
    except ReadingSystem.DoesNotExist:
        return render(request, "404.html", {})

    rs.status = rs_status
    rs.save()
    return redirect('/manage/') 
