from urllib import urlencode

from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
import os
from models import ReadingSystem, Evaluation, TestSuite, Test, Result, common
from forms import ReadingSystemForm, ResultFormSet
from testsuite import settings
import helper_functions
import permissions

class IndexView(TemplateView):
    "Home page"
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        testsuite = TestSuite.objects.get_most_recent_testsuite()
        categories = testsuite.get_top_level_categories()
        rs_scores = helper_functions.get_public_scores(categories)
        view_option = request.GET.get('view', 'simple')
        return render(request, self.template_name, {'categories': categories, 'rs_scores': rs_scores,
            "testsuite_date": testsuite.version_date, 'view_option': view_option})

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


class CompareResultsView(TemplateView):
    "Compare results form page"
    template_name = "compare_form.html"
    
    def get(self, request, *args, **kwargs):
        testsuite = TestSuite.objects.get_most_recent_testsuite()
        data = helper_functions.testsuite_to_dict(testsuite)
        action_url = "/compare/"
        return render(request, self.template_name, 
            {"data": data, "action_url": action_url})

    def post(self, request, *args, **kwargs):
        view_option = request.GET.get('view', 'simple')
        test_ids = request.POST.getlist('test-selected', []) #getlist is a method of django's QueryDict object
        tests = Test.objects.filter(pk__in = test_ids)
        reading_systems = ReadingSystem.objects.filter(visibility = common.VISIBILITY_PUBLIC)
        test_arrays = []
        list_max = 13
        # split the tests up into arrays of 13 for display purposes
        if tests.count() <= list_max:
            test_arrays.append(tests)
        else:
            start = 0
            end = list_max
            for n in range(0, tests.count() / list_max):
                arr = tests[start:end]
                start += list_max
                end += list_max
                test_arrays.append(arr)

            if tests.count() % list_max != 0:
                mod = (tests.count() % list_max)
                start = tests.count()-mod
                arr = tests[start:tests.count()]
                test_arrays.append(arr)

        return render(request, "compare_results.html", 
            {'test_arrays': test_arrays, 'reading_systems': reading_systems, "view_option": view_option})

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
            messages.add_message(request, messages.INFO, 'You do not have permission to delete that reading system.')
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
        
        Evaluation.objects.delete_associated(rs)
        rs.delete()
        messages.add_message(request, messages.INFO, "Reading system deleted")
        return HttpResponse(status=204)

class EditEvaluationView(UpdateView):
    "Edit reading system evaluation"
    template_name = "evaluation_form.html"

    def get(self, request, *args, **kwargs):
        try:
            rs = ReadingSystem.objects.get(id=kwargs['pk'])
        except ReadingSystem.DoesNotExist:
            return render(request, "404.html", {})

        action_url = "/rs/{0}/eval/".format(rs.id)
        evaluation = rs.get_current_evaluation()
        results_form = ResultFormSet(instance = evaluation)
        testsuite = TestSuite.objects.get_most_recent_testsuite()
        data = helper_functions.testsuite_to_dict(testsuite)[0:1]
        
        can_edit = permissions.user_can_edit_reading_system(request.user, rs)
        if can_edit == False:
            messages.add_message(request, messages.INFO, 'You do not have permission to edit that evaluation.')
            return redirect("/manage/")

        return render(request, self.template_name,
            {'evaluation': evaluation, 'results_form': results_form, 'data': data,
            'rs': rs, "action_url": action_url})

    def post(self, request, *args, **kwargs):
        try:
            rs = ReadingSystem.objects.get(id=kwargs['pk'])
        except ReadingSystem.DoesNotExist:
            return render(request, "404.html", {})

        can_edit = permissions.user_can_edit_reading_system(request.user, rs)
        if can_edit == False:
            messages.add_message(request, messages.INFO, 'You do not have permission to edit that evaluation.')
            return redirect("/manage/")
        evaluation = rs.get_current_evaluation()
        formset = ResultFormSet(request.POST, instance=evaluation)
        
        formset.save()
        evaluation.save()
        
        # if we are auto-saving, don't redirect
        if not request.POST.has_key('auto') or request.POST['auto'] == "false":
            return redirect('/manage/')

# confirm deleting a reading system
class ConfirmDeleteRSView(TemplateView):
    template_name = "confirm_delete_rs.html"
    def get(self, request, *args, **kwargs):
        try:
            rs = ReadingSystem.objects.get(id=kwargs['pk'])
        except ReadingSystem.DoesNotExist:
            return render(request, "404.html", {})

        can_delete = permissions.user_can_delete_reading_system(request.user, rs)
        if can_delete == False:
            messages.add_message(request, messages.INFO, 'You do not have permission to delete that reading system.')
            return redirect("/manage/")
        
        rs_desc = "{0} {1} {2} {3}".format(rs.name, rs.version, rs.locale, rs.operating_system)
        return render(request, self.template_name,
            {"header": 'Confirm delete',
            "warning": "You are about to delete '{0}'. Proceed?".format(rs_desc),
            "confirm_url": "/rs/{0}/".format(kwargs['pk'])
            })

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
            except Evaluation.DoesNotExist:
                return render(request, "404.html", {})
        else:
            form = ReadingSystemForm(request.POST)

        if form.is_valid():
            obj = form.save(commit = False)
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
                evaluation = rs.get_current_evaluation()
                date = evaluation.testsuite.version_date
                results = Result.objects.filter(evaluation = evaluation, result = "2") #not supported
                result_dict_list = []
                for r in results:
                	source = helper_functions.calculate_source(r.test.source)
                	result_dict = {"result": r, "source": source}
                	result_dict_list.append(result_dict)
                # sort the list according to what epub they reference
                sorted_results = sorted(result_dict_list, key=lambda k: k['source']['link']) 
                return render(request, self.template_name, {"rs": rs, "results": sorted_results, "testsuite_date": date})
            except Evaluation.DoesNotExist:
                return render(request, "404.html", {})


        
 
################################################
# helper functions
################################################

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

def export_data(request):
    import export_data
    from lxml import etree
    xmldoc = export_data.export_all_current_evaluations(request.user)
    xmldoc_str = etree.tostring(xmldoc, pretty_print=True)
    response = HttpResponse(mimetype='application/xml')
    response['Content-Disposition'] = 'attachment; filename="export.xml"'
    response.write(xmldoc_str)
    return response

def set_visibility(request, *args, **kwargs):
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

    can_set_vis = permissions.user_can_change_visibility(request.user, rs, visibility)

    if can_set_vis == True:
        rs.visibility = visibility
        rs.save()
    else:
        messages.add_message(request, messages.WARNING, "You don't have permission to change the visibility for this item.")    

    return redirect("/manage/")


