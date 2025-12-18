from django.db import models

class TestData(models.Model):
    firstname = models.CharField(max_length=10)
    lastname = models.CharField(max_length=10)
    email = models.EmailField(null=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"



class PriceData(models.Model):
    final_location = models.CharField(max_length=200)
    year = models.IntegerField()
    city = models.CharField(max_length=100)

    flat_weighted_avg = models.FloatField(null=True, blank=True)
    office_weighted_avg = models.FloatField(null=True, blank=True)
    others_weighted_avg = models.FloatField(null=True, blank=True)
    shop_weighted_avg = models.FloatField(null=True, blank=True)

    flat_50 = models.FloatField(null=True, blank=True)
    office_50 = models.FloatField(null=True, blank=True)
    others_50 = models.FloatField(null=True, blank=True)
    shop_50 = models.FloatField(null=True, blank=True)

    flat_75 = models.FloatField(null=True, blank=True)
    office_75 = models.FloatField(null=True, blank=True)
    others_75 = models.FloatField(null=True, blank=True)
    shop_75 = models.FloatField(null=True, blank=True)

    flat_90 = models.FloatField(null=True, blank=True)
    office_90 = models.FloatField(null=True, blank=True)
    others_90 = models.FloatField(null=True, blank=True)
    shop_90 = models.FloatField(null=True, blank=True)


    def __str__(self):
        return f"{self.final_location} - {self.year}"
    class Meta:
            constraints = [
                models.UniqueConstraint(
                    fields=["final_location", "year", "city"],
                    name="unique_location_year_city"
                )
            ]