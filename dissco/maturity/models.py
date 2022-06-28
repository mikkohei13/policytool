from django.db import models

from common.models import Institution


class Category(models.Model):
    name = models.TextField()
    description = models.TextField()


class SubCategory(models.Model):
    class Period(models.TextChoices):
        CURRENT = 'current'
        FUTURE_12 = 'future_12'

    prompt = models.TextField()
    period = models.TextField(choices=Period.choices)
    order = models.IntegerField(default=0)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)


class InstitutionSubCategory(models.Model):
    value = models.IntegerField()
    comment = models.TextField(blank=True)
    subcategory = models.ForeignKey(SubCategory, related_name='institution_subcategories',
                                    on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, related_name='subcategories',
                                    on_delete=models.CASCADE)
