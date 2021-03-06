# -*- coding: utf-8 -*-
from difflib import get_close_matches
from core import enums
import re


def get_position_fuzzy(original):
    matches = get_close_matches(original, [item[1] for item in enums.LISTENER_POSITIONS])
    if matches:
        return matches[0]
    else:
        # хак, чтобы отловить учителей
        if re.match(u'учитель', original, flags=re.UNICODE|re.IGNORECASE):
            return u'учитель'
        else:
            return enums.LISTENER_POSITIONS[-1][1]

def get_profile_fuzzy(original):
    matches = get_close_matches(original, [item[1] for item in enums.LISTENER_PROFILES])
    if matches:
        return matches[0]
    else:
        return enums.LISTENER_PROFILES[-1][1]

def get_organization_type(original):
    for org_type in enums.ORGANIZATION_TYPES:
        if re.search('%s' % org_type[1], original):
            return org_type[1]


def get_category(organization_cast, position):
    default_category = u'Другие специалисты'
    if organization_cast in enums.POSITIONS_DICT:
        inverted = {}
        for key, values in enums.POSITIONS_DICT[organization_cast].iteritems():
            for value in values:
                inverted[value] = key

        if position in inverted:
            return inverted[position]
    return default_category


def firstcaps(s):
    """
    Returns string in lowercase with first letter capitalized
    """
    return s[0].upper() + s[1:].lower()


def get_hours_data():
    from core.models import Subject
    data = {}
    for subj in Subject.objects.all():
        data[subj.id] = subj.hours.split(',')
    data['default'] = [choice[0] for choice in enums.HOURS_CHOICES]
    return data


class ExtraContextMixin(object):

    def get_context_data(self, **kwargs):
        context = super(ExtraContextMixin, self).get_context_data(**kwargs)
        if hasattr(self, 'extra_context'):
            if callable(self.extra_context):
                context.update(self.extra_context())
            else:
                context.update(self.extra_context)

        return context
