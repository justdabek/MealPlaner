from django.db import models

class Product(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=40)
    kcalPer100g=models.IntegerField()
    proteinsPer100g=models.FloatField()
    fiberPer100g=models.FloatField()
    fatPer100g=models.FloatField()