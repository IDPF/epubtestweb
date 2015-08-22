from testsuite.models import *
import import_testsuite

# to be called after the epubs are imported into the database
# config_section = top-level testsuite YAML config section
def import_features(config_section, testsuite):
    categories = config_section['Categories']
    for category in categories:
        db_category = testsuite.get_category_by_id(category['Id'])

        for feature in category['Features']:
            db_feature = import_testsuite.add_feature(feature['Id'], feature['Name'], db_category)

            for testid in category['TestIds']:
                db_test = testsuite.get_test_by_id(testid)
                if db_test == None:
                    print "Warning: test {0} not found in database.".format(testid)
                else:
                    db_test.feature = db_feature
                    db_test.save()

    sanity_check(testsuite)


# check that all database tests have features assigned to them
def sanity_check(testsuite):
    tests = testsuite.get_tests()
    for test in tests:
        if test.feature == None:
            print "Warning: test {0} does not belong to a feature.".format(test.testid)


    

