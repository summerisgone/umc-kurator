# -*- coding: utf-8 -*-
from django import forms
from core.models import StudyGroup

class StudyGroupCreateForm(forms.ModelForm):
    class Meta:
        model = StudyGroup
        fields = ('subject', 'department', 'start', 'end', 'hours')

    class Media:
        js = ('//ajax.googleapis.com/ajax/libs/jqueryui/1.8.23/jquery-ui.min.js',)

    def __init__(self, *args, **kwds):
        super(StudyGroupCreateForm, self).__init__(*args, **kwds)
        self.fields['start'].widget = forms.TextInput(attrs={'data-datepicker': 'datepicker'})
        self.fields['end'].widget = forms.TextInput(attrs={'data-datepicker': 'datepicker'})

    def save(self, **kwds):
        self.instance.name = self.instance.__unicode__()
        super(StudyGroupCreateForm, self).save(**kwds)