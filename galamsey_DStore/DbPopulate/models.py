from django.db import models

# Create your models here.

class GSiteData(models.Model):
    Town = models.CharField(max_length=100)
    Region = models.CharField(max_length=100)
    Number_of_Galamsay_Sites = models.IntegerField()

    class Meta:
        verbose_name_plural = "GSite Data" #Fixes Django admin pluralization
        unique_together = ('Town', 'Region')  # Ensures uniqueness of Town and Region combination

    def __str__(self):
        return f"The Region {self.Region} has {self.Number_of_Galamsay_Sites} Galamsay sites in the {self.Town} city"
