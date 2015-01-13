from django import forms

from test_secretary.models import TestCaseRun, STATUS


class TestCaseRunForm(forms.ModelForm):
    class Meta:
        model = TestCaseRun
        fields = ['status', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control form-element',
                                             'placeholder': 'Optional comment'}),
            'status': forms.Select(attrs={'class': 'form-control form-element'},
                                   choices=STATUS),
        }
