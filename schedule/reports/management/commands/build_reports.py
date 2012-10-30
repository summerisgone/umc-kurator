# coding=utf-8
from datetime import datetime
from dialog import Dialog
from django.core.management.base import BaseCommand
from django.utils import simplejson
from auth.models import Listener
from reports.models import Report, ReportStatus
from reports.query import PARAMETERS, ResultTable


class Command(BaseCommand):
    help = "Process reports"

    def handle(self, *args, **options):
        dialog = Dialog()
        dialog.gauge_start()
        total = Report.objects.filter(status=ReportStatus.Pending).count()
        index = 0

        for report in Report.objects.filter(status=0):
            dialog.gauge_update(int(float(index)/total*100))

            report.status = ReportStatus.Working
            report.save()

            cols = PARAMETERS[report.vertical]()
            rows = PARAMETERS[report.horizontal]()
            # TODO: Ввести временной интервал
            rt = ResultTable(rows, cols, Listener.objects.all())
            rt.process()
            report.data = simplejson.dumps(rt.to_dict())
            report.status = ReportStatus.Ready
            report.template = 'reports/default.html'
            report.year = datetime.today().year
            report.save()
            # TOOD: try-except

            index += 1

        dialog.gauge_stop()