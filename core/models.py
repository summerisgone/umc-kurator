# coding=utf-8
from datetime import date
from dateutil.relativedelta import relativedelta
from django.core.urlresolvers import reverse
from django.db import models
from auth.models import Listener
from core.enums import StudyGroupStatus
import enums


def query_set_factory(query_set_class):
    """Allows to use QuerySet methods in chain"""
    class ChainedManager(models.Manager):

        def get_query_set(self):
            return query_set_class(self.model)

        def __getattr__(self, attr, *args):
            try:
                return getattr(self.__class__, attr, *args)
            except AttributeError:
                return getattr(self.get_query_set(), attr, *args)
    return ChainedManager()

class GroupQuerySet(models.query.QuerySet):

    def available_for_enroll(self):
        period = date.today() + relativedelta(days=+2)
        return self.filter(status=enums.StudyGroupStatus.Pending, start__lte=period)

class StudyGroup(models.Model):
    start = models.DateField(verbose_name=u'Начало курса')
    end = models.DateField(verbose_name=u'Завершение курса')
    hours = models.IntegerField(verbose_name=u'Количество часов', choices=enums.HOURS_CHOICES)
    subject = models.ForeignKey('Subject', verbose_name=u'Направление')
    students = models.ManyToManyField('auth.Listener', verbose_name=u'Слушатели',
        through='Vizit', related_name='group')
    department = models.ForeignKey('Department', related_name='groups',
        verbose_name=u'Структурное продразделение')
    status = models.IntegerField(verbose_name=u'Статус группы',
        choices=enums.STUDY_GROUP_STATUSES, default=enums.StudyGroupStatus.Pending)
    number = models.IntegerField(verbose_name=u'Номер группы', null=True, blank=True)

    objects = query_set_factory(GroupQuerySet)

    class Meta:
        ordering = ['start', 'number', 'id']

    def get_absolute_url(self):
        return reverse('department:studygroup_detail', args=(self.department.pk, self.pk,))

    def organizations(self):
        return Organization.objects.filter(listener__vizit__group=self).distinct()

    def lateness(self):
        return (self.start - date.today()).days

    def save(self, *args, **kwds):
        # логика автоматической нумерации при создании
        if not self.pk and not self.number:
            if StudyGroup.objects.exists():
                last_number = StudyGroup.objects.order_by('number','-start')[0].number
                print 'last_number', last_number
            else:
                last_number = 0
            self.number = last_number + 1
        return super(StudyGroup, self).save(*args, **kwds)

    def __unicode__(self):
        return u'%s-%s' % (self.subject, self.hours)


def update_group_numbers():
    """
    Логика автоматической нумерации по запросу
    """
    if StudyGroup.objects.exclude(status=StudyGroupStatus.Pending).exists():
        last_number = StudyGroup.objects.exclude(status=StudyGroupStatus.Pending).order_by(
            '-start', 'number')[0].number
    else:
        last_number = 0
    for group in StudyGroup.objects.filter(status=StudyGroupStatus.Pending).order_by('start'):
        last_number += 1
        group.number = last_number
        group.save()


class Vizit(models.Model):

    class Meta:
        ordering = ['registration_date', 'id']

    group = models.ForeignKey('StudyGroup', verbose_name=u'Предмет')
    listener = models.ForeignKey('auth.Listener', verbose_name=u'Слушатель')
    registration_date = models.DateTimeField(verbose_name=u'Дата регистрации', auto_now_add=True)
    completed = models.BooleanField(verbose_name=u'Курс прослушан', default=False)
    attestation_work_name = models.CharField(verbose_name=u'Название курсовой работы', max_length=255,
        null=True, blank=True)


class Department(models.Model):
    name = models.CharField(verbose_name=u'Название', max_length=255)
    address = models.CharField(verbose_name=u'Адрес', max_length=255,
        null=True, blank=True)

    def get_absolute_url(self):
        return reverse('department:index', args=(self.pk,))

    def organizations(self):
        return Organization.objects.filter(listener__group__department=self).distinct()

    def listeners(self):
        return Listener.objects.filter(vizit__group__department=self).distinct()

    def __unicode__(self):
        return u'Филиал %s' % self.name

class Organization(models.Model):
    name = models.CharField(verbose_name=u'Название', max_length=255, unique=True)
    number = models.IntegerField(verbose_name=u'Номер', null=True, blank=True)
    address = models.CharField(verbose_name=u'Адрес', max_length=255,
        null=True, blank=True)
    cast = models.CharField(verbose_name=u'Тип организации', max_length=50,
        choices=enums.ORGANIZATION_TYPES, null=True, blank=True)

    def save(self, *args, **kwds):
        self.name = self.name.strip()
        return super(Organization, self).save(*args, **kwds)

    def __unicode__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(verbose_name=u'Название', max_length=255)
    short_name = models.CharField(verbose_name=u'Сокращенное наименование',
        max_length=255, blank=True, null=True)
    hours = models.CommaSeparatedIntegerField(verbose_name=u'Количество часов', max_length=64)

    def __unicode__(self):
        return self.short_name


class Certificate(models.Model):
    name = models.CharField(verbose_name=u'Название', max_length=255)
    cast = models.CharField(verbose_name=u'Тип документа', max_length=50,
        choices=enums.DOCUMENT_CAST, null=True, blank=True)
    group = models.ForeignKey('StudyGroup', verbose_name=u'Предмет')
    listener = models.ForeignKey('auth.Listener', verbose_name=u'Владелец')
    number = models.CharField(verbose_name=u'Номер', max_length=64, null=True, blank=True)

    def __unicode__(self):
        return self.name
