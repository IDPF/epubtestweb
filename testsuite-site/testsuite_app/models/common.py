SHORT_STRING = 50
LONG_STRING = 255

EVALUATION_TYPE = (
    ("1", "Internal"),
    ("2", "Public"),
)

CATEGORY_TYPE = (
    ("1", "External"),
    ("2", "Epub"),
    ("3", "Internal"),
)

RESULT_TYPE = (
    ("1", "Supported"),
    ("2", "Not Supported"),
)

class ItemMixin():
    # TODO change to a static property
    def get_depth(self):
        if self.parent_category == None:
            return 0
        else:
            return self.parent_category.get_depth() + 1
