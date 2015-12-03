# this is specifically for importing pre-fall-2015 site data
# user profiles are not supported yet, so all evals are credited to 'tester'

import testsuite_app.models.common
from testsuite_app.models import *
from lxml import etree

NSMAP = {"ts": "http://idpf.org/ns/testsuite"}

def import_migration_data(filepath):
    user = create_dummy_user()
    p = etree.XMLParser(remove_blank_text = True)
    f = open(filepath)
    fdata = f.read()
    doc = etree.XML(fdata.encode('utf-8'), parser = p)
    reading_system_elms = doc.xpath("//ts:readingSystem", namespaces = NSMAP)
    for reading_system_elm in reading_system_elms:
        reading_system = add_reading_system(reading_system_elm, user)
        result_set_elms = reading_system_elm.xpath("ts:resultset", namespaces = NSMAP)
        for result_set_elm in result_set_elms:
            add_evaluation(reading_system, result_set_elm, user)


def create_dummy_user():
    user = UserProfile.objects.create_user("tester", "test@example.com", "password")
    user.first_name = "tester"
    user.last_name = ""
    user.is_superuser = False
    user.save()
    return user

def add_reading_system(reading_system_elm, user):
    rs = ReadingSystem(
        name = reading_system_elm.attrib['name'],
        operating_system = reading_system_elm.attrib['operating_system'],
        user = user,
        version = reading_system_elm.attrib['version'],
        notes = reading_system_elm.attrib['notes']
    )
    rs.save()
    # status is now stored on evaluations, not the reading system. we need to track it here temporarily by
    # storing it with the rs object, but it won't go in the db
    rs.status = reading_system_elm.attrib['status']
    return rs

def add_evaluation(reading_system, result_set_elm, user):
    # locate the corresponding testsuite 
    testsuite = None
    testsuite_type = result_set_elm.attrib['testsuite_type']
    if testsuite_type == "DEFAULT":
        testsuite = TestSuite.objects.get_most_recent_testsuite(common.TESTSUITE_TYPE_DEFAULT)
    else:
        testsuite = TestSuite.objects.get_most_recent_testsuite(common.TESTSUITE_TYPE_ACCESSIBILITY)
    
    evaluation = Evaluation.objects.create_evaluation(reading_system, testsuite=testsuite, user = user)
    evaluation.visibility = result_set_elm.attrib['visibility']
    evaluation.status = reading_system.status
    if 'notes' in result_set_elm.attrib.keys():
        evaluation.notes = result_set_elm.attrib['notes']
    evaluation.save()

    results = evaluation.get_results()
    for result in results:
        testid = result.test.test_id
        xpath_expr = "ts:result[@testid='{}']".format(result.test.test_id)
        result_elm = result_set_elm.xpath(xpath_expr, namespaces = NSMAP)[0]
        
        if result_elm != None:
            if result_elm.attrib['result'] == "supported":
                result.result = common.RESULT_SUPPORTED
            elif result_elm.attrib['result'] == "not_supported":
                result.result = common.RESULT_NOT_SUPPORTED
            elif result_elm.attrib['result'] == "incomplete":
                result.result = None
        result.save()

    if testsuite_type == "ACCESSIBILITY":

        evaluation.add_metadata(
            result_set_elm.attrib['assistive_technology'], 
            result_set_elm.attrib['input_type'], 
            str_to_bool(result_set_elm.attrib['supports_screenreader']), 
            str_to_bool(result_set_elm.attrib['supports_braille'])
        )

def str_to_bool(s):
    return s == "True"