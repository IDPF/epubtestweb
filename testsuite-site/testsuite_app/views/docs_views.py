from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from testsuite_app import helper_functions
from testsuite import settings

class InstructionsForEvaluatorsView(TemplateView):
    template_name = "instructions_for_evaluators.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class InstructionsForAccessibilityEvaluatorsView(TemplateView):
    template_name = "instructions_for_accessibility_evaluators.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class CallForModeratorsView(TemplateView):
    template_name = "call_for_moderators.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class ParticipateView(TemplateView):
    template_name = "participate.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class SignUpView(TemplateView):
    template_name = "signup.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO, 'Thank you for signing up! You will be contacted shortly by one of our moderators.')

        body = "Accessibility testing sign-up request received at epubtest.org:\n\n"
        body += "Name: {}\n".format(request.POST.get("name", "Not given"))
        body += "Phone: {}\n".format(request.POST.get("phone", "Not given"))
        body += "Email: {}\n".format(request.POST.get("email", "Not given"))
        body += "OS: {}\n".format(", ".join(request.POST.getlist("os")))

        notification_email_addresses = []
        for os in request.POST.getlist("os"):
            if os in settings.email_notifications_to["A11yTesterSignUps"]:
                notification_email_addresses.extend(settings.email_notifications_to["A11yTesterSignUps"][os])

        helper_functions.send_email("Request to sign up for accessibility testing on epubtest.org", body, notification_email_addresses)

        return redirect('/participate')
