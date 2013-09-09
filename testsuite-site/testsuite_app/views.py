from django.views.generic import TemplateView, ListView, View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.edit import FormView

from django.shortcuts import render
from django.utils import timezone

from django.http import HttpResponseRedirect

import web_db_helper
from models import *
from forms import *

from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime
from urllib import urlencode


from django.forms.models import inlineformset_factory

# home page
class IndexView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        ts = web_db_helper.get_most_recent_testsuite()
        cats = web_db_helper.get_top_level_categories(ts)
        scores = web_db_helper.get_scores(cats)
        return render(request, self.template_name, {'categories': cats, 'scores': scores})

# simple about page
class AboutView(TemplateView):
    template_name = "about.html"

# details for a single reading system
class ReadingSystemView(TemplateView):
    template_name = "reading_system.html"

    def get(self, request, *args, **kwargs):
        try:
            rs = ReadingSystem.objects.get(id=kwargs['pk'])
        except ReadingSystem.DoesNotExist:
            return render(request, "404.html", {})
        evaluation = web_db_helper.get_most_recent_evaluation(rs)
        print 'start calculations .. {0}'.format(web_db_helper.generate_timestamp())
        data = web_db_helper.get_reading_system_evaluation_as_nested_categories(evaluation)
        print 'end calculations .. {0}'.format(web_db_helper.generate_timestamp())
        eval_date = web_db_helper.get_most_recent_evaluation(rs).timestamp

        # split the data across 2 lists to make it easy to consume for the reading system view
        # TODO replace this with a multicolumn definition list
        first_half = []
        second_half = []
        for n in range(0, len(data)):
            if n < len(data)/2:
                first_half.append(data[n])
            else:
                second_half.append(data[n])

        return render(request, self.template_name, {'rs': rs, 'data': data, 'eval_date': eval_date,
            'first_half': first_half, 'second_half': second_half})

# my account
class ManageView(TemplateView):
    template_name = "manage.html"

    def get(self, request, *args, **kwargs):
        reading_systems = ReadingSystem.objects.all()
        for r in reading_systems:
            r.public_evals = web_db_helper.get_public_evaluations(r)
            r.internal_evals = web_db_helper.get_internal_evaluations(r)
            r.has_summary = web_db_helper.get_most_recent_evaluation(r) != None

        return render(request, self.template_name,
            {'reading_systems': reading_systems})

# edit an evaluation
class EditEvaluationView(UpdateView):
    template_name = "edit_evaluation.html"

    def get(self, request, *args, **kwargs):
        evaluation = Evaluation.objects.get(id=kwargs['pk'])

        if request.user != evaluation.user:
            messages.add_message(request, messages.INFO, 'You do not have permission to edit that evaluation.')
            return redirect("/manage/")

        eval_form = EvaluationForm(instance = evaluation)
        results_form = ResultFormSet(instance = evaluation)

        data = web_db_helper.get_reading_system_evaluation_as_nested_categories(evaluation)
        integrated_data = []
        for d in data:
            tmp = web_db_helper.mash_summary_data_with_form_data(d, results_form)
            integrated_data.append(d)


        return render(request, self.template_name,
            {'eval_form': eval_form, 'results_form': results_form, 'data': integrated_data})

    def post(self, request, *args, **kwargs):
        evaluation = Evaluation.objects.get(id=kwargs['pk'])
        evaluation.timestamp = web_db_helper.generate_timestamp()

        form = EvaluationForm(request.POST, instance=evaluation)
        if form.is_valid():
            form.save()

        formset = ResultFormSet(request.POST, instance=evaluation)
        if formset.is_valid():
            formset.save()
        web_db_helper.calculate_and_save_scores(evaluation)
        evaluation.percent_complete = web_db_helper.float_to_decimal(web_db_helper.get_pct_complete(evaluation))
        evaluation.save()
        messages.add_message(request, messages.INFO, 'Evaluation saved.')
        return redirect('/manage/')

# ask the user if they want to delete the reading system
class ConfirmDeleteRSView(TemplateView):
    template_name = "confirm.html"
    def get(self, request, *args, **kwargs):
        rs_id = request.GET.get('rs', '0')
        rs = ReadingSystem.objects.get(id = rs_id)
        rs_desc = "{0} {1} {2} {3}".format(rs.name, rs.version, rs.locale, rs.operating_system)
        return render(request, self.template_name,
            {"header": 'Confirm delete',
            "warning": "You are about to delete '{0}', which also deletes all its evaluations. Proceed?".format(rs_desc),
            "confirm_url": "/delete_rs/?rs={0}".format(rs_id),
            "cancel_url": "/manage/"
            })

# ask the user if they want to delete the reading system
class ConfirmDeleteEvalView(TemplateView):
    template_name = "confirm.html"
    def get(self, request, *args, **kwargs):
        eval_id = request.GET.get('evalid', '0')
        ev = Evaluation.objects.get(id = eval_id)
        warning = "You are about to delete an evaluation for '{0}' from {1}. Proceed?".format(
            ev.reading_system.name, datetime.strftime(ev.timestamp, "%b %d %Y %H:%M:%S"))
        return render(request, self.template_name,
            {"heading": 'Confirm delete',
            "warning": warning,
            "confirm_url": "/delete_ev/?evalid={0}".format(eval_id),
            "cancel_url": "/manage/".format(eval_id)
            })

# create new
class NewReadingSystemView(TemplateView):
    template_name = "new_reading_system.html"

    def get(self, request, *args, **kwargs):
        form = ReadingSystemForm()
        # read the query string for initial values
        for fieldname in form.fields.keys():
            value = request.GET.get(fieldname, '')
            form.initial[fieldname] = value
        return render(request, self.template_name,{"form": form, "action_url": "/new_rs/"})

    def post(self, request, *args, **kwargs):
        form = ReadingSystemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Reading system added.')
            return redirect('/manage/')
        else:
            messages.add_message(request, messages.INFO, 'Please complete name and version fields.')
            # query string hack
            clean_data = form.clean()
            qstr = urlencode(clean_data)
            return redirect("/new_rs/?{0}".format(qstr))


# edit existing
# TODO combine with above view
class EditReadingSystemView(TemplateView):
    template_name = "new_reading_system.html"

    def get(self, request, *args, **kwargs):
        rsid = kwargs['pk']
        rs = ReadingSystem.objects.get(id=rsid)
        form = ReadingSystemForm(instance = rs)
        return render(request, self.template_name,{"form": form, "action_url": "/edit_rs/{0}/".format(rsid)})

    def post(self, request, *args, **kwargs):
        rsid = kwargs['pk']
        rs = ReadingSystem.objects.get(id=rsid)
        form = ReadingSystemForm(request.POST, instance = rs)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Reading system edited.')
            return redirect('/manage/')
        else:
            messages.add_message(request, messages.INFO, 'Please complete name and version fields.')
            return redirect("/edit_rs/{0}/".format(rsid))

class CreateNewEvaluationView(View):

    def get(self, request, *args, **kwargs):
        rs_id = request.GET.get('rs', '0')
        testsuite = web_db_helper.get_most_recent_testsuite()
        rs = ReadingSystem.objects.get(id = rs_id)
        new_eval = web_db_helper.create_new_evaluation(testsuite, "1", rs, request.user)
        if new_eval is not None:
            return redirect("/edit_evaluation/{0}/".format(new_eval.id))
        else:
            return redirect("/manage/")

################################################
# helper functions
################################################

def create_new_evaluation(request, onsuccess='/edit_evaluation/', onfail='/manage/'):
    rs_id = request.GET.get('rs', '0')
    testsuite = web_db_helper.get_most_recent_testsuite()
    rs = ReadingSystem.objects.get(id = rs_id)
    new_eval = web_db_helper.create_new_evaluation(testsuite, "1", rs, request.user)

    if new_eval is not None:
        return redirect(onsuccess + str(new_eval.id) + "/")
    else:
        return redirect(onfail)

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

# really truly delete a reading system
def delete_rs(request):
    rs_id = request.GET.get('rs', '0')
    rs = ReadingSystem.objects.get(id=rs_id)
    rs.delete()
    messages.add_message(request, messages.INFO, "Reading system deleted")
    return redirect("/manage/")

# really truly delete an evaluation
def delete_ev(request):
    eval_id = request.GET.get('evalid', '0')
    evaluation = Evaluation.objects.get(id=eval_id)
    evaluation.delete()
    messages.add_message(request, messages.INFO, "Evaluation deleted")
    return redirect("/manage/")
