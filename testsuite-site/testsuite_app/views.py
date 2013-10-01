from urllib import urlencode

from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse

from models import ReadingSystem, Evaluation, TestSuite
from forms import ReadingSystemForm, ResultFormSet, EvaluationForm
import helper_functions

class IndexView(TemplateView):
    "Home page"
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        testsuite = TestSuite.objects.get_most_recent_testsuite()
        categories = testsuite.get_top_level_categories()
        scores = helper_functions.get_public_scores(categories)
        return render(request, self.template_name, {'categories': categories, 'scores': scores,
            "testsuite_date": testsuite.version_date})

class AboutView(TemplateView):
    "About page"
    template_name = "about.html"

class ManageView(TemplateView):
    "Manage page"
    template_name = "manage.html"

    def get(self, request, *args, **kwargs):
        display_name = request.user.username
        testsuite = TestSuite.objects.get_most_recent_testsuite()
        if len(request.user.first_name) > 0 or len(request.user.last_name) > 0:
            display_name = "{0} {1}".format(request.user.first_name, request.user.last_name)
            display_name = display_name.strip()
        reading_systems = ReadingSystem.objects.all()
        return render(request, self.template_name,
            {'reading_systems': reading_systems, 'display_name': display_name,
            "testsuite_date": testsuite.version_date})

class ReadingSystemView(TemplateView):
    "Details for a single reading system"
    template_name = "reading_system.html"

    def get(self, request, *args, **kwargs):
        try:
            rs = ReadingSystem.objects.get(id=kwargs['pk'])
        except ReadingSystem.DoesNotExist:
            return render(request, "404.html", {})
        data = helper_functions.get_results_as_nested_categories(rs)
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
        rs.delete()
        messages.add_message(request, messages.INFO, "Reading system deleted")
        return HttpResponse(status=204)



class EditEvaluationView(UpdateView):
    "Edit reading system evaluation"
    template_name = "edit_evaluation.html"

    def get(self, request, *args, **kwargs):
        try:
            rs = ReadingSystem.objects.get(id=kwargs['pk'])
        except ReadingSystem.DoesNotExist:
            return render(request, "404.html", {})

        action_url = "/rs/{0}/edit/".format(rs.id)
        evaluation = rs.get_current_evaluation()
        eval_form = EvaluationForm(instance = evaluation)
        results_form = ResultFormSet(instance = evaluation)

        nested_data = helper_functions.get_results_as_nested_categories(rs)
        data = []
        for d in nested_data:
            helper_functions.mash_summary_data_with_form_data(d, results_form)
            data.append(d)

        if request.user != rs.user:
            messages.add_message(request, messages.INFO, 'You do not have permission to edit that reading system.')
            return redirect("/manage/")

        return render(request, self.template_name,
            {'eval_form': eval_form, 'results_form': results_form, 'data': data,
            'rs': rs, "action_url": "/rs/{0}/eval/".format(rs.id)})

    def post(self, request, *args, **kwargs):
        try:
            rs = ReadingSystem.objects.get(id=kwargs['pk'])
        except ReadingSystem.DoesNotExist:
            return render(request, "404.html", {})

        if request.user != rs.user:
            messages.add_message(request, messages.INFO, 'You do not have permission to edit that evaluation.')
            return redirect("/manage/")
        evaluation = rs.get_current_evaluation()
        eval_form = EvaluationForm(request.POST, instance=evaluation)
        formset = ResultFormSet(request.POST, instance=evaluation)

        formset.save()
        eval_form.save()
        
        
        # if we are auto-saving, don't redirect
        if not request.POST.has_key('auto') or request.POST['auto'] == "false":
            return redirect('/manage/')

# confirm deleting a reading system
class ConfirmDeleteRSView(TemplateView):
    template_name = "confirm.html"
    def get(self, request, *args, **kwargs):
        try:
            rs = ReadingSystem.objects.get(id=kwargs['pk'])
        except ReadingSystem.DoesNotExist:
            return render(request, "404.html", {})
        rs_desc = "{0} {1} {2} {3}".format(rs.name, rs.version, rs.locale, rs.operating_system)
        return render(request, self.template_name,
            {"header": 'Confirm delete',
            "warning": "You are about to delete '{0}'. Proceed?".format(rs_desc),
            "confirm_url": "/rs/{0}/".format(kwargs['pk'])
            })

# create new reading system
class EditReadingSystemView(TemplateView):
    template_name = "edit_reading_system.html"

    def get(self, request, *args, **kwargs):
        form = None
        title = ""
        action_url = ""
        if kwargs.has_key('pk'):
            try:
                rs = ReadingSystem.objects.get(id=kwargs['pk'])
            except:
                return render(request, "404.html", {})
            if request.user != rs.user:
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


