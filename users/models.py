from django.contrib.auth.models import User as BaseUser
from django.db import models


class SubTitle(models.Model):
    title = models.CharField(max_length=50)

    def __unicode__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=50)

    def __unicode__(self):
        return self.title


class User(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    member_id = models.CharField(max_length=20)
    profile_pic_url = models.URLField(null=True, blank=True)
    apk = models.CharField(max_length=20, null=True, blank=True)
    events = models.ManyToManyField(Event, null=True, blank=True)
    sub = models.ManyToManyField(SubTitle, null=True, blank=True)
    age = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.email


class Lead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ManyToManyField(Event, null=True, blank=True)
    days_ago = models.IntegerField(default=0)
    source = models.CharField(max_length=30)

    def __unicode__(self):
        return self.source


class Trial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    event = models.ManyToManyField(Event, null=True, blank=True)
    trial_days = models.IntegerField(default=0)
    subscriptions_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.full_name
