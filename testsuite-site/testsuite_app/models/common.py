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

CATEGORY_EXTERNAL = "1"
CATEGORY_EPUB = "2"
CATEGORY_INTERNAL = "3"

CATEGORY_TYPE = (
    (CATEGORY_EXTERNAL, "External"),
    (CATEGORY_EPUB, "Epub"),
    (CATEGORY_INTERNAL, "Internal"),
)

RESULT_SUPPORTED = "1"
RESULT_NOT_SUPPORTED = "2"
RESULT_NOT_APPLICABLE = "3"
RESULT_NOT_ANSWERED = None

RESULT_TYPE = (
    (RESULT_NOT_ANSWERED, "---------"), # TODO a way to make this appear by default as in RESULT_NA_TYPE ?
    (RESULT_SUPPORTED, "Supported"),
    (RESULT_NOT_SUPPORTED, "Not Supported"),
)

RESULT_NA_TYPE = (
    (RESULT_SUPPORTED, "Supported"),
    (RESULT_NOT_SUPPORTED, "Not Supported"),
    (RESULT_NOT_APPLICABLE, "Not Applicable"),
)

ACCESS_TYPE_KEYBOARD = "1"
ACCESS_TYPE_MOUSE = "2"
ACCESS_TYPE_TOUCH = "3"

ACCESS_TYPE = (
    (ACCESS_TYPE_KEYBOARD, "Keyboard access to all features"),
    (ACCESS_TYPE_MOUSE, "Mouse access to all features"),
    (ACCESS_TYPE_TOUCH, "Touchscreen access to all features"),
)

TESTSUITE_TYPE_DEFAULT = "1"
TESTSUITE_TYPE_ACCESSIBILITY = "2"
TESTSUITE_TYPE = (
    (TESTSUITE_TYPE_DEFAULT, "Default"),
    (TESTSUITE_TYPE_ACCESSIBILITY, "Accessibility"),
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

