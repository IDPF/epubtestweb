# this is specifically for importing pre-fall-2015 site data
# before you run this!
#   1. import the testsuite
#   2. copy the users

from lxml import etree

import testsuite_app.models.common
from testsuite_app.models import *


NSMAP = {"ts": "http://idpf.org/ns/testsuite"}

def import_migration_data(filepath):
    p = etree.XMLParser(remove_blank_text = True)
    f = open(filepath)
    fdata = f.read()
    doc = etree.XML(fdata.encode('utf-8'), parser = p)
    
    reading_system_elms = doc.xpath("//ts:readingSystem", namespaces = NSMAP)
    for reading_system_elm in reading_system_elms:
        reading_system = add_reading_system(reading_system_elm)
        result_set_elms = reading_system_elm.xpath("ts:resultset", namespaces = NSMAP)
        for result_set_elm in result_set_elms:
            add_evaluation(reading_system, result_set_elm)

def add_reading_system(reading_system_elm):
    user = lookup_user(reading_system_elm.attrib['user'])
    rs = ReadingSystem(
        name = reading_system_elm.attrib['name'],
        operating_system = reading_system_elm.attrib['operating_system'],
        user = user,
        version = reading_system_elm.attrib['version'],
        notes = reading_system_elm.attrib['notes']
    )
    # locale is deprecated; move it to 'notes'
    if reading_system_elm.attrib['locale'] != "":
        rs.notes = "{}\n{}".format(rs.notes, "locale = {}".format(reading_system_elm.attrib['locale']))
    rs.save()
    # status is now stored on evaluations, not the reading system. we need to track it here temporarily by
    # storing it with the rs object, but it won't go in the db
    rs.status = reading_system_elm.attrib['status']
    return rs

def add_evaluation(reading_system, result_set_elm):
    # locate the corresponding testsuite 
    testsuite = None
    testsuite_type = result_set_elm.attrib['testsuite_type']
    if testsuite_type == "DEFAULT":
        testsuite = TestSuite.objects.get_most_recent_testsuite(common.TESTSUITE_TYPE_DEFAULT)
    else:
        testsuite = TestSuite.objects.get_most_recent_testsuite(common.TESTSUITE_TYPE_ACCESSIBILITY)

    user = lookup_user(result_set_elm.attrib['user'])
    
    evaluation = Evaluation.objects.create_evaluation(reading_system, testsuite=testsuite, user = user)
    visibility = result_set_elm.attrib['visibility']
    if visibility == "2": #public
        evaluation.is_published = True
    else:
        evaluation.is_published = False
    if reading_system.status == "2": #archived
        evaluation.is_archived = True
    else:
        evaluation.is_archived = False
    
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
    evaluation.update_scores()
    evaluation.update_percent_complete()

def lookup_user(username):
    user = UserProfile.objects.get(username = username)
    return user


def str_to_bool(s):
    return s == "True"