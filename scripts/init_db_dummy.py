import testsuite.models
import admin_functions

# populate the database for testing
# important: import the testsuite first

def init_for_testing():
    # make sure there's a testsuite present
    found_testsuite = False
    for testsuite_type in common.TESTSUITE_TYPE:
        ts = TestSuite.objects.get_most_recent_testsuite(testsuite_type[0])
        if ts == None:
            print "Warning: No testsuite for {0}".format(testsuite_type[1])
        else:
            found_testsuite = True

    if found_testsuite == False:
        print "Could not initialize: no testsuites present."
        return

    users = create_users()
    rses = create_reading_systems(users)

    for rs in rses:
        for testsuite_type in common.TESTSUITE_TYPE:
            create_evaluation(rs, )

def create_users():
    # create 10 users. the first will be an admin.
    users = []
    users.append(add_user("admin", True))
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
    import random
    # use the first 5 users as owners
    oses = ("OSX", "Windows", "Linux")
    rses = []
    for n in range(0, len(users)/2):
        x = random.randrange(0,3)
        rses.append(add_rs("Reader1", users[n], oses[x]))
    return rses


def create_evaluation(reading_system, evalution_type):
    
    

def add_user(username, is_superuser):
    user = models.UserProfile.objects.create_user(username, "test@example.com", "password")
    user.first_name = username
    user.last_name = ""
    user.is_superuser = is_superuser
    user.save()
    return user

def add_rs(name, user, os):
    rs = models.ReadingSystem(
        locale = "",
        name = name,
        operating_system = "OSX",
        notes = "",
        version = "1.0",
        user = user,
    )
    rs.save() 
    return rs
