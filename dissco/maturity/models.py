from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.TextField()
    description = models.TextField()


class Period(models.TextChoices):
    CURRENT = 'current'
    FUTURE_12 = 'future_12'


class Question(models.Model):
    prompt = models.TextField()
    period = models.TextField(choices=Period.choices)
    order = models.IntegerField(default=0)
    category = models.ForeignKey(Category, related_name='questions', on_delete=models.CASCADE)


class ResponderType(models.TextChoices):
    TEAM = 'team'
    ORGANISATION = 'organisation'
    NODE = 'node'


class Responder(models.Model):
    type = models.TextField(choices=ResponderType.choices)
    name = models.TextField()
    comment = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'owner'], name='unique_name_owner'),
        ]

    def __str__(self) -> str:
        return f'{self.type}: {self.name} [owner: {self.owner.username}]'


class Answer(models.Model):
    value = models.IntegerField()
    comment = models.TextField(blank=True)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    responder = models.ForeignKey(Responder, related_name='answers', on_delete=models.CASCADE)
