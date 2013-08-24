# create a set of dummy data

from testsuite_app import models
from random import randrange
from testsuite_app import web_db_helper


def add_data():
    user = add_user()
    print "Added user: "
    print user.username
    rs = add_reading_system()
    print "\nAdded reading system: "
    print rs.name
    add_evaluation(user, rs)

    print "\nAdded 1 evaluation."


def clear_data():
    models.UserProfile.objects.all().delete()
    models.ReadingSystem.objects.all().delete()
    models.Evaluation.objects.all().delete()


def add_user():
    user1 = models.UserProfile.objects.create_user('user1', 'user1@example.org', 'secretpassword')
    user1.first_name = "User1"
    user1.last_name = "One"
    user1.is_superuser = False
    user1.default_evaluation_type = "1"
    user1.organization = "Test Experts Inc"
    user1.save()

    return user1


def add_reading_system():
    rs1 = models.ReadingSystem(
        locale = "US",
        name = "SuperReader",
        operating_system = "OSX",
        sdk_version = "N/A",
        version = "1.0"
    )
    rs1.save()

    return rs1

def add_evaluation(user, rs):
    ts = web_db_helper.get_most_recent_testsuite()
    evaluation = web_db_helper.create_new_evaluation(
        ts,
        "2",
        rs,
        user
    )

    results = models.Result.objects.filter(evaluation = evaluation)
    for r in results:
        r.result = str(randrange(1, 4))
        r.save()
    evaluation.percent_complete = web_db_helper.get_pct_complete(evaluation)

    # save the scores for the top-level categories
    web_db_helper.calculate_and_save_scores(evaluation)

    evaluation.save()
    return evaluation
