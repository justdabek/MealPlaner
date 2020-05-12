from django.db import models

class Product(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=40)
    kcalPer100g=models.IntegerField()
    proteinsPer100g=models.FloatField()
    fiberPer100g=models.FloatField()
    fatPer100g=models.FloatField()

    def __str__(self):
        return self.name

class Meal(models.Model):
    MEAL_TYPES=(('S','Sniadanie'),('O','Obiad'),('K','Kolacja'))
    id=models.IntegerField(primary_key=True)
    date=models.DateField()
    typeOfMeal=models.CharField(choices=MEAL_TYPES, max_length=2)
    products=models.ManyToManyField(Product, blank=True)
