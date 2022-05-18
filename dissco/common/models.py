from django.db import models


class Institution(models.Model):
    name = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    code = models.TextField(max_length=255, blank=True)
    wikidata_id = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return f'{self.name} [{self.code}]'
