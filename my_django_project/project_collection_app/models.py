from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class GithubProject(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    rating = models.IntegerField(
             default=1,
             validators=[MaxValueValidator(5), MinValueValidator(1)]
     	     )
    created = models.DateTimeField(auto_now_add = True)
    owner = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)

    def __str__(self):
        return f"Name: {self.name}, Rating: {self.rating}, Created: {self.created}, Owner: {self.owner}"
