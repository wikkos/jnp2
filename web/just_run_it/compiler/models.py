from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone


class Submission(models.Model):
    created = models.DateTimeField(editable=False)
    user = models.ForeignKey(User, verbose_name='author of the source code', on_delete=models.CASCADE)

    content = models.TextField('Your source code')
    input = models.TextField()

    err_code = models.IntegerField('Error code of the program', null=True)
    output = models.TextField('Written to standard output')
    err_output = models.TextField('Written to standard error output')

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        return super(Submission, self).save(*args, **kwargs)
