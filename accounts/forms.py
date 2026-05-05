from django import forms
from django.contrib.auth.models import User
from .models import Report, Profile

glass_attrs = {
    'class': 'form-control bg-white bg-opacity-25 text-white border-0 rounded-4 px-3 py-2',
    'style': 'color: white !important;'
}

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ReportForm(forms.ModelForm):
    extra_media = forms.FileField(
        required=False,
        label="Add Photos or Videos"
    )

    class Meta:
        model = Report
        fields = ['title', 'description'] 
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control bg-white bg-opacity-25 text-white border-0 rounded-4 px-3 py-2',
                'placeholder': 'Enter log title',
                'style': 'color: white !important;'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control bg-white bg-opacity-25 text-white border-0 rounded-4 px-3 py-2',
                'rows': 4,
                'style': 'color: white !important;'
            }),   }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['extra_media'].widget.attrs.update({
            'multiple': True,
            'class': 'form-control bg-white bg-opacity-25 text-white border-0 rounded-4 px-3 py-2',
            'style': 'color: white !important;'  })

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control glass-input'}), 
            'email': forms.EmailInput(attrs={'class': 'form-control glass-input'}), 
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'dob', 'sex', 'civil_status', 'phone_number', 'address']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control glass-input'}),
            'dob': forms.DateInput(attrs={'class': 'form-control glass-input', 'type': 'date'}),
            'sex': forms.Select(attrs={'class': 'form-select glass-input'}),
            'civil_status': forms.Select(attrs={'class': 'form-select glass-input'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': '+63...'}),
            'address': forms.Textarea(attrs={'class': 'form-control glass-input', 'rows': 3, 'placeholder': 'Enter your full address...'}),
        }