from django.db import models

SHORT_STRING = 50
LONG_STRING = 255

VISIBILITY_MEMBERS_ONLY = "1"
VISIBILITY_PUBLIC = "2"
VISIBILITY_OWNER_ONLY = "3"

VISIBILITY_TYPE = (
    (VISIBILITY_MEMBERS_ONLY, "Members only"),
    (VISIBILITY_PUBLIC, "Public"),
    (VISIBILITY_OWNER_ONLY, "Owner only")
)

RESULT_SUPPORTED = "1"
RESULT_NOT_SUPPORTED = "2"
RESULT_NOT_APPLICABLE = "3"
RESULT_NOT_ANSWERED = None

RESULT_TYPE = (
    (RESULT_SUPPORTED, "Supported"),
    (RESULT_NOT_SUPPORTED, "Not Supported"),
)

RESULT_NA_TYPE = (
    (RESULT_SUPPORTED, "Supported"),
    (RESULT_NOT_SUPPORTED, "Not Supported"),
    (RESULT_NOT_APPLICABLE, "Not Applicable"),
)

TESTSUITE_TYPE_DEFAULT = "1"
TESTSUITE_TYPE_ACCESSIBILITY = "2"
TESTSUITE_TYPE = (
    (TESTSUITE_TYPE_DEFAULT, "default"),
    (TESTSUITE_TYPE_ACCESSIBILITY, "accessibility"),
)

INPUT_TYPE_KEYBOARD = "1"
INPUT_TYPE_MOUSE = "2"
INPUT_TYPE_TOUCH = "3"
INPUT_TYPE = (
    (INPUT_TYPE_KEYBOARD, "Keyboard"),
    (INPUT_TYPE_MOUSE, "Mouse"),
    (INPUT_TYPE_TOUCH, "Touch/Gestures"),
)

READING_SYSTEM_STATUS_TYPE_CURRENT = "1"
READING_SYSTEM_STATUS_TYPE_ARCHIVED = "2"
READING_SYSTEM_STATUS_TYPE = (
    (READING_SYSTEM_STATUS_TYPE_CURRENT, "Current"),
    (READING_SYSTEM_STATUS_TYPE_ARCHIVED, "Archived")
)

TESTSUITE_ALLOW_ONE = "1"
TESTSUITE_ALLOW_MANY = "2"
TESTSUITE_ALLOW = (
    (TESTSUITE_ALLOW_MANY, "Many"),
    (TESTSUITE_ALLOW_ONE, "One")
)

CONTEXT_INDEX = "index"
CONTEXT_MANAGE = "manage"
CONTEXT_RS = "rs"

class ItemMixin():
    # convenience function to calculate depth; used only while saving
	def calculate_depth(self):
		if self.parent_category == None:
			return 0
		else:
			return self.parent_category.calculate_depth() + 1

	def get_parents(self):
		if self.parent_category == None:
			return []
		else:
			parents = [self.parent_category]
			parents.extend(self.parent_category.get_parents())
			return parents

class FloatToDecimalMixin():
    # this is the "right way"...
    # http://docs.python.org/release/2.6.7/library/decimal.html#decimal-faq
    # and this is the way that works in practice (in this case, we can live with rounding error past 2 decimal places)
    def float_to_decimal(self, f):
        from decimal import Decimal
        s = str(f)
        return Decimal(s)

