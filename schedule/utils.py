# -*- coding: utf-8 -*-
from difflib import get_close_matches
from schedule import enums
import re

def get_position_fuzzy(original):
    matches = get_close_matches(original, [item[1] for item in enums.LISTENER_POSITIONS])
    if matches:
        return matches[0]
    else:
        return enums.LISTENER_POSITIONS[-1][1]

def get_organization_type(original):
    for org_type in enums.ORGANIZATION_TYPES:
        if re.search('%s' % org_type[1], original):
            return org_type[1]


def firstcaps(s):
    """
    Returns string in lowercase with first letter capitalized
    """
    return s[0].upper() + s[1:].lower()


class ExtraContextMixin(object):

    def get_context_data(self, **kwargs):
        context = super(ExtraContextMixin, self).get_context_data(**kwargs)
        if hasattr(self, 'extra_context'):
            if callable(self.extra_context):
                context.update(self.extra_context())
            else:
                context.update(self.extra_context)

        return context
