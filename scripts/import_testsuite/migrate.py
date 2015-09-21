def migrate_data(previous_testsuite):
    "look for any tests that haven't changed since the last import and copy reading system results over"
    print "Looking for data to migrate"
    reading_systems = ReadingSystemVersion.objects.all()
    testsuite = None
    if previous_testsuite.testsuite_type == common.TESTSUITE_TYPE_DEFAULT:
        testsuite = TestSuite.objects.get_most_recent_testsuite()
    else:
        testsuite = TestSuite.objects.get_most_recent_accessibility_testsuite()
    
    for rs in reading_systems:
        old_result_sets = rs.get_result_sets_for_testsuite(previous_testsuite)
        for old_rset in old_result_sets:
            new_result_set = Evaluation.objects.create_evaluation(rs, testsuite, old_rset.user)
            new_result_set.copy_metadata(old_rset)

            
            print "Migrating data for {0} {1} {2}".format(rs.name.encode('utf-8'), rs.version.encode('utf-8'), rs.operating_system.encode('utf-8'))
            results = new_result_set.get_results()
            print "Processing {0} results".format(results.count())
            
            for result in results:
                try:
                    old_test_version = Test.objects.get(testsuite = previous_testsuite, test_id = result.test.test_id)
                except Test.DoesNotExist:
                    # the test may be new
                    print("No previous version of test {0} was found".format(result.test.test_id))
                    result.test.flagged_as_new = True
                    result.test.save()
                    continue

                # if the ID (checked above) and xhtml for the test matches, then copy over the old result
                if result.test.xhtml == old_test_version.xhtml:
                    previous_result = old_rset.get_result_for_test_by_id(result.test.test_id)
                    result.result = previous_result.result
                    result.notes = previous_result.notes
                    result.save()
                else:
                    print("Test {0} has changed from the previous test suite".format(result.test.test_id))
                    result.test.flagged_as_changed = True
                    result.test.save()
            new_result_set.save()


