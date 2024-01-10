from django import forms
from .models import *

from django.urls import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class add_powerbi_setting_form(forms.Form):
    app_id_ = forms.CharField(max_length=200,label="App ID")
    tenant_id_ = forms.CharField(max_length=200,label="Tenant ID")   
    mail_address_ = forms.CharField(max_length=200, label="Mail Address")
    password_ = forms.CharField(widget=forms.PasswordInput(render_value = True), label="Password")

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit','Submit'))


"""
class add_powerbi_setting_form(forms.ModelForm):
    class Meta:
        model = PowerBI_Setting
        fields = '__all__'
        exclude = ['insertedDate']
"""