from testsuite_app.models import ReadingSystem, Evaluation, Test, Result, Category, TestSuite
from lxml.builder import ElementMaker
from lxml import etree
from testsuite_app import helper_functions
from testsuite_app.models import common
import permissions

E = ElementMaker(namespace="http://idpf.org/ns/testsuite",
		nsmap={'ts' : "http://idpf.org/ns/testsuite"})

DOC = E.evaluations
EVAL = E.evaluation
RS = E.readingSystem
RESULT = E.result
CATEGORY = E.category
RESULTS = E.results
TEST = E.test
NOTES = E.notes

def export_all_current_evaluations(user):
	reading_systems = ReadingSystem.objects.all()
	testsuite = TestSuite.objects.get_most_recent_testsuite()
	xmldoc = DOC(testsuite="{0}-{1}".format(testsuite.version_date, testsuite.version_revision))

	for rs in reading_systems:
		if permissions.user_can_view_reading_system(user, rs, 'manage') or \
		user == None: #None means we are running the CLI
			rs_elm = rs_to_xml(rs)
    		xmldoc.append(rs_elm)
	tree = etree.ElementTree(xmldoc)
	return tree


def rs_to_xml(rs):
	testsuite = TestSuite.objects.get_most_recent_testsuite()
	data = helper_functions.testsuite_to_dict(testsuite)
	results_elm = RESULTS()
	for item in data:
		top_level_category_elm = category_to_xml(item, rs)
		results_elm.append(top_level_category_elm)

	evaluation = rs.get_current_evaluation()
	eval_elm = EVAL(
		RS(name=rs.name, version=rs.version, operating_system=rs.operating_system, locale=rs.locale, sdk_version=rs.sdk_version),
		results_elm,
		last_updated=str(evaluation.last_updated),	
	)
	return eval_elm

def category_to_xml(category, rs):
	evaluation = rs.get_current_evaluation()
	category_score = evaluation.get_category_score(category['item'])
	category_elm = CATEGORY(name=category['item'].name, score=str(category_score.pct_total_passed))
	for t in category['tests']:
		result = evaluation.get_result(t)
		result_elm = result_to_xml(result)
		category_elm.append(result_elm)

	for subcat in category['subcategories']:
		subcat_elm = category_to_xml(subcat, rs)
		category_elm.append(subcat_elm)

	return category_elm

def result_to_xml(r):
	test_elm = TEST(testid=r.test.testid, name=r.test.name)
	result_elm = RESULT(
		test_elm,
		result = result_to_string(r),)
	if r.notes != None and len(r.notes) > 0:
		notes_elm = NOTES(r.notes)
		result_elm.append(notes_elm)
	return result_elm

def result_to_string(result):
	if result.result == common.RESULT_NOT_ANSWERED:
		return "incomplete"
	elif result.result == common.RESULT_SUPPORTED:
		return "supported"
	elif result.result == common.RESULT_NOT_SUPPORTED:
		return "not_supported"
	

