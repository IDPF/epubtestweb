def generate_timestamp():
    from datetime import datetime
    from django.utils.timezone import utc
    return datetime.utcnow().replace(tzinfo=utc)

def force_score_refresh():
    from testsuite_app.models.evaluation import Evaluation
    evaluations = Evaluation.objects.all()
    for evaluation in evaluations:
        evaluation.update_scores()


def force_percent_complete_refresh():
    from testsuite_app.models.evaluation import Evaluation
    evaluations = Evaluation.objects.all()
    for evaluation in evaluations:
        evaluation.save(generate_timestamp = False) #save triggers update_percent_complete