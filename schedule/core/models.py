# coding=utf-8
from django.db import models


class Course(models.Model):
    name = models.CharField(verbose_name=u'Название', max_length=255)
    start = models.DateField(verbose_name=u'Начало курса')
    end = models.DateField(verbose_name=u'Завершение курса')
    hours = models.IntegerField(verbose_name=u'Количество часов')
    subject = models.ForeignKey('Subject')
    students = models.ManyToManyField('auth.User', through='Vizit', related_name='courses')


class Vizit(models.Model):
    course = models.ForeignKey('Course')
    user = models.ForeignKey('auth.User')


class Department(models.Model):
    name = models.CharField(verbose_name=u'Название', max_length=255)
    address = models.CharField(verbose_name=u'Адрес', max_length=255)
    courses = models.ManyToManyField('Course')


class Organization(models.Model):
    name = models.CharField(verbose_name=u'Название', max_length=255)
    address = models.CharField(verbose_name=u'Адрес', max_length=255)


class Subject(models.Model):
    name = models.CharField(verbose_name=u'Название', max_length=255)
    teacher = models.ForeignKey('auth.User')


class Certificate(models.Model):
    name = models.CharField(verbose_name=u'Название', max_length=255)
    required_hours = models.IntegerField(verbose_name=u'Количество часов')
    course = models.ForeignKey('Course')
