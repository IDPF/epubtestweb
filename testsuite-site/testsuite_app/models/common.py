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

EVALUATION_STATUS_TYPE_CURRENT = "1"
EVALUATION_STATUS_TYPE_ARCHIVED = "2"
EVALUATION_STATUS_TYPE = (
    (EVALUATION_STATUS_TYPE_CURRENT, "Current"),
    (EVALUATION_STATUS_TYPE_ARCHIVED, "Archived")
)

CONTEXT_INDEX = "index"
CONTEXT_MANAGE = "manage"
CONTEXT_RS = "rs"

