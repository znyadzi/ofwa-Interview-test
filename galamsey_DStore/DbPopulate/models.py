from typing import Any

from django.db import models

# Create your models here.

class UploadedFile(models.Model):
    id = models.AutoField(primary_key=True)
    FileName = models.CharField(max_length=150)
    DateUploaded = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(args, kwargs)
        self.id = None

    def __str__(self):
        return f"[{self.id}] [{self.FileName}] - [{self.DateUploaded}]"

class SiteRecords(models.Model):
    id = models.AutoField(primary_key=True)
    Town = models.CharField(max_length=200)
    Region = models.CharField(max_length=200)
    Number_of_Galamsay_Sites = models.IntegerField()
    FileID = models.ForeignKey(UploadedFile, on_delete=models.CASCADE, related_name='FileID')

    def __str__(self):
        return f"[{self.id}] [{self.Town}] - [{self.Region}] - [{self.Number_of_Galamsay_Sites}] - [{self.FileID}]"