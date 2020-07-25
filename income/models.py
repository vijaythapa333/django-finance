from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Source(models.Model):
    name = models.CharField(max_length=255, verbose_name="Income Category")

    def __str__(self):
        return self.name
    

class Income(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now, verbose_name="Income Amount")
    description = models.TextField(verbose_name="Description")
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="Owner")
    source = models.ForeignKey(to=Source, on_delete=models.DO_NOTHING, verbose_name="Income Source")

    def __str__(self):
        return self.description

    #To get the latest Expense short by date in descending order
    class Meta:
        ordering: ['-date']

    


