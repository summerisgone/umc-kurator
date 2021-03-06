# -*- coding: utf-8 -*-

def make_choices(*choice_list):
    numbers = range(len(choice_list))
    return zip(choice_list, choice_list)

# порядок важен, т.е. под ОУ попадают так же ДОУ
ORGANIZATION_TYPES = make_choices(u'ДОУ', u'ДОД', u'ОУ', u'УМЦ')
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

LISTENER_CATEGORIES = make_choices(u'Педагогический работник', u'Руководящий работник', u'Другие специалисты')
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
    u'музыкальный руководитель',
    u'инструктор по физической культуре',

    u'педагог дополнительного образования',

    u'секретарь-документовед',
    u'библиотекарь',
    u'дежурный по режиму',

    u'помощник воспитателя',
    u'младший воспитатель',
    u'делопроизводитель',
    u'инструктор по гигиеническому воспитанию',

    u'секретарь',
    u'другие должности',
)

POSITIONS_DICT = {
    u'ОУ': {
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
            u'другие должности',
        )
    },
    u'ДОУ': {
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
            u'другие должности',
        )
    },
    u'ДОД': {
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
            u'другие должности'
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


class StudyGroupStatus:
    Pending = 1
    Completing = 2
    Active = 3
    Certificating = 4
    Certificated = 5
    Closed = 6

STUDY_GROUP_STATUSES = (
    (StudyGroupStatus.Pending, u'Не укомплектована'),
    (StudyGroupStatus.Completing, u'Комплектуется'),
    (StudyGroupStatus.Active, u'Идут занятия'),
    (StudyGroupStatus.Certificating, u'Аттестуется'),
    (StudyGroupStatus.Certificated, u'Аттестована'),
    (StudyGroupStatus.Closed, u'Закрыта'),
)

HOURS_CHOICES = (
    (6, 6),
    (8, 8),
    (12, 12),
    (18, 18),
    (36, 36),
)



# Pernission settings
ADMINISTRATOR_PERMISSION = ('is_admin', u'Секретарь')
OPERATOR_PERMISSION = ('is_kurator', u'Куратор подразделения')

ADMINISTRATOR_GROUP_NAME = u'Секретари'
OPERATOR_GROUP_NAME= u'Кураторы подразделений'

# Для использования в команде updatepermissions
ALL_PERMISSIONS = [OPERATOR_PERMISSION, ADMINISTRATOR_PERMISSION]
GROUPS = (
    (ADMINISTRATOR_GROUP_NAME, (ADMINISTRATOR_PERMISSION[0],)),
    (OPERATOR_GROUP_NAME, (OPERATOR_PERMISSION[0],)),
)
