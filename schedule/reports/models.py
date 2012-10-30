# coding=utf-8
from django.core.urlresolvers import reverse
from django.db import models


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