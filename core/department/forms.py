# -*- coding: utf-8 -*-
from django import forms
from core import enums
from core.auth.models import Listener
from core.models import Organization, Vizit, Certificate
import random


class ListenerAddForm(forms.Form):
    # User creation fields
    last_name = forms.CharField(label=u'Фамилия')
    first_name = forms.CharField(label=u'Имя')
    patronymic = forms.CharField(label=u'Отчество')

    last_name_inflated = forms.CharField(label=u'Фамилия')
    first_name_inflated = forms.CharField(label=u'Имя')
    patronymic_inflated = forms.CharField(label=u'Отчество')

    user_id = forms.IntegerField(widget=forms.HiddenInput, required=False)

    organization = forms.CharField(label=u'Организация', required=False)
    category = forms.ChoiceField(label=u'Категория слушателя', choices=enums.LISTENER_CATEGORIES,
        required=False)
    position = forms.ChoiceField(label=u'Должность', choices=enums.LISTENER_POSITIONS,
        required=False)
    profile = forms.ChoiceField(label=u'Профиль', choices=enums.LISTENER_PROFILES, required=False)

    def __init__(self, studygroup, *args, **kwds):
        self.studygroup = studygroup
        super(ListenerAddForm, self).__init__(*args, **kwds)

    def user_is_new(self):
        return 'user_id' not in self.data

    def clean(self):
        if self.studygroup.status != enums.StudyGroupStatus.Pending:
            raise forms.ValidationError(u'В эту группу уже нельзя добавлять слушателей')

        if ('user_id' in self.cleaned_data and
            self.cleaned_data['user_id'] and
            Listener.objects.get(id=self.cleaned_data['user_id']).exists()):
            return self.cleaned_data
        else:
            if all(map(lambda k: k in self.cleaned_data,
                ['organization', 'category', 'position', 'profile'])):
                return self.cleaned_data
            else:
                raise forms.ValidationError(u'Для нового пользователя все поля обязательны к '
                                            u'заполнению')

    def save(self):
        if 'user_id' in self.cleaned_data and self.cleaned_data['user_id']:
            listener = Listener.objects.get(id=self.cleaned_data['user_id'])
        else:
            listener = Listener(
                username='user-%6d' % random.randint(0, 999999),
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                patronymic=self.cleaned_data['patronymic'],

                first_name_inflated=self.cleaned_data['first_name_inflated'],
                last_name_inflated=self.cleaned_data['last_name_inflated'],
                patronymic_inflated=self.cleaned_data['patronymic_inflated'],

                category=self.cleaned_data['category'],
                position=self.cleaned_data['position'],
                profile=self.cleaned_data['profile'],
            )

            listener.organization = Organization.objects.get(
                name=self.cleaned_data['organization']
            )
            listener.save()

        Vizit.objects.create(group=self.studygroup, listener=listener)


class EmitCertificateForm(forms.models.ModelForm):
    class Meta:
        model = Certificate
        fields = ('name', 'cast')

    def __init__(self, studygroup, listener, *args, **kwds):
        super(EmitCertificateForm, self).__init__(*args, **kwds)
        self.instance.studygroup = studygroup
        self.instance.listener = listener


class BatchListenersForm(forms.Form):
    listeners = forms.ModelMultipleChoiceField(label="Слушатели",
        queryset=Listener.objects.all())
