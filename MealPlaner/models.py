from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Product(models.Model):
    id=models.AutoField(auto_created=True, primary_key=True)
    name=models.CharField(max_length=40)
    kcalPer100g=models.IntegerField()
    proteinsPer100g=models.FloatField()
    fiberPer100g=models.FloatField()
    fatPer100g=models.FloatField()

class Goal(models.Model):
    MALE = 'Male'
    FEMALE = 'Female'
    SEX_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]

    RARELY = 'Rarely'
    MODERATELY= 'Moderately'
    OFTEN= 'Often'
    ACTIVITY_CHOICES = [
        (RARELY, 'Rarely'),
        (MODERATELY, 'Moderately'),
        (OFTEN, 'Often'),
    ]

    activity_wages = {'Rarely': 1.4, 'Moderately': 1.7, 'Often': 2.0}
    
    user_id = models.CharField(max_length=100, blank=True)
    activity = models.CharField(max_length=10,  choices=ACTIVITY_CHOICES)
    age = models.DecimalField(decimal_places=0, max_digits=3, validators=[
        MaxValueValidator(150),
        MinValueValidator(0)
        ]       
    )
    sex = models.CharField(max_length=10,  choices=SEX_CHOICES)
    height_cm = models.DecimalField(decimal_places=1, max_digits=4, validators=[
        MaxValueValidator(300),
        MinValueValidator(50)
        ]       
    )
    # weight = models.DecimalField(decimal_places=1, max_digits=3)
    target_weight = models.DecimalField(decimal_places=1, max_digits=4, validators=[
        MaxValueValidator(500),
        MinValueValidator(1)
        ]       
    )
    # target_time_weeks = models.DecimalField(decimal_places=0, max_digits=3)  
    target_kcal = 0.0

    def get_kcal_needed(self):
        ## ze wzoru Mifflina - St. Jeor
        if self.sex == "Male":
            self.target_kcal = 10*float(self.target_weight) + 6.25 * float(self.height_cm) - 5 * float(self.age) + 5     # PPM 
            self.target_kcal = self.target_kcal * self.activity_wages.get(self.activity, 0)                                # CPM
            print("------KCAL-------")
            print(self.target_kcal)

        elif self.sex == "Female":
            self.target_kcal = 10*float(self.target_weight) + 6.25 * float(self.height_cm) - 5 * float(self.age) - 161   # PPM
            self.target_kcal = self.target_kcal * self.activity_wages.get(self.activity, 0)                                # CPM
            print("------KCAL-------")
            print(self.target_kcal)
        else: 
            assert 0, "Wrong sex given"
        
    # def __str__(self):
    #     return self.name

# class Meal(models.Model):
#     MEAL_TYPES=(('S','Sniadanie'),('O','Obiad'),('K','Kolacja'))
#     id=models.IntegerField(primary_key=True)
#     date=models.DateField()
#     typeOfMeal=models.CharField(choices=MEAL_TYPES, max_length=2)
#     products=models.ManyToManyField(Product, blank=True)

class Breakfast(models.Model):
    id=models.AutoField(auto_created=True, primary_key=True)
    date=models.DateField()
    products=models.ManyToManyField(Product, blank=True)

class Lunch(models.Model):
    id=models.AutoField(auto_created=True, primary_key=True)
    date=models.DateField()
    products=models.ManyToManyField(Product, blank=True)

class Dinner(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    date = models.DateField()
    products = models.ManyToManyField(Product, null=True, blank=True)
