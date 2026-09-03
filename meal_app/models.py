from django.db import models
from django.utils import timezone
#Meal Point
# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=45)
    email = models.EmailField(max_length=55)
    phone = models.CharField(max_length=13)
    question = models.TextField() 
    contact_date = models.DateTimeField(default=timezone.now)
class Feedback(models.Model):
    name = models.CharField(max_length=45)
    email = models.EmailField(max_length=55)
    rating = models.CharField(max_length=5)
    review = models.TextField() 
    date = models.DateTimeField(default=timezone.now)
class CustomerDetail(models.Model):
    name = models.CharField(max_length=45)
    email = models.EmailField(max_length=55,primary_key=True)
    password = models.CharField(max_length=55)
    phone = models.CharField(max_length=13)
    profile_pic = models.ImageField(upload_to='photo', default="")
class ManagerDetail(models.Model):
    name=models.CharField(max_length=45)
    email=models.EmailField(max_length=55,primary_key=True)
    password=models.CharField(max_length=55)
    phone=models.CharField(max_length=13)
    city=models.CharField(max_length=60)
    address=models.TextField()
    profile_pic=models.ImageField(default="",upload_to="managerpic")
class MealPlan(models.Model):
    plan_name = models.CharField(max_length=45)
    meals_included = models.TextField()
    duration = models.CharField(max_length=20)
    cost = models.IntegerField()

    plan_image = models.ImageField(
        upload_to='meal_plan/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.plan_name
class Payment(models.Model):
    customer = models.ForeignKey(CustomerDetail,on_delete=models.CASCADE )
    plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE)
    amount = models.IntegerField()
    booking_date = models.DateField(default=timezone.now)
    payment_status = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100)
    def __str__(self):
        return self.customer.name
class UpiDetail(models.Model):
    upiid = models.CharField(
        max_length=100,
        unique=True
    )
    def __str__(self):
        return self.upiid