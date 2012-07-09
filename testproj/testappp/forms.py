__author__ = 'lex'
from django import forms
from testproj.testappp.models import BioModel


class EditUserForm(forms.ModelForm):
    class Meta:
        model = BioModel
