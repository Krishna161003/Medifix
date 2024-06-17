from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import profile, camp_details, camp_services, doctor, appointment
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter First name'}), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter last name'}), required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Enter Email address'}), required=True)
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter username'}), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Enter Password','aria-describedby':"password1-visible"}), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'ReEnter Password','aria-describedby':"reenter-password-visible"}), required=True)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

    ### This is used to check if the registering email is exists in the database or not.
    def clean_email(self):
        email = self.cleaned_data.get("email")
        user_count = User.objects.filter(email=email).count()
        if user_count > 0:
            raise forms.ValidationError("This email is already exists.")
        return email
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = profile
        fields = ['phone_number', 'date_of_birth', 'camp_register', 'submitted_application','about']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'camp_register': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'submitted_application': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'aria-describedby': 'abouthelp'}),
        }

class CampDetailsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(CampDetailsForm, self).__init__(*args, **kwargs)
        
        # Iterate through all fields
        for field_name, field in self.fields.items():
            # Add 'form-control' class to each field widget
            field.widget.attrs['class'] = 'form-control'

        boolean_fields = ['camp_register_active', 'registration']
        for field_name in boolean_fields:
            self.fields[field_name].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})
        
        # Set custom widget for start_date_time field
        self.fields['start_date_time'].widget = forms.DateTimeInput(attrs={'class': 'form-control','type': 'datetime-local'})
        self.fields['end_date_time'].widget = forms.DateTimeInput(attrs={'class': 'form-control','type': 'datetime-local'})
        
    class Meta:
        model = camp_details
        fields = ('camp_name', 'location', 'latitude', 'longitude', 'start_date_time', 'end_date_time', 'contact_website', 'hospital_name', 'club_name', 'other', 'description', 'type_of_camp', 'total_camp_registrations', 'cost', 'camp_register_active', 'registration')
        exclude = ['createdby']

class DoctorForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(DoctorForm, self).__init__(*args, **kwargs)
        # Filter camp_name choices based on the logged-in user
        self.fields['camp_name'].queryset = camp_details.objects.filter(createdby=user)

        for field_name, field in self.fields.items():
            # Add 'form-control' class to each field
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = doctor
        fields = ['camp_name', 'doctor_name', 'doctor_title', 'doctor_description']

class CampServiceForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(CampServiceForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            # Add 'form-control' class to each field
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = camp_services
        fields = ['camp_name', 'service_name']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = appointment
        fields = ['appointment_date']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        }

