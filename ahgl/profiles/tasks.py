from celery.task import task
from account.models import AccountDeletion

@task(name="profiles.tasks.expunge_deleted", ignore_result=True)
def expunge_deleted():
    return AccountDeletion.expunge()
