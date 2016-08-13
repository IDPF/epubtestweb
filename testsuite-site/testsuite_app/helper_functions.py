def generate_timestamp():
    from datetime import datetime
    from django.utils.timezone import utc
    return datetime.utcnow().replace(tzinfo=utc)

def force_score_refresh():
    from testsuite_app.models.evaluation import Evaluation
    evaluations = Evaluation.objects.all()
    for evaluation in evaluations:
        evaluation.update_scores()


def force_percent_complete_refresh():
    from testsuite_app.models.evaluation import Evaluation
    evaluations = Evaluation.objects.all()
    for evaluation in evaluations:
        evaluation.save(generate_timestamp = False) #save triggers update_percent_complete

def send_email_to_admins(subject, body):
    from testsuite_app.models.user_profile import UserProfile
    from django.core.mail import send_mail
    from django.contrib import messages
    from testsuite import settings

    receive_email_notifications = []
    for username in settings.receive_email_notifications:
        try:
            user = UserProfile.objects.get(username=username)
            receive_email_notifications.append(user.email)
        except UserProfile.DoesNotExist:
            continue

    try:
        send_mail(
            subject,
            body,
            settings.email_notifications_from,
            receive_email_notifications,
            fail_silently=True,
        )
    except ConnectionRefusedError:
        return -1

    return 0

def send_email_evaluation_created(evaluation):
    msgbody = "An evaluation has been created on epubtest.org. The details are:\n"
    msgbody += generate_evaluation_description(evaluation)
    msgbody += "for the reading system\n"
    msgbody += generate_reading_system_description(evaluation.reading_system)
    return send_email_to_admins("Evaluation created on epubtest.org", msgbody)

def send_email_request_to_publish_evaluation(evaluation):
    from testsuite_app.models.evaluation import Evaluation
    msgbody = "A user has requested to publish their evaluation. The details are:\n"
    msgbody += generate_evaluation_description(evaluation)
    msgbody += "for the reading system\n"
    msgbody += generate_reading_system_description(evaluation.reading_system)
    return send_email_to_admins("Request to publish evaluation on epubtest.org", msgbody)

def generate_evaluation_description(evaluation):
    from testsuite_app.models.evaluation import Evaluation
    desc = """
    Evaluation ID: {eval_id}\n
    Evaluation type: {eval_type}\n
    Evaluation added by: {user_first} {user_last}\n
    """.format(user_first = evaluation.user.first_name, 
        user_last = evaluation.user.last_name,
        eval_id = evaluation.id,
        eval_type = "Accessibility" if evaluation.testsuite.testsuite_type == "2" else "Default"
    )
    return desc

def generate_reading_system_description(reading_system):
    from testsuite_app.models.reading_system import ReadingSystem

    desc = """
    Reading System Name: {reading_system}\n
    Version: {version}\n
    OS: {operating_system}\n
    OS Version: {os_version}\n
    Reading System added by: {user_first} {user_last}\n""".format(
        reading_system = reading_system.name,
        version = reading_system.version,
        operating_system = reading_system.operating_system,
        os_version = reading_system.operating_system_version,
        user_first = reading_system.user.first_name, 
        user_last = reading_system.user.last_name,)

    return desc
