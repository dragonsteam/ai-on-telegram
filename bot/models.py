from django.db import models


class Record(models.Model):
    user_id = models.IntegerField()
    question = models.TextField()
    answer = models.TextField()