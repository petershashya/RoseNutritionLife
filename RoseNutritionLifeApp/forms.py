from django import forms
from django.contrib.auth.models import User
from .models import (
    UserDetail, Viewer , Disease, Medicine, CheckUp, 
    BusinessPlan, BusinessLevel ,PatientForm, CheckUp_SalesForm, 
    Medicine_SalesForm, Advertisement
)

# Choice constants
GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female')
]

COMPANY_RANK_CHOICES = [
    ('director', 'Director'),
    ('vice_director', 'Vice Director'),
    ('business_teacher', 'Business Teacher'),
    ('manager', 'Manager'),
    ('doctor', 'Doctor'),
    ('it_officer', 'IT Officer'),
    ('supervisor', 'Supervisor'),
    ('reception', 'Reception'),
    ('accountant', 'Accountant'),
]

# SuperUser Registration Form
class SuperUserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    mobile_contact = forms.CharField(max_length=15, required=True, label='Mobile Number')
    email = forms.EmailField(required=False, label='Email Address')
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True)
    age = forms.IntegerField(required=True, min_value=1)
    region = forms.CharField(max_length=100, required=True)
    postal_address = forms.CharField(max_length=255, required=False)
    company_rank = forms.ChoiceField(choices=COMPANY_RANK_CHOICES, required=False)
    membership_no = forms.CharField(max_length=50, required=True, label="Membership No")
    profile_image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'accept': 'image/*'}))

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']

    def clean_mobile_contact(self):
        mobile_contact = self.cleaned_data.get('mobile_contact')
        if UserDetail.objects.filter(mobile_contact=mobile_contact).exists():
            raise forms.ValidationError("This mobile number is already registered.")
        return mobile_contact

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get("password"):
            user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            UserDetail.objects.create(
                user=user,
                profile_image=self.cleaned_data.get('profile_image'),
                mobile_contact=self.cleaned_data['mobile_contact'],
                email=self.cleaned_data.get('email'),
                gender=self.cleaned_data.get('gender'),
                age=self.cleaned_data.get('age'),
                region=self.cleaned_data['region'],
                postal_address=self.cleaned_data.get('postal_address'),
                company_rank=self.cleaned_data.get('company_rank'),
                membership_no=self.cleaned_data.get('membership_no'),
            )
        return user

# Member Registration Form (same as SuperUser but not staff)
class MemberRegistrationForm(SuperUserRegistrationForm):
    pass

# Viewer Registration Form
class ViewerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    mobile_contact = forms.CharField(max_length=15, required=True)
    email = forms.EmailField(required=False)
    full_name = forms.CharField(max_length=255, required=True)
    religion = forms.CharField(max_length=100, required=True)
    postal_address = forms.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ['username', 'password']

    def clean_mobile_contact(self):
        mobile_contact = self.cleaned_data.get('mobile_contact')
        if Viewer.objects.filter(mobile_contact=mobile_contact).exists():
            raise forms.ValidationError("This mobile number is already registered.")
        return mobile_contact

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get("password"):
            user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            Viewer.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                mobile_contact=self.cleaned_data['mobile_contact'],
                email=self.cleaned_data.get('email'),
                religion=self.cleaned_data['religion'],
                postal_address=self.cleaned_data.get('postal_address'),
            )
        return user
    

class DiseaseForm(forms.ModelForm):
    class Meta:
        model = Disease
        fields = [
            'disease_name',
            'description',
            'symptoms',
            'causes',
            'treatment',
            'additional_comment',
            'image',
            'video',
        ]
        widgets = {
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'video': forms.ClearableFileInput(attrs={'accept': 'video/*'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter description...'}),
            'symptoms': forms.Textarea(attrs={'rows': 3, 'placeholder': 'List symptoms...'}),
            'causes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Specify causes...'}),
            'treatment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Provide treatment information...'}),
            'additional_comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Additional comments...'}),
        }
        labels = {
            'disease_name': 'Disease Name',
            'description': 'Description',
            'symptoms': 'Symptoms',
            'causes': 'Causes',
            'treatment': 'Treatment',
            'additional_comment':'Additional Comment',
            'image': 'Disease Image',
            'video': 'Disease Video',
        }
        


# ---------------- Medicine Form ----------------
class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = [
            'medicine_name',
            'description',
            'solution',
            'additional_comment',
            'dose',
            'cost',
            'image',
            'video',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter description...'}),
            'solution': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter solution...'}),
            'additional_comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Additional comments...'}),
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'video': forms.ClearableFileInput(attrs={'accept': 'video/*'}),
        }
        labels = {
            'medicine_name': 'Medicine Name',
            'description': 'Description',
            'solution': 'Solution',
            'additional_comment': 'Additional Comment',
            'dose': 'Dose',
            'cost': 'Cost',
            'image': 'Medicine Image',
            'video': 'Medicine Video',
        }

# ---------------- CheckUp Form ----------------
class CheckUpForm(forms.ModelForm):
    class Meta:
        model = CheckUp
        fields = [
            'checkup_name',
            'description',
            'treatment',
            'solution',
            'additional_comment',
            'dose',
            'cost',
            'image',
            'video',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter description...'}),
            'treatment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Provide treatment details...'}),
            'solution': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter solution...'}),
            'additional_comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Additional comments...'}),
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'video': forms.ClearableFileInput(attrs={'accept': 'video/*'}),
        }
        labels = {
            'checkup_name': 'CheckUp Name',
            'description': 'Description',
            'treatment': 'Treatment',
            'solution': 'Solution',
            'additional_comment': 'Additional Comment',
            'dose': 'Dose',
            'cost': 'Cost',
            'image': 'CheckUp Image',
            'video': 'CheckUp Video',
        }

# ---------------- BusinessPlan Form ----------------
class BusinessPlanForm(forms.ModelForm):
    class Meta:
        model = BusinessPlan
        fields = [
            'description',
            'sales_and_marketing',
            'business_member',
            'pv_points',
            'additional_comment',
            'image',
            'video',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter business description...'}),
            'sales_and_marketing': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter sales and marketing strategies...'}),
            'business_member': forms.Textarea(attrs={'rows': 3, 'placeholder': 'How business members being profitable...'}),
            'pv_points': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Explain how can archive Pv Points...'}),
            'additional_comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Additional comments...'}),
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'video': forms.ClearableFileInput(attrs={'accept': 'video/*'}),
        }
        labels = {
            'description': 'Description',
            'sales_and_marketing': 'Sales & Marketing',
            'business_member': 'Business Members',
            'pv_points': 'PV Points',
            'additional_comment': 'Additional Comment',
            'image': 'BusinessPlan Image',
            'video': 'BusinessPlan Video',
        }

# ---------------- BusinessLevel Form ----------------
class BusinessLevelForm(forms.ModelForm):
    class Meta:
        model = BusinessLevel
        fields = [
            'level_name',
            'description',
            'additional_comment',
            'image',
            'video',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter description...'}),
            'additional_comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Additional comments...'}),
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'video': forms.ClearableFileInput(attrs={'accept': 'video/*'}),
        }
        labels = {
            'level_name': 'Level Name',
            'description': 'Description',
            'additional_comment': 'Additional Comment',
            'image': 'BusinessLevel Image',
            'video': 'BusinessLevel Video',
        }

# ---------------- Patient Form ----------------
class PatientModelForm(forms.ModelForm):
    class Meta:
        model = PatientForm
        fields = [
            'full_name',
            'age',
            'gender',
            'mobile_no',
            'email',
            'region',
            'postal_address',
            'membership_no',
        ]
        widgets = {
            'postal_address': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Enter postal address...'}),
        }
        labels = {
            'full_name': 'Full Name',
            'age': 'Age',
            'gender': 'Gender',
            'mobile_no': 'Mobile Number',
            'email': 'Email',
            'region': 'Region',
            'postal_address': 'Postal Address',
            'membership_no': 'Membership No.',
        }



# ---------------- Advertisement Form ----------------
class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = [
            'infoname',
            'description',
            'location',
            'image',
            'video',
        ]
        widgets = {
            'infoname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter advertisement title or info name...'
            }),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Enter advertisement description...'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter location...'
            }),
            'image': forms.ClearableFileInput(attrs={
                'accept': 'image/*'
            }),
            'video': forms.ClearableFileInput(attrs={
                'accept': 'video/*'
            }),
        }
        labels = {
            'infoname': 'Info Name',
            'description': 'Description',
            'location': 'Location',
            'image': 'Advertisement Image',
            'video': 'Advertisement Video',
        }
        

# ---------------- CheckUp Sales Form ----------------
class CheckUpSalesForm(forms.ModelForm):
    class Meta:
        model = CheckUp_SalesForm
        fields = [
            'checkup',       # select CheckUp
            'checkup_name',  # auto-filled, but we keep it in DB
            'checkup_type',  # auto-filled
            'checkup_cost',  # auto-filled
        ]
        widgets = {
            'checkup': forms.Select(attrs={'class': 'form-control'}),
            'checkup_name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'checkup_type': forms.TextInput(attrs={'readonly': 'readonly'}),
            'checkup_cost': forms.NumberInput(attrs={'readonly': 'readonly'}),
        }
        labels = {
            'checkup': 'Select CheckUp',
            'checkup_name': 'CheckUp Name',
            'checkup_type': 'CheckUp Type',
            'checkup_cost': 'CheckUp Cost',
        }

# ---------------- Medicine Sales Form ----------------
class MedicineSalesForm(forms.ModelForm):
    class Meta:
        model = Medicine_SalesForm
        fields = [
            'medicine',       # select Medicine
            'medicine_name',  # auto-filled
            'medicine_type',  # auto-filled
            'medicine_cost',  # auto-filled
            'medicine_pv',    # still entered by user
        ]
        widgets = {
            'medicine': forms.Select(attrs={'class': 'form-control'}),
            'medicine_name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'medicine_type': forms.TextInput(attrs={'readonly': 'readonly'}),
            'medicine_cost': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'medicine_pv': forms.NumberInput(attrs={'placeholder': 'Enter PV points'}),
        }
        labels = {
            'medicine': 'Select Medicine',
            'medicine_name': 'Medicine Name',
            'medicine_type': 'Medicine Type',
            'medicine_cost': 'Medicine Cost',
            'medicine_pv': 'Medicine PV Points',
        }