from .models import common

def user_can_edit_reading_system(user, reading_system):
    return user.is_superuser or user == reading_system.user

def user_can_edit_evaluation(user, evaluation):
    return evaluation.user == user or user.is_superuser

def user_can_publish_evaluation(user, evaluation):
    return user.is_superuser

