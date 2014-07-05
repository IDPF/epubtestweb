from models import common

def user_can_edit_reading_system(user, rs):
    "Edit RS: change details"
    return user.is_superuser or user == rs.user

def user_can_delete_reading_system(user, rs):
    "Delete RS: delete rs and its result sets"
    return user.is_superuser or user == rs.user

def user_can_view_reading_system(user, rs, context):
    """Can view: user can see that this RS exists and can view data entered for it.
    context indicates the page that we're viewing on (i.e. 'manage' or 'index') """
    rsvis = rs.visibility
    if context == common.CONTEXT_INDEX:
        return rsvis == common.VISIBILITY_PUBLIC
    elif context == common.CONTEXT_MANAGE or context == common.CONTEXT_RS:
        # all logged-in users can see members-only or public reading systems
        if rsvis == common.VISIBILITY_MEMBERS_ONLY or rsvis == common.VISIBILITY_PUBLIC:
            return True
        else: #if rsvis == common.VISIBILITY_OWNER_ONLY
            return user == rs.user or user.is_superuser
    else:
        return False

def user_can_create_accessibility_result_set(user, rs):
    # anyone who can see the reading system can add an accessibility config
    return user_can_view_reading_system(user, rs, common.CONTEXT_MANAGE)

def user_can_edit_accessibility_result_set(user, result_set):
    # the accessibility config owner can edit (so can superusers)
    return result_set.reading_system.user == user or user.is_superuser

def user_can_delete_accessibility_result_set(user, result_set):
    # the accessibility config owner can delete (so can superusers)
    return result_set.reading_system.user == user or user.is_superuser    

def user_can_view_accessibility_result_set(user, result_set):
    can_view_rs = user_can_view_reading_system(user, result_set.reading_system, common.CONTEXT_MANAGE)
    print "can view rs {0}".format(can_view_rs)
    if can_view_rs and result_set.visibility == common.VISIBILITY_MEMBERS_ONLY:
        return True
    if can_view_rs and result_set.visibility == common.VISIBILITY_OWNER_ONLY and user == rset.user:
        return True
    if can_view_rs and result_set.visibility == common.VISIBILITY_PUBLIC:
        return True
    return False

#########################
def user_can_edit_result_set(user, rset):
    return user.is_superuser or user == rset.reading_system.user

def user_can_change_reading_system_visibility(user, rs, new_visibility):
    if new_visibility == rs.visibility: # no change
        return False

    if user.is_superuser: # superusers can do anything
        return True

    if user == rset.reading_system.user and new_visibility != common.VISIBILITY_PUBLIC:
        return True
    
    return False

def user_can_change_result_set_visibility(user, rset, new_visibility):
    "Change visibility: change RS visibility (public, owner-only, members-only)"

    if rset == None:
        return False

    if new_visibility == rset.visibility: # no change
        return False

    # basically, it can't be more visible than the reading system itself
    rsvis = rset.reading_system.visibility
    if rsvis == common.VISIBILITY_MEMBERS_ONLY:
        if new_visibility == common.VISIBILITY_PUBLIC:
            return False
    if rsvis == common.VISIBILITY_OWNER_ONLY:
        if new_visibility == common.VISIBILITY_MEMBERS_ONLY:
            return False
        if new_visibility == common.VISIBILITY_PUBLIC:
            return False

    if user.is_superuser: # superusers can do anything
        return True

    if rset == default_result_set:
        if user == rset.reading_system.user and new_visibility != common.VISIBILITY_PUBLIC:
            return True
    else:
        if new_visibility != common.VISIBILITY_PUBLIC:
            return True

    return False