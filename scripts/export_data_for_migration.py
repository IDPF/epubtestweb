# this is a version of export_data.py that is specifically for the fall 2015 migration/site upgrade
from testsuite_app.models import ReadingSystem, Test, Result, Category, TestSuite
from lxml.builder import ElementMaker
from lxml import etree
from testsuite_app import helper_functions
from testsuite_app.models import common

E = ElementMaker(namespace="http://idpf.org/ns/testsuite",
        nsmap={'ts' : "http://idpf.org/ns/testsuite"})

DOC = E.evaluations
EVAL = E.evaluation
RESULT_SET = E.resultset
RS = E.readingSystem
RESULT = E.result
NOTES = E.notes

# export a document containing all reading systems
def export_data_for_migration():
    reading_systems = ReadingSystem.objects.all()
    xmldoc = DOC()

    for rs in reading_systems:
        rs_elm = rs_to_xml(rs)
        if rs_elm != None:
            xmldoc.append(rs_elm)
    tree = etree.ElementTree(xmldoc)
    return tree

def rs_to_xml(rs):
    testsuite = TestSuite.objects.get_most_recent_testsuite()
    accessibility_testsuite = TestSuite.objects.get_most_recent_accessibility_testsuite()
    
    rs_elm = RS(name=rs.name, version=rs.version, operating_system=rs.operating_system, locale=rs.locale, notes=rs.notes, \
        user=rs.user.username, visibility=rs.visibility, status=rs.status)
    result_set = rs.get_default_result_set()
    if result_set != None:
        result_set_elm = result_set_to_xml(rs, result_set, testsuite)
        rs_elm.append(result_set_elm)

    accessibility_result_sets = rs.get_accessibility_result_sets()

    for accessibility_result_set in accessibility_result_sets:
        if accessibility_result_set != None:
            accessibility_result_set_elm = result_set_to_xml(rs, accessibility_result_set, accessibility_testsuite)
            rs_elm.append(accessibility_result_set_elm) 
    
    return rs_elm

def result_set_to_xml(rs, result_set, testsuite):
    testsuite_type = "DEFAULT"
    if testsuite.testsuite_type == common.TESTSUITE_TYPE_ACCESSIBILITY:
        testsuite_type = "ACCESSIBILITY"
    result_set_elm = RESULT_SET(testsuite_type = testsuite_type)
    if testsuite.testsuite_type == common.TESTSUITE_TYPE_ACCESSIBILITY:
        atmeta = result_set.get_metadata()
        if atmeta != None:
            result_set_elm.attrib['assistive_technology'] = atmeta.assistive_technology
            result_set_elm.attrib['input_type'] = atmeta.input_type
            result_set_elm.attrib['supports_screenreader'] = str(atmeta.supports_screenreader)
            result_set_elm.attrib['supports_braille'] = str(atmeta.supports_braille)
            if atmeta.notes != None:
                result_set_elm.attrib['notes'] = atmeta.notes
            else:
                result_set_elm.attrib['notes'] = ""

    results = result_set.get_results()
    for result in results:
        result_elm = result_to_xml(result)
        result_set_elm.append(result_elm)

    return result_set_elm


def result_to_xml(r):
    resultstr = result_to_string(r)
    result_elm = RESULT(testid=r.test.testid, result = resultstr)
    if r.notes != None and len(r.notes) > 0:
        notes_elm = NOTES(r.notes, publish_notes=str(r.publish_notes))
        result_elm.append(notes_elm)
    return result_elm

def result_to_string(result):
    if result.result == common.RESULT_NOT_ANSWERED:
        return "incomplete"
    elif result.result == common.RESULT_SUPPORTED:
        return "supported"
    elif str(result.result) == common.RESULT_NOT_SUPPORTED:
        return "not_supported"
    return "incomplete"
    

