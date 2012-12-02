# coding=utf-8
from django.core.management.base import BaseCommand
from reports.models import Report, ReportStatus

class Command(BaseCommand):
    help = "Process pending reports"

    def handle(self, *args, **options):
        for report in Report.objects.filter(status=ReportStatus.Pending):
            report.process.delay()
