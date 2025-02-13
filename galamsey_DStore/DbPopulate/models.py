from django.db import models


# Table 1: csvfiledata
class CsvFileData(models.Model):
    Id = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=100)
    createdAt = models.CharField(max_length=100)
    Numberofrecords = models.IntegerField()

    def __str__(self):
        return f"File: {self.filename}, Records: {self.Numberofrecords}, Created At: {self.createdAt}"


# Table 2: GSiteData
class GSiteData(models.Model):
    Id = models.AutoField(primary_key=True)
    Town = models.CharField(max_length=100)
    Region = models.CharField(max_length=100)
    Number_of_Galamsay_Sites = models.IntegerField()
    csvfileid = models.ForeignKey(CsvFileData, on_delete=models.CASCADE)  # Foreign Key to CsvFileData

    class Meta:
        verbose_name_plural = "GSite Data"  # Fixes Django admin pluralization

    def __str__(self):
        return f"Region: {self.Region}, Town: {self.Town}, Sites: {self.Number_of_Galamsay_Sites}"

        #        return f"The Region [{self.Region}] has [{self.Number_of_Galamsay_Sites}] Galamsay sites in the [{self.Town}] city"
