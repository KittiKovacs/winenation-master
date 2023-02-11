from django.db import models


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Variety(models.Model):

    class Meta:
        verbose_name_plural = 'Varieties'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Wine_region(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):

    sku = models.CharField(max_length=254)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(
        max_length=1024, null=True, blank=True)
    image = models.ImageField(upload_to='', null=True, blank=True)
    category = models.ForeignKey('Category', null=True,
                                 blank=True, on_delete=models.SET_NULL)
    winery = models.CharField(max_length=254, null=True,
                              blank=True)
    country = models.CharField(max_length=254, null=True,
                               blank=True)
    variety = models.ForeignKey('Variety', null=True, blank=True,
                                on_delete=models.SET_NULL, max_length=254)
    vintage = models.IntegerField(null=True, blank=True)
    region = models.ForeignKey('Wine_region', null=True, blank=True,
                               on_delete=models.SET_NULL, max_length=254)
    alc_vol = models.DecimalField(null=True, blank=True,
                                  max_digits=6, decimal_places=2)
    pairing = models.CharField(null=True, blank=True, max_length=254)
    is_a_subscription = models.BooleanField(default=False)

    def __str__(self):
        return self.name
