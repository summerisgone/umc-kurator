# -*- coding: utf-8 -*-
from django import forms
from south.migration.migrators import LoadInitialDataMigrator
from core.models import StudyGroup

class StudyGroupCreateForm(forms.ModelForm):

    auto_number = forms.BooleanField(label=u'Автоматически', initial=True, required=False)

    class Meta:
        model = StudyGroup
        fields = ('subject', 'department', 'start', 'end', 'hours', 'number')

    class Media:
        js = ('//ajax.googleapis.com/ajax/libs/jqueryui/1.8.23/jquery-ui.min.js',)

    def __init__(self, *args, **kwds):
        super(StudyGroupCreateForm, self).__init__(*args, **kwds)
        self.fields['start'].widget = forms.TextInput(attrs={'data-datepicker': 'datepicker'})
        self.fields['end'].widget = forms.TextInput(attrs={'data-datepicker': 'datepicker'})
        if self.instance.pk:
            del self.fields['auto_number']

    def save(self, **kwds):
        if 'auto_number' in self.cleaned_data and self.cleaned_data['auto_number']:
            del self.cleaned_data['number']

        self.instance.name = self.instance.__unicode__()
        super(StudyGroupCreateForm, self).save(**kwds)
