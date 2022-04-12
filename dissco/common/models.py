from django.db import models


class Institution(models.Model):
    name = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    code = models.CharField(max_length=10)
    ror_id = models.CharField(max_length=9, blank=True)

    def __str__(self) -> str:
        return f'Institution - {self.name}'
