# coding=utf-8
from django.db import models

class Profile(models.Model):
    user = models.ForeignKey('auth.User')
    organization = models.ForeignKey('core.Organization')
