from django.db import models
from django.db.models.fields import BooleanField
from django.contrib.postgres.fields import ArrayField

from agents.models import Agent

class Groups(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=True)
    status = models.BooleanField(null=False, default=True)
    autojoin_enabled = models.BooleanField(null=False, default=False)
    autojoin_filters = ArrayField(
        models.CharField(max_length=255, null=False, blank=True),
        null=False,
        blank=True,
        default=list,
    )
