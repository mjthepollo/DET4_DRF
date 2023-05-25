from django.db import models

from core.models import TimeStampedModel
from user.models import User

DRAWING_STATUS_CHOICES = (
    ("active", "활성"), ("inactive", "비활성"),
)

ANIMATIOIN_PURPOSE_CHOICES = (
    ("wait1", "대기1"), ("wait2", "대기2"), ("listen1", "듣는중1"), ("listen2", "듣는중2")
)


class Drawing(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    link = models.URLField()
    status = models.CharField(
        max_length=15, choices=DRAWING_STATUS_CHOICES, default="active")


class Animation(TimeStampedModel):
    drawing = models.ForeignKey(Drawing, on_delete=models.CASCADE)
    link = models.URLField()
    purpose = models.CharField(
        max_length=10, choices=ANIMATIOIN_PURPOSE_CHOICES)
