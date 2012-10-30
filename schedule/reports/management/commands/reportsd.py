# coding=utf-8
from django.core.management.base import BaseCommand
from reports.models import Report, ReportStatus
from django.conf import settings
from os.path import join

PIDFILE = join(settings.PROJECT_DIR, 'run', 'reportsd.pid')


class Command(BaseCommand):
    help = "Process reports daemon"


    def handle(self, *args, **options):
        for report in Report.objects.filter(status=ReportStatus.Pending):
            report.process()