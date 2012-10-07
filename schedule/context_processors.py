# -*- coding: utf-8 -*-
from django.utils import simplejson
import sys
from schedule import enums

class SettingsProcessor(object):
    def __getattr__(self, attr):
        if attr == '__file__':
            # autoreload support in dev server
            return __file__
        else:
            return lambda request: {attr: simplejson.dumps(getattr(enums, attr))}

sys.modules[__name__ + '.enums'] = SettingsProcessor()