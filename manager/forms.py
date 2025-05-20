from django import forms
from .models import System, Team,User,PlaySession

class TeamForm(forms.ModelForm):
    teamMembers = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        # widget=forms.CheckboxSelectMultiple,
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        # widget=forms.SelectMultiple(),
        label="Team Members"
    )
    class Meta:
        model = Team
        fields = ['teamMembers', 'systemType']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add ordering to make the user list more usable
        self.fields['teamMembers'].queryset = User.objects.all().order_by('uuid')
        
    def clean(self):
        cleaned_data = super().clean()
        # Add custom validation if needed
        if not cleaned_data.get('teamMembers'):
            raise forms.ValidationError("At least one team member must be selected")
        return cleaned_data

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name','phoneNumber'] 

class SystemForm(forms.ModelForm):
    class Meta:
        model = System
        fields = ['systemName']

class playSessionSearchForm(forms.ModelForm):
    uuid=forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        # widget=forms.CheckboxSelectMultiple,
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        # widget=forms.SelectMultiple(),
        to_field_name='uuid',  # Critical fix for the validation error< 
        label="Team Member"
    )
    class Meta:
        model = PlaySession
        fields = ['uuid']
