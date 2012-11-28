# coding=utf-8
from django.contrib.auth.models import User
from django.db import models
from core import enums
from utils import firstcaps


class ExtendedUser(User):
    class Meta:
        abstract = True

    patronymic = models.CharField(verbose_name=u'Отчество', max_length=255)
    phone = models.CharField(verbose_name=u'Телефон', max_length=50)

class Employee(ExtendedUser):
    department = models.ManyToManyField('core.Department', verbose_name=u'Подразделения')

    class Meta:
        verbose_name = u'Сотрудник'
        verbose_name_plural = u'Сотрудники'


class Listener(ExtendedUser):

    class Meta:
        verbose_name = u'Слушатель'
        verbose_name_plural = u'Слушатели'

    organization = models.ForeignKey('core.Organization', verbose_name=u'Организация')
    category = models.CharField(verbose_name=u'Категория', max_length=50, choices=enums.LISTENER_CATEGORIES)
    position = models.CharField(verbose_name=u'Должность', max_length=50, choices=enums.LISTENER_POSITIONS)
    profile = models.CharField(verbose_name=u'Специфика должности', max_length=50, choices=enums.LISTENER_PROFILES)

    first_name_inflated = models.CharField(verbose_name=u'Имя (дат. падеж)', max_length=50)
    last_name_inflated = models.CharField(verbose_name=u'Фамилия (дат. падеж)', max_length=50)
    patronymic_inflated = models.CharField(verbose_name=u'Отчество (дат. падеж)', max_length=50)

    def normalize_name(self, morph, save=True):
        from pymorphy.contrib import lastnames_ru
        # имя
        if not self.first_name:
            first_name = morph.normalize(self.first_name_inflated.upper()).pop()
            self.first_name = firstcaps(first_name)

        sex = morph.get_graminfo(self.first_name_inflated.upper())[0]['info'].split(',', 1)[0]
        # отчество
        if not self.patronymic:
            patronymic = morph.inflect_ru(self.patronymic_inflated.upper(), u'им')
            self.patronymic = firstcaps(patronymic)

        # фамилия
        if not self.last_name:
            last_name = lastnames_ru.normalize(morph, self.last_name_inflated.upper(), sex)
            self.last_name = firstcaps(last_name)

        if save:
            self.save()

    def fio(self):
        return u'%s %s %s' % (self.last_name, self.first_name, self.patronymic)

    def fio_inflated(self):
        return u'%s %s %s' % (self.last_name_inflated, self.first_name_inflated, self.patronymic_inflated)

    def apply_studygroup(self, group):
        if self.vizit_set.filter(group=group).exists():
            return None
        else:
            return self.vizit_set.create(group=group)

    def attest(self, group, attestation_work_name):
        return self.vizit_set.filter(group=group).update(attestation_work_name=attestation_work_name)

    def complete_course(self, group):
        return self.vizit_set.filter(group=group).update(completed=True)

    def issue_certificate(self, group, cert_number):
        return self.certificate_set.create(**{
            'cert_number': cert_number,
            'group': group,
        })


    def __unicode__(self):
        return self.fio()
