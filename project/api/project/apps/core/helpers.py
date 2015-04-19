import os
import uuid
import requests
from HTMLParser import HTMLParser
from random import choice

from django.conf import settings
from post_office import mail

from .tasks import send_queued_mail_async


class HTMLStripper(HTMLParser):
    """
    Removes HTML Tags!
    """

    def __init__(self):
        HTMLParser.__init__(self)
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def make_tuple(x):
    """
    Make  a tuple out a variable x
    """
    return x, x  # str(x) if needed


def strip_tags(value):
    stripper = HTMLStripper()
    stripper.feed(value)
    return stripper.get_data()


def fetch_to_dict(cursor):
    """
    Returns all rows from a cursor as a dict
    """
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def generate_excerpt(value, character_count):
    """
    Returns an excerpt based on character count for a specific value.
    limiting to e.g 100 chars with ... in the end
    """
    stripped_description = strip_tags(value)
    if stripped_description:
        if len(stripped_description) < character_count:
            value_length = len(stripped_description)
            return stripped_description[:value_length].strip()
        else:
            return stripped_description[:character_count].strip() + " ..."


def generate_random_character_sequence(count):
    """
    Generates random characters based on the ASCII library.
    Some characters should not be causing confusion such as 1, I and 0 and O
    """
    chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
    sequence = ''
    for num in range(count):
        sequence += choice(chars)
    return sequence


def send_mail(recipients, template_name, context_values, async=True):
    """
    Sends email and also allows async sending using celery tasks.
    For options See: https://github.com/ui/django-post_office
    """
    try:
        mail.send(
            recipients,
            template=template_name,
            context=context_values
        )
        if async:
            send_queued_mail_async.delay()
    except(ValueError, TypeError) as e:
        raise e


def upload_to(filename, folder_name):
    """
    Uploads file in a specified location.
    """
    uid = uuid.uuid4().get_hex()
    ext = os.path.splitext(filename)[-1]
    return '{folder}/{file_hash}{ext}'.format(
        folder=folder_name,
        file_hash=uid[4:],
        ext=ext
    )

def image_downloader(url, filename):
    image_stream = requests.get(url, stream=True)
    if image_stream.status_code == 200:
        #static_dir = settings.STATICFILES_DIRS
        media_dir = settings.MEDIA_ROOT
        with open(media_dir+'/'+filename, mode='wb') as f:
            for chunk in image_stream.iter_content():
                f.write(chunk)


