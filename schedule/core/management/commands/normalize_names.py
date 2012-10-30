# coding=utf-8
from django.core.management.base import BaseCommand
from auth.models import Listener
from pymorphy import get_morph
from django.conf import settings
from os.path import join
from dialog import Dialog


class Command(BaseCommand):
    help = "Normalizes names"

    def handle(self, *args, **options):
        morph = get_morph(join(settings.PROJECT_DIR, 'morph'))
        self.dialog = Dialog()
        listeners = Listener.objects.filter(first_name__exact=u'')

        total = listeners.count()
        index = 0
        self.dialog.gauge_start()

        for listener in listeners:
            listener.normalize_name(morph)
            text = u'%s %s %s' % (listener.last_name, listener.first_name, listener.patronymic)
            self.dialog.gauge_update(int(float(index)/total*100),
                text=text.encode('utf-8'),
                update_text=True)
            index += 1

        self.dialog.gauge_stop()
