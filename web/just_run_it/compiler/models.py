from enum import Enum

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone


class Submission(models.Model):
    C = 'C'
    CPP17 = 'CPP17'
    PYTHON3 = 'PYTHON3'
    LANGUAGES = (
        (C, 'gcc'),
        (CPP17, 'g++17'),
        (PYTHON3, 'python3')
    )

    SU = 'SU'
    OK = 'OK'
    STATUSES = (
        (SU, 'submitted'),
        (OK, 'completed successfully')
    )

    created = models.DateTimeField(editable=False)
    user = models.ForeignKey(User, verbose_name='author of the source code', on_delete=models.CASCADE)

    content = models.TextField('Your source code')
    input = models.TextField(blank=True)
    language = models.CharField(max_length=10,
                                choices=LANGUAGES,
                                default=C)

    status = models.CharField(max_length=3, choices=STATUSES, default=SU)
    err_code = models.IntegerField('Error code of the program', null=True)
    output = models.TextField('Written to standard output')
    err_output = models.TextField('Written to standard error output')

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        return super(Submission, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.created.strftime('%H:%M:%S %d.%m.%Y')) + \
               " " + str(self.language) + \
               " " + str(self.status) + \
               " " + str(self.err_code)