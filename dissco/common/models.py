from django.contrib.auth.models import User
from django.db import models


class Institution(models.Model):
    name = models.CharField(max_length=1000)
    code = models.TextField(max_length=255, blank=True)
    wikidata_id = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return f'{self.name} [{self.code}]'


class InstitutionUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
