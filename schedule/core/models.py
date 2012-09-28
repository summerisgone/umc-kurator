# coding=utf-8
from django.core.urlresolvers import reverse
from django.db import models
from schedule import enums


class Course(models.Model):
    name = models.CharField(verbose_name=u'Название', max_length=255)
    start = models.DateField(verbose_name=u'Начало курса')
    end = models.DateField(verbose_name=u'Завершение курса')
    hours = models.IntegerField(verbose_name=u'Количество часов')
    subject = models.ForeignKey('Subject')
    students = models.ManyToManyField('auth.Listener', verbose_name=u'Слушатели',
        through='Vizit', related_name='courses')
    department = models.ForeignKey('Department', related_name='courses', verbose_name=u'Филиал')

    def get_absolute_url(self):
        return reverse('core.course.read', args=(self.pk,))

    def __unicode__(self):
        return u'%s (%s ч.)' % (self.subject, self.hours)


class Vizit(models.Model):
    course = models.ForeignKey('Course', verbose_name=u'Предмет')
    listener = models.ForeignKey('auth.Listener', verbose_name=u'Слушатель')


class Department(models.Model):
    name = models.CharField(verbose_name=u'Название', max_length=255)
    address = models.CharField(verbose_name=u'Адрес', max_length=255,
        null=True, blank=True)

    def get_absolute_url(self):
        return reverse('core.department.read', args=(self.pk,))

    def __unicode__(self):
        return u'Филиал %s' % self.name

class Organization(models.Model):
    name = models.CharField(verbose_name=u'Название', max_length=255)
    number = models.IntegerField(verbose_name=u'Номер', null=True, blank=True)
    address = models.CharField(verbose_name=u'Адрес', max_length=255,
        null=True, blank=True)
    cast = models.CharField(verbose_name=u'Тип организации', max_length=50,
        choices=enums.ORGANIZATION_TYPES, null=True, blank=True)

    def __unicode__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(verbose_name=u'Название', max_length=255)
    teacher = models.ForeignKey('auth.Teacher', verbose_name=u'Педагог')

    def __unicode__(self):
        return self.name


class Certificate(models.Model):
    name = models.CharField(verbose_name=u'Название', max_length=255)
    cast = models.CharField(verbose_name=u'Тип документа', max_length=50,
        choices=enums.DOCUMENT_CAST, null=True, blank=True)
    course = models.ForeignKey('Course', verbose_name=u'Предмет')
    listener = models.ForeignKey('auth.Listener', verbose_name=u'Владелец')

    def __unicode__(self):
        return self.name