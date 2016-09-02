from django.db import models
import random
import string
import os

from django.db import models
from django.utils.timezone import now as timezone_now

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


def create_random_string(length=30):
    if length <= 0:
        length = 30

    symbols = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join([random.choice(symbols) for x in range(length)])


def upload_to(instance, filename):
    now = timezone_now()
    filename_base, filename_ext = os.path.splitext(filename)
    return 'my_uploads/{}_{}{}'.format(
        now.strftime("%Y/%m/%d/%Y%m%d%H%M%S"),
        create_random_string(),
        filename_ext.lower()
    )


class Attachment(models.Model):
    parent_id = models.CharField(max_length=18)
    file_name = models.CharField(max_length=100)
    attachment = models.FileField(upload_to=upload_to)

class UploadFile(models.Model):
    file = models.FileField(upload_to='textfiles')