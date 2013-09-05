SHORT_STRING = 50
LONG_STRING = 255

EVALUATION_TYPE = (
    ("1", "Internal"),
    ("2", "Public"),
    # TODO consider a third type "Temporary"
)

CATEGORY_TYPE = (
    ("1", "External"),
    ("2", "Epub"),
    ("3", "Internal"),
)

RESULT_TYPE = (
    ("1", "Pass"),
    ("2", "Fail"),
    ("3", "NA")
)

class ItemMixin():
    # TODO change to a static property
    def get_depth(self):
        if self.parent_category == None:
            return 0
        else:
            return self.get_depth(self.parent_category) + 1
