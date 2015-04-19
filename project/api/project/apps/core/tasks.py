from __future__ import absolute_import

from celery import shared_task
from django.core.management import call_command


@shared_task
def send_queued_mail_async():
    call_command('send_queued_mail', interactive=False)
