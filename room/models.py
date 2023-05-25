from django.db import models

from core.models import TimeStampedModel
from user.models import User

MESSAGE_ROLE_CHOICES = (
    ("system", "초기설정"), ("assistant", "GPT"), ("user", "유저"),
)


class Room(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Message(TimeStampedModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    audio_url = models.URLField(null=True, blank=True)
    text = models.TextField()
    role = models.CharField(max_length=10, choices=MESSAGE_ROLE_CHOICES)
