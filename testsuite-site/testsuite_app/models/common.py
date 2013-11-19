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
RESULT_NOT_ANSWERED = None

RESULT_TYPE = (
    (RESULT_SUPPORTED, "Supported"),
    (RESULT_NOT_SUPPORTED, "Not Supported"),
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

