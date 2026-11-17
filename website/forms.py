from django import forms
from .models import ContactInquiry


class ContactForm(forms.ModelForm):
    """Contact/project inquiry form with styled widgets and honeypot spam protection."""
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'tabindex': '-1',
            'autocomplete': 'off',
            'aria-hidden': 'true',
            'class': 'hp-field',
        })
    )

    class Meta:
        model = ContactInquiry
        fields = [
            'name', 'email', 'phone', 'company',
            'service', 'budget_range', 'project_details'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your full name',
                'id': 'contact-name',
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'you@company.com',
                'id': 'contact-email',
                'autocomplete': 'email',
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': '+880 XXXX XXXXXX',
                'id': 'contact-phone',
                'autocomplete': 'tel',
            }),
            'company': forms.TextInput(attrs={
                'placeholder': 'Your company or business name',
                'id': 'contact-company',
                'autocomplete': 'organization',
            }),
            'service': forms.Select(attrs={
                'id': 'contact-service',
            }),
            'budget_range': forms.Select(attrs={
                'id': 'contact-budget',
            }),
            'project_details': forms.Textarea(attrs={
                'placeholder': 'Tell us about your project, goals, and any specific requirements...',
                'id': 'contact-details',
                'rows': 6,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add consistent CSS classes and accessibility attributes to fields
        for field_name, field in self.fields.items():
            if field_name == 'website':
                continue
            field.widget.attrs.setdefault('class', '')
            field.widget.attrs['class'] = (field.widget.attrs['class'] + ' form-control').strip()
            if field.required:
                field.widget.attrs['aria-required'] = 'true'

    def clean_phone(self):
        return self.cleaned_data.get('phone', '').strip()

    def clean_website(self):
        value = self.cleaned_data.get('website', '').strip()
        if value:
            raise forms.ValidationError('Invalid submission.')
        return value
