from testsuite_app.models import *

# migrate all evaluations to the new testsuite

class MigrateData:
    results = None
    evaluations = None

    def pre_migrate(self, old_testsuite):
        print("Pre Migrate")

        self.results = Result.objects.filter(evaluation__testsuite = old_testsuite)
        for result in self.results:
            result.test_id = result.test.test_id
            result.test_xhtml = result.test.xhtml

        self.evaluations = Evaluation.objects.filter(testsuite = old_testsuite)

    def update_testsuite(self, testsuite):
        for evaluation in self.evaluations:
            evaluation.testsuite = testsuite
            evaluation.save(False)


    def migrate(self):
        print("Migrating data for {} evaluations".format(self.evaluations.count()))

        # clear and recreate all score objects
        for evaluation in self.evaluations:
            scores = Score.objects.filter(evaluation = evaluation)
            scores.delete()
            evaluation.create_score_objects()

        # clear the answers for any changed tests
        for result in self.results:
            try:
                test = Test.objects.get(test_id = result.test_id)
                result.test = test
                if self.compare_xhtml(test.xhtml, result.test_xhtml) == False:
                #if test.xhtml != result.test_xhtml:
                    # clear the current answer because the test has changed
                    result.result = common.RESULT_NOT_ANSWERED
                    result.flagged = True
                result.save()
            # a test may have been removed
            except Test.DoesNotExist:
                result.delete()

        # add results for new tests and update all scores
        for evaluation in self.evaluations:
            tests = evaluation.testsuite.get_tests()
            for test in tests:
                result = evaluation.get_result_for_test(test)
                if result == None:
                    # create a result if a test is new
                    result = Result(evaluation = evaluation, test = test)
                    result.result = common.RESULT_NOT_ANSWERED
                    result.flagged = True
                    result.save()


            evaluation.update_scores()
            print("migrated evaluation ID {}".format(evaluation.id))

    def compare_xhtml(self, comp1, comp2):
        # filter the strings a bit before comparing them
        comp1 = comp1 \
            .replace(" class=\"ftest\"", "") \
            .replace(" class=\"ctest\"", "") \
            .replace(" xmlns=\"http://www.w3.org/1999/xhtml\"", "") \
            .replace(" xmlns:epub=\"http://www.idpf.org/2007/ops\"", "")
        comp2 = comp2 \
            .replace(" class=\"ftest\"", "") \
            .replace(" class=\"ctest\"", "") \
            .replace(" xmlns=\"http://www.w3.org/1999/xhtml\"", "") \
            .replace(" xmlns:epub=\"http://www.idpf.org/2007/ops\"", "")

        return comp1 == comp2
