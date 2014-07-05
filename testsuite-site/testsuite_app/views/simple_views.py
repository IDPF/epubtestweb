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
from view_helper import *

class IndexView(TemplateView):
    "Home page"
    template_name = "index.html"        

class AboutView(TemplateView):
    "About page"
    template_name = "about.html"

class TestsuiteView(TemplateView):
    "Testsuite download page"
    template_name = "testsuite.html"

    def get(self, request, *args, **kwargs):
        files = os.listdir(settings.EPUB_ROOT)
        downloads = []

        for f in sorted(files):
            ext = os.path.splitext(f)[1]
            if ext == '.epub' or ext == '.zip':
                # the download link is going to be EPUB_URL + filename
                filename = os.path.basename(f)
                link = "{0}{1}".format(settings.EPUB_URL, filename)
                
                label = ""
                if ext == '.epub':
                    # assuming the filenames are all like:
                    # epub30-test-0220-20131016.epub
                    # chop off the first 12 and the last 14 to get the number, e.g. 0220.
                    # this matches what is usually in the publication title and what is shown to the user in the test form
                    label = "Document {0}".format(f[12:len(f)-14])
                else:
                    label = "All Testsuite Documents (zip)"

                dl = {"label": label, "link": link}
                downloads.append(dl)
        return render(request, self.template_name, {'downloads': downloads})

class CurrentResultsView(TemplateView):
    "Grid of scores"
    template_name = "current_results.html"

    def get(self, request, *args, **kwargs):
        testsuite = TestSuite.objects.get_most_recent_testsuite()
        categories = testsuite.get_top_level_categories()
        rs_scores = helper_functions.get_public_scores(categories)
        view_option = request.GET.get('view', 'simple')
        return render(request, self.template_name, {'categories': categories, 'rs_scores': rs_scores,
            "testsuite_date": testsuite.version_date, 'view_option': view_option})


class ManageView(TemplateView):
    "Manage page"
    template_name = "manage.html"

    def get(self, request, *args, **kwargs):
        testsuite = TestSuite.objects.get_most_recent_testsuite()
        if len(request.user.first_name) > 0 or len(request.user.last_name) > 0:
            display_name = "{0} {1}".format(request.user.first_name, request.user.last_name)
            display_name = display_name.strip()
        reading_systems = ReadingSystem.objects.all()
        return render(request, self.template_name,
            {'reading_systems': reading_systems, "testsuite_date": testsuite.version_date})


class ReadingSystemView(TemplateView):
    "Details for a single reading system"
    template_name = "reading_system.html"

    def get(self, request, *args, **kwargs):
        try:
            rs = ReadingSystem.objects.get(id=kwargs['pk'])
        except ReadingSystem.DoesNotExist:
            return render(request, "404.html", {})

        can_view = permissions.user_can_view_reading_system(request.user, rs, 'rs')
        if can_view == False:
            messages.add_message(request, messages.INFO, 'You do not have permission to view that reading system.')
            return redirect("/")

        testsuite = TestSuite.objects.get_most_recent_testsuite()
        data = helper_functions.testsuite_to_dict(testsuite)
        # split the data across 2 lists to make it easy to consume for the reading system view
        # TODO replace this with a multicolumn definition list
        first_half = []
        second_half = []
        for n in range(0, len(data)):
            if n < len(data)/2:
                first_half.append(data[n])
            else:
                second_half.append(data[n])

        return render(request, self.template_name, {'rs': rs, 'data': data,
            'first_half': first_half, 'second_half': second_half})

    def delete(self, request, *args, **kwargs):
        try:
            rs = ReadingSystem.objects.get(id=kwargs['pk'])
        except ReadingSystem.DoesNotExist:
            return render(request, "404.html", {})

        can_delete = permissions.user_can_delete_reading_system(request.user, rs)
        if can_delete == False:
            messages.add_message(request, messages.INFO, 'You do not have permission to delete that reading system.')
            return redirect("/manage/")
        
        rs.delete_associated()
        rs.delete()
        messages.add_message(request, messages.INFO, "Reading system deleted")
        return HttpResponse(status=204)

# create new reading system
class EditReadingSystemView(TemplateView):
    template_name = "reading_system_details_form.html"

    def get(self, request, *args, **kwargs):
        form = None
        title = ""
        action_url = ""
        if kwargs.has_key('pk'):
            try:
                rs = ReadingSystem.objects.get(id=kwargs['pk'])
            except:
                return render(request, "404.html", {})
            can_edit = permissions.user_can_edit_reading_system(request.user, rs)
            if can_edit == False:
                messages.add_message(request, messages.INFO, 'You do not have permission to edit that reading system.')
                return redirect("/manage/")
            form = ReadingSystemForm(instance = rs)
            action_url = "/rs/{0}/edit/".format(rs.id)
            title = "Edit Reading System"
        else:
            form = ReadingSystemForm()
            # read the query string for initial values
            for fieldname in form.fields.keys():
                value = request.GET.get(fieldname, '')
                form.initial[fieldname] = value
            action_url = "/rs/new/"
            title = "Add Reading System"
        return render(request, self.template_name, {'rs_form': form,
            "title": title, "action_url": action_url})

    def post(self, request, *args, **kwargs):
        form = None
        if kwargs.has_key('pk'):
            try:
                rs = ReadingSystem.objects.get(id=kwargs['pk'])
                form = ReadingSystemForm(request.POST, instance = rs)
            except ReadingSystem.DoesNotExist:
                return render(request, "404.html", {})
        else:
            form = ReadingSystemForm(request.POST)

        if form.is_valid():
            obj = form.save(commit = False)
            if hasattr(obj, 'user') == False:
                obj.user = request.user
            obj.save()
            return redirect("/manage/")
        else:
            messages.add_message(request, messages.INFO, 'Please complete all required fields.')
            if kwargs.has_key('pk'): #if we were editing an existing RS
                return redirect("/rs/{0}/edit/".format(kwargs['pk']))
            else:
                # pass the user's form values in the query string
                # so they don't have to retype everything
                clean_data = form.clean()
                qstr = urlencode(clean_data)
                return redirect("/rs/new/?{0}".format(qstr))


class ProblemReportView(TemplateView):
    template_name = "report.html"

    def get(self, request, *args, **kwargs):
        if kwargs.has_key('pk'):
            try:
                rs = ReadingSystem.objects.get(id=kwargs['pk'])
                result_set = rs.get_default_result_set()
                date = result_set.testsuite.version_date
                results = result_set.get_not_supported_results()
                result_dict_list = []
                for r in results:
                    source = helper_functions.calculate_source(r.test.source)
                    result_dict = {"result": r, "source": source}
                    result_dict_list.append(result_dict)
                # sort the list according to what epub they reference
                sorted_results = sorted(result_dict_list, key=lambda k: k['source']['link']) 
                return render(request, self.template_name, {"rs": rs, "results": sorted_results, "testsuite_date": date})
            except ReadingSystem.DoesNotExist:
                return render(request, "404.html", {})

class AccessibilityConfigurationsView(TemplateView):
    "Lists evaluated configurations for a single reading system"
    template_name = "accessibility_configurations.html"

    def get(self, request, *args, **kwargs):
        try:
            rs = ReadingSystem.objects.get(id=kwargs['pk'])
        except ReadingSystem.DoesNotExist:
            return render(request, "404.html", {})

        can_view = permissions.user_can_view_reading_system(request.user, rs, 'rs')

        if can_view == False:
            messages.add_message(request, messages.INFO, 'You do not have permission to view that reading system.')
            return redirect("/")

        result_sets = rs.get_accessibility_result_sets()
        allowed_result_sets = []
        for rset in result_sets:
            can_view_config = permissions.user_can_view_accessibility_result_set(request.user, rset)
            if can_view and can_view_config:
                allowed_result_sets.append(rset)
            else:
                print "cannot view"
        
        return render(request, self.template_name, {'rs': rs, 'result_sets': allowed_result_sets, 'edit': False})

class EditAccessibilityConfigurationsView(TemplateView):
    "Lists evaluated configurations for a single reading system"
    template_name = "accessibility_configurations.html"

    def get(self, request, *args, **kwargs):
        try:
            rs = ReadingSystem.objects.get(id=kwargs['pk'])
        except ReadingSystem.DoesNotExist:
            return render(request, "404.html", {})

        can_view = permissions.user_can_view_reading_system(request.user, rs, 'rs')
        if can_view == False:
            messages.add_message(request, messages.INFO, 'You do not have permission to view that reading system.')
            return redirect("/")

        result_sets = rs.get_accessibility_result_sets()

        return render(request, self.template_name, {'rs': rs, 'result_sets': result_sets, 'edit': True})


class AccessibilityReadingSystemView(TemplateView):
    "Details for a single reading system's accessibility evaluation"
    template_name = "reading_system_accessibility.html"

    def get(self, request, *args, **kwargs):
        try:
            rs = ReadingSystem.objects.get(id=kwargs['pk'])
        except ReadingSystem.DoesNotExist:
            return render(request, "404.html", {})

        try:
            rset = ResultSet.objects.get(id=kwargs['rset'])
        except ResultSet.DoesNotExist:
            return render(request, "404.html", {})

        can_view = permissions.user_can_view_accessibility_result_set(request.user, rset)
        if can_view == False:
            messages.add_message(request, messages.INFO, 'You do not have permission to view that accessibility evaluation.')
            return redirect("/manage".format(rs.id))

        ts = TestSuite.objects.get_most_recent_testsuite_of_type(common.TESTSUITE_TYPE_ACCESSIBILITY)
        data = helper_functions.testsuite_to_dict(ts)
        return render(request, self.template_name, {'rs': rs, 'data': data, 'result_set': rset})

    def delete(self, request, *args, **kwargs):
        print "DELETING ACCESSIBILITY CONFIG"
        try:
            rs = ReadingSystem.objects.get(id=kwargs['pk'])
        except ReadingSystem.DoesNotExist:
            return render(request, "404.html", {})

        try:
            rset = ResultSet.objects.get(id=kwargs['rset'])
        except ResultSet.DoesNotExist:
            return render(request, "404.html", {})        

        can_delete = permissions.user_can_delete_accessibility_result_set(request.user, rset)
        if can_delete == False:
            messages.add_message(request, messages.INFO, 'You do not have permission to delete that accessibility evaluation.')
            return redirect("/manage/")
        
        rset.delete_associated()
        rset.delete()
        messages.add_message(request, messages.INFO, "Accessibility evaluation deleted")
        return HttpResponse(status=204)

