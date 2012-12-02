# coding=utf-8
import celery
from django.core.urlresolvers import reverse
from django.db import models
from core.auth.models import Listener
from core.models import Vizit
from reports.query import PARAMETERS, ResultTable
from django.utils import simplejson


class ReportStatus:
    Pending = 0
    Working = 1
    Ready = 2
    Error = -1

REPORT_STATUS = (
    (ReportStatus.Pending, u'В очереди'),
    (ReportStatus.Working, u'Обрабатывается'),
    (ReportStatus.Ready, u'Готов'),
    (ReportStatus.Error, u'Ошибка'),
)


class Report(models.Model):
    template_name = models.CharField(max_length=64)
    data = models.TextField()  # JSON serialized data

    horizontal = models.CharField(max_length=64)
    vertical = models.CharField(max_length=64)
    grouping = models.CharField(max_length=64)
    # Для дополнительных опций, по умолчанию не исопльзуются
    filter_name = models.CharField(max_length=64)
    filter_value = models.CharField(max_length=64)

    status = models.IntegerField(choices=REPORT_STATUS)

    def get_absolute_url(self):
        return reverse('report_detail', args=[self.pk])

#    @celery.task
    def process(self):
        try:
            self.status = ReportStatus.Working
            self.save()

            cols = PARAMETERS[self.vertical]()
            rows = PARAMETERS[self.horizontal]()
            grouping = PARAMETERS[self.grouping]()

            qs = Vizit.objects.all()
            if self.filter_name and self.filter_value:
                qs = qs.filter(**{self.filter_name: self.filter_value})

            rt = ResultTable(rows, cols, grouping, qs)
            rt.process()
            self.data = simplejson.dumps(rt.to_dict())
            self.status = ReportStatus.Ready
            self.save()
        except Exception, e:
            self.status = ReportStatus.Error
            self.save()
            raise
