from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class User(models.Model):
    
    def __str__(self):
        return str(self.id)
    
    
class Book(models.Model):
    ISBN = models.CharField(max_length = 100, primary_key = True)
    title = models.CharField(max_length = 100)
    author = models.CharField(max_length = 50)
    publicationYear = models.CharField(max_length = 4)
    publisher = models.CharField(max_length = 50)
    ratings = models.ManyToManyField(User, through = "Rating")
    
    def __str__(self):
        return self.title
    
    
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    book = models.ForeignKey(Book, on_delete = models.CASCADE)
    ratingValue = models.PositiveSmallIntegerField(validators = [MinValueValidator(1), MaxValueValidator(10)])
    
    def __str__(self):
        return str(self.ratingValue)
