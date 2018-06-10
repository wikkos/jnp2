from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone


class Submission(models.Model):
    created = models.DateTimeField(editable=False)
    user = models.ForeignKey(User, verbose_name='author of the source code', on_delete=models.CASCADE)

    content = models.TextField('Your source code')
    input = models.TextField()

    status = models.CharField(max_length=30, default='submitted')
    err_code = models.IntegerField('Error code of the program', null=True)
    output = models.TextField('Written to standard output')
    err_output = models.TextField('Written to standard error output')

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        return super(Submission, self).save(*args, **kwargs)


    def __str__(self):
        return str(self.created.strftime('%H:%M:%S %d.%m.%Y')) + " " + str(self.status) + " " + str(self.err_code)
