from testsuite_app.models import ReadingSystem, Evaluation, Test, Result, Category, TestSuite
from lxml.builder import ElementMaker
from lxml import etree
from testsuite_app import helper_functions

E = ElementMaker(namespace="http://idpf.org/ns/testsuite",
		nsmap={'ts' : "http://idpf.org/ns/testsuite"})

DOC = E.evaluations
EVAL = E.evaluation
RS = E.readingSystem
RESULT = E.result
CATEGORY = E.category
RESULTS = E.results
TEST = E.test

def export_all_current_evaluations():
	reading_systems = ReadingSystem.objects.all()
	testsuite = TestSuite.objects.get_most_recent_testsuite()
	xmldoc = DOC(testsuite="{0}-{1}".format(testsuite.version_date, testsuite.version_revision))

	for rs in reading_systems:
		rs_elm = rs_to_xml(rs)
		xmldoc.append(rs_elm)
	tree = etree.ElementTree(xmldoc)
	return tree


def rs_to_xml(rs):
	data = helper_functions.get_results_as_nested_categories(rs)
	results_elm = RESULTS()
	for item in data:
		top_level_category_elm = category_to_xml(item)
		results_elm.append(top_level_category_elm)

	evaluation = rs.get_current_evaluation()
	eval_elm = EVAL(
		RS(name=rs.name, version=rs.version, operating_system=rs.operating_system, locale=rs.locale, sdk_version=rs.sdk_version),
		results_elm,
		last_updated=str(evaluation.last_updated),	
	)
	return eval_elm

def category_to_xml(category):
	category_elm = CATEGORY(name=category['item'].name, score=str(category['category_score']))
	
	for r in category['results']:
		result_elm = result_to_xml(r)
		category_elm.append(result_elm)

	for subcat in category['subcategories']:
		subcat_elm = category_to_xml(subcat)
		category_elm.append(subcat_elm)

	return category_elm

def result_to_xml(r):
	test_elm = TEST(testid=r.test.testid, name=r.test.name)
	result_elm = RESULT(
		test_elm,
		result = result_to_string(r),)
	return result_elm

def result_to_string(result):
	if result.result == None:
		return "incomplete"
	elif result.result == "1":
		return "pass"
	elif result.result == "2":
		return "fail"
	else:
		return "na"

