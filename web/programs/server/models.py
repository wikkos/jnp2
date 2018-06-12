from django.db import models


class Execution(models.Model):
    RUNNING = 0
    EXECUTED = 1
    FAILED = 2

    username = models.CharField(max_length=100)
    folderName = models.CharField(max_length=200)
    timeExecuted = models.DateTimeField()
    status = models.IntegerField()