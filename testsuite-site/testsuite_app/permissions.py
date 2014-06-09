from models import common

def user_can_edit_reading_system(user, rs):
    "Edit RS: change details and evaluation"
    return user.is_superuser or user == rs.user

def user_can_delete_reading_system(user, rs):
    "Delete RS: delete rs and its evaluations"
    return user.is_superuser or user == rs.user

def user_can_change_visibility(user, rs, new_visibility):
    "Change visibility: change RS visibility (public, owner-only, members-only)"
    if new_visibility == rs.visibility: # no change
        return False

    if user.is_superuser: # superusers can do anything
        return True

    if user == rs.user and new_visibility != common.VISIBILITY_PUBLIC:
        return True

def user_can_view_reading_system(user, rs, context):
    """Can view: user can see that this RS exists and can view data entered for it.
    context indicates the page that we're viewing on (i.e. 'manage' or 'index') """
    if context == common.CONTEXT_INDEX:
        return rs.visibility == common.VISIBILITY_PUBLIC
    elif context == common.CONTEXT_MANAGE or context == common.CONTEXT_RS:
        # all logged-in users can see members-only or public reading systems
        if rs.visibility == common.VISIBILITY_MEMBERS_ONLY or rs.visibility == common.VISIBILITY_PUBLIC:
            return True
        else: #if r.visibility == common.VISIBILITY_OWNER_ONLY
            return user == rs.user or user.is_superuser
    else:
        return False

def user_can_create_accessibility_eval(user, rs):
    return user_can_view_reading_system(user, rs, common.CONTEXT_MANAGE)

def user_can_edit_accessibility_eval(user, result_set):
    return result_set.user == user or user.is_superuser

def user_can_delete_accessibility_eval(user, result_set):
    return result_set.user == user or user.is_superuser    

def user_can_view_accessibility_eval(user, rs):
    return user_can_view_reading_system(user, rs, common.CONTEXT_MANAGE)

