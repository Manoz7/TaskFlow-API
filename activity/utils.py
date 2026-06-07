from .models import ActivityLog


def log_activity(
    *,
    user,
    action,
    project=None,
    task=None
):
    ActivityLog.objects.create(
        user=user,
        action=action,
        project=project,
        task=task
    )