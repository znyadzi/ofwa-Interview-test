from django.db import models

# Create your models here.

class GSiteData(models.Model):
    Town = models.CharField(max_length=100)
    Region = models.CharField(max_length=100)
    Number_of_Galamsay_Sites = models.IntegerField()

    def __str__(self):
        return f"{self.Town} ({self.Region}) - {self.Number_of_Galamsay_Sites} sites"