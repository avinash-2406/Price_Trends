from django.db import models

class TestData(models.Model):
    firstname = models.CharField(max_length=10)
    lastname = models.CharField(max_length=10)
    email = models.EmailField(null=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"



class PriceData(models.Model):
    location = models.CharField(max_length=200)
    year = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.location} - {self.year} - {self.price}"
