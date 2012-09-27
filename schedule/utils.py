# -*- coding: utf-8 -*-
from difflib import get_close_matches
from schedule import enums

def get_position_fuzzy(original):
    matches = get_close_matches(original, [item[1] for item in enums.LISTENER_POSITIONS])
    if matches:
        return matches[0]
    else:
        return enums.LISTENER_POSITIONS[-1][1]
