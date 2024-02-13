from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass
    #homeaddress = models.CharField(max_length=64)

class State(models.Model):
    name = models.CharField(max_length=32)
    def __str__(self):
        return f"{self.name}"

class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="cities")
    name = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.name}, {self.state.name}"

class PetSitter(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="petsitters")
    name = models.CharField(max_length=64)
    lastname = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    cellphone = models.CharField(max_length=64)
    photoURL = models.CharField(max_length=256)
    edad = models.PositiveSmallIntegerField()
    #
    def __str__(self):
        return f"{self.pk}# {self.name} {self.lastname} from {self.city}"

class PetsType(models.Model):
    description = models.CharField(max_length=128)
    petsitters = models.ManyToManyField(PetSitter, blank=True, related_name="petstypes")
    #
    def __str__(self):
        return f"{self.description}"
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    petsitter = models.ForeignKey(PetSitter, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField()
    comment = models.CharField(max_length=250)
    #
    def __str__(self):
        return f"Post #{self.id} by {self.user} to {self.petsitter}"