def generate_timestamp():
    from datetime import datetime
    from django.utils.timezone import utc
    return datetime.utcnow().replace(tzinfo=utc)

def force_score_refresh():
    from testsuite_app.models.evaluation import Evaluation
    evaluations = Evaluation.objects.all()
    for evaluation in evaluations:
        evaluation.update_scores()


