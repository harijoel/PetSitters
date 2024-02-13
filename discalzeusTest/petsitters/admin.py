from django.contrib import admin
from .models import User, State, City, PetSitter, PetsType, Review

# Register your models here.
admin.site.register(User)
admin.site.register(State)
admin.site.register(City)
admin.site.register(PetSitter)
admin.site.register(PetsType)
admin.site.register(Review)
