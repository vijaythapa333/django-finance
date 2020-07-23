from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Expense Category")

    def __str__(self):
        return self.name
    
    # To display custome name for the model in admin
    class Meta:
        verbose_name_plural = 'Categories'
    

class Expense(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now, verbose_name="Expense Amount")
    description = models.TextField(verbose_name="Description")
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="Owner")
    category = models.ForeignKey(to=Category, on_delete=models.DO_NOTHING, verbose_name="Expense Category")

    def __str__(self):
        return self.description

    #To get the latest Expense short by date in descending order
    class Meta:
        ordering: ['-date']

    


