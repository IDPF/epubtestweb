from testsuite.models import ReadingSystem, Test, Result, Category, TestSuite
from lxml.builder import ElementMaker
from lxml import etree
from testsuite import helper_functions
from testsuite.models import common
import permissions

E = ElementMaker(namespace="http://idpf.org/ns/testsuite",
		nsmap={'ts' : "http://idpf.org/ns/testsuite"})

DOC = E.evaluations
EVAL = E.evaluation
RESULT_SET = E.resultset
RS = E.readingSystem
RESULT = E.result
CATEGORY = E.category
TEST = E.test
NOTES = E.notes

# export a document containing all reading systems
def export_all_current_reading_systems(user):
	reading_systems = ReadingSystem.objects.all()
	xmldoc = DOC()

	for rs in reading_systems:
		rs_elm = export_reading_system(rs, user)
        if rs_elm != None:
            xmldoc.append(rs_elm)
	tree = etree.ElementTree(xmldoc)
	return tree

# export a document containing a single reading system
def export_single_reading_system(rs, user):
    xmldoc = DOC()
    rs_elm = export_reading_system(rs, user)
    if rs_elm != None:
        xmldoc.append(rs_elm)
    tree = etree.ElementTree(xmldoc)
    return tree

# export the single reading system XML
def export_reading_system(rs, user):
    can_view = permissions.user_can_view_reading_system(user, rs, 'manage')
    #user == None means we are running the CLI
    if can_view or user == None: 
        return rs_to_xml(rs)

    return None

def rs_to_xml(rs):
    testsuite = TestSuite.objects.get_most_recent_testsuite()
    accessibility_testsuite = TestSuite.objects.get_most_recent_accessibility_testsuite()
    #testsuite_date = "{0}-{1}".format(testsuite.version_date, testsuite.version_revision)
    testsuite_date = str(testsuite.version_date)
    #accessibility_testsuite_date = "{0}-{1}".format(accessibility_testsuite.version_date, accessibility_testsuite.version_revision)
    accessibility_testsuite_date = str(accessibility_testsuite.version_date)
    
    testsuite_data = helper_functions.testsuite_to_dict(testsuite)
    accessibility_testsuite_data = helper_functions.testsuite_to_dict(accessibility_testsuite)
    
    rs_elm = RS(name=rs.name, version=rs.version, operating_system=rs.operating_system, locale=rs.locale, notes=rs.notes)
    result_set_elm = result_set_to_xml(rs, rs.get_default_result_set(), testsuite, testsuite_data, testsuite_date)
    rs_elm.append(result_set_elm)

    accessibility_result_sets = rs.get_accessibility_result_sets()

    for accessibility_result_set in accessibility_result_sets:
        accessibility_result_set_elm = result_set_to_xml(rs, accessibility_result_set, \
            accessibility_testsuite, accessibility_testsuite_data, accessibility_testsuite_date)
        rs_elm.append(accessibility_result_set_elm)	
    print etree.tostring(rs_elm)
    return rs_elm

def result_set_to_xml(rs, result_set, testsuite, testsuite_data, testsuite_date):
    testsuite_type = "DEFAULT"
    if testsuite.testsuite_type == common.TESTSUITE_TYPE_ACCESSIBILITY:
        testsuite_type = "ACCESSIBILITY"
    result_set_elm = RESULT_SET(
        testsuite_date = str(testsuite_date), 
        testsuite_type = testsuite_type, 
        last_updated = str(result_set.last_updated)
    )
    for item in testsuite_data:
        top_level_category_elm = category_to_xml(item, rs, result_set)
        result_set_elm.append(top_level_category_elm)

    return result_set_elm

def category_to_xml(category, rs, result_set):
    category_score = result_set.get_category_score(category['item'])
    category_elm = CATEGORY(name=category['item'].name, score=str(category_score.pct_total_passed))
    for t in category['tests']:
        result = result_set.get_result_for_test(t)
        result_elm = result_to_xml(result)
        category_elm.append(result_elm)
    
    for subcat in category['subcategories']:
		subcat_elm = category_to_xml(subcat, rs, result_set)
		category_elm.append(subcat_elm)

    return category_elm

def result_to_xml(r):
    test_elm = TEST(testid=r.test.testid, name=r.test.name, required=str(r.test.required))
    resultstr = result_to_string(r)
    result_elm = RESULT(test_elm, result = resultstr)
    if r.notes != None and len(r.notes) > 0:
        notes_elm = NOTES(r.notes)
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
	

