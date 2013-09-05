# create a set of dummy data

from testsuite_app import models
from random import randrange
from testsuite_app import util, evaluation_helper, scoring


def add_data():
    user = add_user()
    print "Added user: "
    print user.username
    rs1, rs2 = add_reading_system()
    print "\nAdded reading system: "
    add_evaluation(user, rs1)
    add_evaluation(user, rs2)

    print "\nAdded 2 evaluations."


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

    rs2 = models.ReadingSystem(
        locale = "US",
        name = "FasterReader",
        operating_system = "OSX",
        sdk_version = "N/A",
        version = "2.0"
    )
    rs2.save()

    return (rs1, rs2)

def add_evaluation(user, rs):
    ts = util.get_most_recent_testsuite()
    evaluation = evaluation_helper.create_new_evaluation(
        ts,
        "2",
        rs,
        user
    )

    results = models.Result.objects.filter(evaluation = evaluation)
    for r in results:
        r.result = str(randrange(1, 4))
        r.save()
    evaluation.percent_complete = evaluation_helper.get_pct_complete(evaluation)

    # save the scores for the top-level categories
    scoring.calculate_and_save_scores(evaluation)

    evaluation.save()
    return evaluation
