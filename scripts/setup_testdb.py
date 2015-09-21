import admin_functions
import random
import testsuite_app.models.common
from testsuite_app.models import *

# populate the database for testing
# important: import the testsuite first

def init_for_testing():
    # make sure there's a testsuite present
    testsuites = TestSuite.objects.get_most_recent_testsuites()
    
    if testsuites == None:
        print("Could not initialize: no testsuites present.")
        return

    users = create_users()
    rses = create_reading_systems(users)

    assistive_technology = ["ScreenReader", "Magnifier", "Braille"]
    
    for rs in rses:
        #rs_versions = rs.get_all_versions()
        # # they all have more than one version
        # idx = random.randrange(0,2)
        # one_rs_version = rs_versions[idx]
        # idx = random.randrange(0,2)
        # another_rs_version = rs_versions[idx]
        # # the idea is that the evaluations might not be for the same version (but they could be)

        for testsuite in testsuites:
            if testsuite.allow_many_evaluations == False:
                evaluation = create_evaluation(rs, testsuite, users[random.randrange(0,9)])
                
            else:
                # create 2 or 3 accessibility evaluations
                num = random.randrange(2,4)
                for n in range(0,num): 
                    evaluation = create_evaluation(rs, testsuite, users[random.randrange(0,9)])
                    
                    if testsuite.testsuite_type == common.TESTSUITE_TYPE_ACCESSIBILITY:
                        # attach assistive technology metadata
                        evaluation.add_metadata(
                            assistive_technology[random.randrange(0,3)], 
                            str(random.randrange(1,4)), 
                            bool(random.randrange(0,2)), 
                            bool(random.randrange(0,2))
                        )


        from testsuite_app.helper_functions import force_score_refresh
        force_score_refresh()
                        



def create_users():
    # create 9 users.
    users = []
    users.append(add_user("user1", False))
    users.append(add_user("user2", False))
    users.append(add_user("user3", False))
    users.append(add_user("user4", False))
    users.append(add_user("user5", False))
    users.append(add_user("user6", False))
    users.append(add_user("user7", False))
    users.append(add_user("user8", False))
    users.append(add_user("user9", False))
    return users
    
def create_reading_systems(users):
    reading_systems = []
    reading_system_versions = []
    reading_systems.append(add_reading_system("Super Reader", users[0], "OSX"))
    reading_systems.append(add_reading_system("Happy Book", users[1], "Windows"))
    reading_systems.append(add_reading_system("Speed Read", users[2], "Linux"))
    reading_systems.append(add_reading_system("Page Turner", users[3], "iOS"))

    reading_system_versions.append(add_reading_system_version(reading_systems[0], "1.0", users[4], False))
    reading_system_versions.append(add_reading_system_version(reading_systems[0], "1.2", users[4], False))
    reading_system_versions.append(add_reading_system_version(reading_systems[0], "1.3", users[4], True))
    reading_system_versions.append(add_reading_system_version(reading_systems[1], "2.2", users[5], False))
    reading_system_versions.append(add_reading_system_version(reading_systems[1], "2.3", users[5], True))
    reading_system_versions.append(add_reading_system_version(reading_systems[2], "1.4", users[6], False))
    reading_system_versions.append(add_reading_system_version(reading_systems[2], "2.5", users[6], True))
    reading_system_versions.append(add_reading_system_version(reading_systems[3], "4.0", users[7], True))
    reading_system_versions.append(add_reading_system_version(reading_systems[3], "4.1", users[7], True))

    return reading_system_versions



def create_evaluation(reading_system, testsuite, user):
    print("before")
    evaluation = Evaluation.objects.create_evaluation(reading_system, testsuite=testsuite, user = user)
    print("after")
    results = evaluation.get_results()
    print("populating results")
    for result in results:
        x = random.randrange(1,3)
        if x == 1:
            result.result = common.RESULT_SUPPORTED
        else:
            result.result = common.RESULT_NOT_SUPPORTED

        result.save()
    print("done populating")
    #evaluation.update_scores()
    return evaluation
    
    

def add_user(username, is_superuser):
    user = UserProfile.objects.create_user(username, "test@example.com", "password")
    user.first_name = username
    user.last_name = ""
    user.is_superuser = is_superuser
    user.save()
    return user

def add_reading_system(name, user, os):
    rs = ReadingSystem(
        name = name,
        operating_system = os,
        user = user
    )
    rs.save() 
    return rs

def add_reading_system_version(reading_system, version, user, is_most_recent_version):
    return ReadingSystemVersion.objects.create_reading_system_version(
        version, 
        "", 
        user, 
        reading_system, 
        is_most_recent_version)

