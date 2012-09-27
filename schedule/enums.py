# -*- coding: utf-8 -*-
from django.contrib.databrowse.datastructures import EasyChoice
from django.contrib.databrowse.views import choice_list

def make_choices(*choice_list):
    numbers = range(len(choice_list))
    return zip(numbers, choice_list)

ORGANIZATION_TYPES = make_choices(u'МОУ', u'МДОУ', u'МУДОД')
LISTENER_PROFILES = make_choices(
    u'Русский язык',
    u'Литература',
    u'Математика',
    u'Информатика',
    u'География',
    u'Физика',
    u'Химия',
    u'ИЗО',
    u'Технология',
    u'Физкультура',
    u'Начальные классы',
    u'Музыка',
    u'История',
    u'Обществознание',
    u'ОБЖ',
    u'Черчение',
    u'Астрономия',
    u'МХК',
    u'Иностранный язык',
    u'Другое',
)

LISTENER_CATEGORIES = make_choices(u'Руководящий работник', u'Педагогический работник', u'Другие специалисты')
LISTENER_POSITIONS = make_choices(
    u'директор',
    u'заместитель директора',
    u'заведующий СП (филиал)',

    u'учитель',
    u'школьный психолог',
    u'педагог-психолог',
    u'учитель-логопед',
    u'учитель-дефектолог',
    u'социальный педагог',
    u'педагог дополнительного образования',
    u'организатор ОБЖ',
    u'руководитель физического воспитания',

    u'воспитатель',
    u'старший воспитатель',
    u'педагог-психолог',
    u'учитель-логопед',
    u'учитель-дефектолог',
    u'социальный педагог',
    u'педагог дополнительного образования',
    u'музыкальный руководитель',
    u'инструктор по физической культуре',

    u'педагог дополнительного образования'
    u'педагог-психолог',
    u'социальный педагог',

    u'секретарь-документовед',
    u'библиотекарь',
    u'дежурный по режиму',
    u'другие должности, не относящиеся к педагогическим',

    u'помощник воспитателя',
    u'младший воспитатель',
    u'делопроизводитель',
    u'инструктор по гигиеническому воспитанию',
    u'другие должности, не относящиеся к педагогическим',

    u'секретарь',
    u'делопроизводитель',
    u'другие должности, не относящиеся к педагогическим'
)

POSITIONS_DICT = {
    u'МОУ': {
        u'Руководящий работник': (
            u'директор',
            u'заместитель директора',
            u'заведующий СП (филиал)',
        ),
        u'Педагогический работник': (
            u'учитель',
            u'школьный психолог',
            u'педагог-психолог',
            u'учитель-логопед',
            u'учитель-дефектолог',
            u'социальный педагог',
            u'педагог дополнительного образования',
            u'организатор ОБЖ',
            u'руководитель физического воспитания',
        ),
        u'Другие специалисты': (
            u'секретарь-документовед',
            u'библиотекарь',
            u'дежурный по режиму',
            u'другие должности, не относящиеся к педагогическим',
        )
    },
    u'МДОУ': {
        u'Руководящий работник': (
            u'директор',
            u'заместитель директора',
            u'заведующий СП (филиал)',
        ),
        u'Педагогический работник': (
            u'воспитатель',
            u'старший воспитатель',
            u'педагог-психолог',
            u'учитель-логопед',
            u'учитель-дефектолог',
            u'социальный педагог',
            u'педагог дополнительного образования',
            u'музыкальный руководитель',
            u'инструктор по физической культуре',
        ),
        u'Другие специалисты': (
            u'помощник воспитателя',
            u'младший воспитатель',
            u'делопроизводитель',
            u'инструктор по гигиеническому воспитанию',
            u'другие должности, не относящиеся к педагогическим',
        )
    },
    u'МУДОД': {
        u'Руководящий работник': (
            u'директор',
            u'заместитель директора',
            u'заведующий СП (филиал)',
        ),
        u'Педагогический работник': (
            u'педагог дополнительного образования'
            u'педагог-психолог',
            u'социальный педагог',
        ),
        u'Другие специалисты': (
            u'секретарь',
            u'делопроизводитель',
            u'другие должности, не относящиеся к педагогическим'
        )
    }

}

COURSE_DIRECTION = make_choices(
    u'ИКТ', u'ФГОС', u'Научно-инновационная деятельность',
    u'Метод. сопровождение', u'АС СГО', u'Интел', u'Менеджмент'
)
COURSE_CAST = make_choices(
    u'Курсы повышения квалификации',
    u'Учебные модульные семинары',
    u'Учебные тематические семинары,'
)

DOCUMENT_CAST = make_choices(u'удостоверение', u'сертификат', u'свидетельство')