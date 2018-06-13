from django.db import models


class Execution(models.Model):
    RUNNING = 0
    EXECUTED = 1
    FAILED = 2

    userName = models.CharField(max_length=100)
    folderName = models.CharField(max_length=150)
    timeExecuted = models.DateTimeField()
    status = models.IntegerField()
    language = models.CharField(max_length=10)
    sid = models.IntegerField
