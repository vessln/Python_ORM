from django.db import models


class MixinIsAwarded(models.Model):
    class Meta:
        abstract = True

    is_awarded = models.BooleanField(default=False)


class MixinLastUpdated(models.Model):
    class Meta:
        abstract = True

    last_updated = models.DateTimeField(auto_now=True)