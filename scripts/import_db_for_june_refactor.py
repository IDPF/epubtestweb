from testsuite_app.models import *
import json
import dateutil.parser
"""
sample input

{
    'reading_systems':
    [
        {
            'name': 'XYZReader',
            'version': '1.0',
            'locale': 'US',
            'operating_system': 'Windows 3.1',
            'sdk_version': '3.2'
            'user': 'username',
            'visibility': '1',
            'evaluation': 
                {
                    'last_updated': '2014-04-03',
                    'results':
                    [
                        {
                            'testid': 'epubnav-010',
                            'result': '2',
                            'notes': 'Sample note',
                            'publish_notes': 'True'
                        },
                        ... more results ...
                    ]

                }
        },
        ... more reading systems ...
    ],
    'testsuite':
        {
            'version_date': '2014-04-02',
            'version_revision': '1',
            'tests':
            [
                {
                    'testid': 'epubnav-010',
                    'flagged_as_new': 'True',
                    'flagged_as_changed': 'False'
                }
                ... more tests ...
            ]
        } 
}
"""

def import_from_json(filepath):
    # first check that the DB contains users and a testsuite
    if UserProfile.objects.count() == 0:
        print "Warning: no users in DB. Please add users before running this script."
        return
    if TestSuite.objects.count() == 0:
        print "Warning: no testsuite in DB. Please add a testsuite before running this script."
        return
    f = open(filepath)
    data = json.loads(f.read())
    f.close()
    for rs in data['reading_systems']:
        add_rs(rs)

    # import the test flags - the new version of the DB will have a fresh testsuite import, so the flags won't be there
    # the idea is that the same testsuite exists in both DBs
    for test in data['testsuite']['tests']:
        add_test_flags(test)

    # save all rs's result sets to update all its status variables
    rses = ReadingSystem.objects.all()
    for rs in rses:
        rs.get_default_result_set().save()

    print "Done importing"

def add_rs(rs):
    print "Adding reading system {0}".format(rs['name'].encode('utf-8'))
    reading_system = ReadingSystem(
        name = rs['name'],
        version = rs['version'],
        locale = rs['locale'],
        operating_system = rs['operating_system'],
        notes = rs['sdk_version'],
        user = get_user(rs['username']),
        visibility = rs['visibility']
    )
    reading_system.save()
    add_result_set(reading_system, rs['evaluation'])
    return reading_system


def add_result_set(reading_system, evaluation):
    testsuite = TestSuite.objects.get_most_recent_testsuite()
    result_set = ResultSet.objects.create_result_set(reading_system, testsuite, reading_system.user)
    result_set.last_updated = dateutil.parser.parse(evaluation['last_updated'])
    
    for result in evaluation['results']:
        add_result(result_set, result)

    result_set.save()
    return result_set


def add_result(result_set, result):
    existing_result = result_set.get_result_for_test_by_id(result['testid'])
    if existing_result == None:
        print "Warning: result not found for test {0}".format(result['testid'])
        return
    existing_result.result = result['result']
    existing_result.notes = result['notes']
    existing_result.publish_notes = result['publish_notes']
    existing_result.save()

def add_test_flags(test):
    testsuite = TestSuite.objects.get_most_recent_testsuite()
    existing_test = testsuite.get_test_by_id(test['testid'])
    if existing_test == None:
        print "Warning: test {0} does not exist".format(test['testid'])
        return
    existing_test.flagged_as_new = test['flagged_as_new']
    existing_test.flagged_as_changed = test['flagged_as_changed']
    existing_test.save()

def get_user(username):
    try:
        return UserProfile.objects.get(username = username)
    except UserProfile.DoesNotExist:
        print "Warning: user {0} not found".format(username)
        return None




