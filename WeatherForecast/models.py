from django.db import models


class PolishCity(models.Model):
    name = models.CharField(max_length=35)
    country_code = models.CharField(max_length=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Polish cities'


class WorldwideCity(models.Model):
    name = models.CharField(max_length=50)
    country_code = models.CharField(max_length=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Worldwide cities'


class FavouriteCity(models.Model):
    name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Favourite cities'
