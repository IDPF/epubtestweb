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

    if user == rs.user and new_visibility != "2": # public
        return True

def user_can_view_reading_system(user, rs, context):
    """Can view: user can see that this RS exists and can view data entered for it.
    context indicates the page that we're viewing on (i.e. 'manage' or 'index') """
    if context == 'index':
        return rs.visibility == '2' #public
    elif context == 'manage':
        # all logged-in users can see members-only or public reading systems
        if rs.visibility == "1" or rs.visibility == "2":
            return True
        else: #if r.visibility == "3", then only the owner can view
            return user == rs.user
    else:
        return False

