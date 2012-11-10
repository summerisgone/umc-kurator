# coding=utf-8
import celery
from django.core.urlresolvers import reverse
from django.db import models
from core.auth.models import Listener
from reports.query import PARAMETERS, ResultTable
from django.utils import simplejson


class ReportStatus:
    Pending = 0
    Working = 1
    Ready = 2
    Error = -1

REPORT_STATUS = (
    (ReportStatus.Pending, "Pending"),
    (ReportStatus.Working, "Working"),
    (ReportStatus.Ready, "Ready"),
    (ReportStatus.Error, "Error"),
)


class Report(models.Model):
    template_name = models.CharField(max_length=64)
    data = models.TextField()  # JSON serialized data

    horizontal = models.CharField(max_length=64)
    vertical = models.CharField(max_length=64)

    year = models.IntegerField()
    time_range = models.CharField(max_length=64)

    status = models.IntegerField(choices=REPORT_STATUS)

    def get_absolute_url(self):
        return reverse('report_detail', args=[self.pk])

    @celery.task
    def process(self):
        self.status = ReportStatus.Working
        self.save()

        cols = PARAMETERS[self.vertical]()
        rows = PARAMETERS[self.horizontal]()
        # TODO: Ввести временной интервал
        rt = ResultTable(rows, cols, Listener.objects.all())
        rt.process()
        self.data = simplejson.dumps(rt.to_dict())
        self.status = ReportStatus.Ready
        self.save()
