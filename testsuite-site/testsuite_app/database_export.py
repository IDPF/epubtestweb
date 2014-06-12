"""export all the database data into JSON
then it can be easily redigested into a new object model.
this is different from export_data, which exports XML for users' consumption.

sample output

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
            'visibility': 'public',
            'evaluation': 
                {
                    'last_updated': '2014-04-03',
                    'results':
                    [
                        {
                            'testid': 'epubnav-010',
                            'result': 'NOT_SUPPORTED',
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

import json
from testsuite_app.models import ReadingSystem, Evaluation, Test, Result, Category, TestSuite
from testsuite_app.models import common

def export_database_as_json_string():
    reading_system_data = export_reading_systems()
    testsuite_data = export_testsuite()
    data = {'reading_systems': reading_system_data, 'testsuite': testsuite_data}
    return json.dumps(data, indent=4)

def export_reading_systems():
    # return an array of reading systems
    reading_systems = ReadingSystem.objects.all()
    data = []
    for rs in reading_systems:
        evaluation = rs.get_current_evaluation()
        # don't add reading systems for which there is no evaluation
        if evaluation != None:
            rs_info = {
                "name": rs.name, 
                "version": rs.version, 
                "operating_system": rs.operating_system, 
                "locale": rs.locale, 
                "sdk_version": rs.sdk_version, 
                "visibility": rs.visibility, 
                "username": rs.user.username
            }
            rs_info['evaluation'] = export_evaluation(evaluation)
            data.append(rs_info)
        else:
            print "WARNING: null evaluation for {0}".format(rs.name)
    return data    

def export_evaluation(evaluation):
    # return a dictionary about the evaluation
    data = {
        "last_updated": str(evaluation.last_updated), 
        "results": []
    }
    results = evaluation.get_all_results()
    for result in results:
        result_data = {
            "testid": result.test.testid,
            "result": result.result,
            "notes": result.notes,
            "publish_notes": result.publish_notes
        }
        data['results'].append(result_data)
    return data

def export_testsuite():
    testsuite = TestSuite.objects.get_most_recent_testsuite()
    data = {
        "date": str(testsuite.version_date),
        "revision": testsuite.version_revision,
        "tests": []
    }
    tests = Test.objects.filter(testsuite = testsuite)
    for test in tests:
        test_data = {
            "testid": test.testid,
            "flagged_as_new": test.flagged_as_new,
            "flagged_as_changed": test.flagged_as_changed
        }
        data['tests'].append(test_data)
    return data
