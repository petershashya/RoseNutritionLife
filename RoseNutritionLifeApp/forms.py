from django import forms
from django.contrib.auth.models import User
from .models import (
    UserDetail, Viewer , Disease, Medicine, CheckUp, 
    BusinessPlan, BusinessLevel ,PatientForm, CheckUp_SalesForm, 
    Medicine_SalesForm, Advertisement,Shop,Meeting,Branch,About,
    DiseaseComment,MedicineComment,CheckupComment,BusinessplanComment,
    BusinesslevelComment ,Comment,Medical,MemberPayment
)

# Choice constants
GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female')
]

COMPANY_RANK_CHOICES = [
    ('', ''),
    ('director', 'Director'),
    ('vice_director', 'Vice Director'),
    ('business_teacher', 'Business Teacher'),
    ('manager', 'Manager'),
    ('doctor', 'Doctor'),
    ('it_officer', 'IT Officer'),
    ('secretary', 'Secretary'),
    ('stationary', 'Stationary'),
    ('reception', 'Reception'),
    #('accountant', 'Accountant'),
    ('pharmacist','Pharmacist' ),
    ('displine','Displine' ),
    ('advisor','Advisor' ),
    ('video_grapher', 'Video Grapher')
]

COMPANY_RANK_MEMBERCHOICES = [
    ('', ''),
]

class SuperUserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    mobile_contact = forms.CharField(max_length=15, required=True, label='Mobile Number')
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True)
    age = forms.IntegerField(required=True, min_value=1)
    region = forms.CharField(max_length=100, required=True)
    postal_address = forms.CharField(max_length=255, required=False)
    company_rank = forms.ChoiceField(choices=COMPANY_RANK_CHOICES, required=False)
    membership_no = forms.CharField(max_length=50, required=True, label="Membership No")
    profile_image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'accept': 'image/*'}))

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        self.instance_user = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)

    def clean_mobile_contact(self):
        mobile_contact = self.cleaned_data.get('mobile_contact')
        qs = UserDetail.objects.filter(mobile_contact=mobile_contact)
        if self.instance_user:
            qs = qs.exclude(user=self.instance_user)
        if qs.exists():
            raise forms.ValidationError("This mobile number is already registered.")
        return mobile_contact

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
            UserDetail.objects.update_or_create(
                user=user,
                defaults={
                    'profile_image': self.cleaned_data.get('profile_image'),
                    'mobile_contact': self.cleaned_data['mobile_contact'],
                    'gender': self.cleaned_data.get('gender'),
                    'age': self.cleaned_data.get('age'),
                    'region': self.cleaned_data['region'],
                    'postal_address': self.cleaned_data.get('postal_address'),
                    'company_rank': self.cleaned_data.get('company_rank'),
                    'membership_no': self.cleaned_data.get('membership_no'),
                }
            )
        return user


# Member Registration Form (same as SuperUser but not staff)
# class MemberRegistrationForm(SuperUserRegistrationForm):
#     pass

class MemberRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    mobile_contact = forms.CharField(max_length=15, required=True, label='Mobile Number')
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True)
    age = forms.IntegerField(required=True, min_value=1)
    region = forms.CharField(max_length=100, required=True)
    postal_address = forms.CharField(max_length=255, required=False)
    company_rank = forms.ChoiceField(choices=COMPANY_RANK_MEMBERCHOICES, required=False)
    membership_no = forms.CharField(max_length=7, required=True, label="Membership No")
    profile_image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'accept': 'image/*'}))

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        self.instance_user = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)

    def clean_mobile_contact(self):
        mobile_contact = self.cleaned_data.get('mobile_contact')
        qs = UserDetail.objects.filter(mobile_contact=mobile_contact)
        if self.instance_user:
            qs = qs.exclude(user=self.instance_user)
        if qs.exists():
            raise forms.ValidationError("This mobile number is already registered.")
        return mobile_contact

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
            UserDetail.objects.update_or_create(
                user=user,
                defaults={
                    'profile_image': self.cleaned_data.get('profile_image'),
                    'mobile_contact': self.cleaned_data['mobile_contact'],
                    'gender': self.cleaned_data.get('gender'),
                    'age': self.cleaned_data.get('age'),
                    'region': self.cleaned_data['region'],
                    'postal_address': self.cleaned_data.get('postal_address'),
                    'company_rank': self.cleaned_data.get('company_rank'),
                    'membership_no': self.cleaned_data.get('membership_no'),
                }
            )
        return user


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
            'profile_image',
            'image',
            'video',
        ]
        widgets = {
            'profile_image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
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
            'profile_image': 'Disease Profile Image',
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
            'profile_image',
            'image',
            'video',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter description...'}),
            'solution': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter solution...'}),
            'additional_comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Additional comments...'}),
            'profile_image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
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
            'profile_image': 'Medicine Profile Image',
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
            'profile_image',
            'image',
            'video',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter description...'}),
            'treatment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Provide treatment details...'}),
            'solution': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter solution...'}),
            'additional_comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Additional comments...'}),
            'profile_image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
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
            'profile_image': 'CheckUp Profile Image',
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
            'profile_image',
            'image',
            'video',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter business description...'}),
            'sales_and_marketing': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter sales and marketing strategies...'}),
            'business_member': forms.Textarea(attrs={'rows': 3, 'placeholder': 'How business members being profitable...'}),
            'pv_points': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Explain how can archive Pv Points...'}),
            'additional_comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Additional comments...'}),
            'profile_image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'video': forms.ClearableFileInput(attrs={'accept': 'video/*'}),
        }
        labels = {
            'description': 'Description',
            'sales_and_marketing': 'Sales & Marketing',
            'business_member': 'Business Members',
            'pv_points': 'PV Points',
            'additional_comment': 'Additional Comment',
            'profile_image': 'BusinessPlan Profile Image',
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
            'profile_image',
            'image',
            'video',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter description...'}),
            'additional_comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Additional comments...'}),
            'profile_image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'video': forms.ClearableFileInput(attrs={'accept': 'video/*'}),
        }
        labels = {
            'level_name': 'Level Name',
            'description': 'Description',
            'additional_comment': 'Additional Comment',
            'profile_image': 'BusinessLevel Profile Image',
            'image': 'BusinessLevel Image',
            'video': 'BusinessLevel Video',
        }

# ---------------- Patient Form ----------------
class PatientModelForm(forms.ModelForm):
    membership_no = forms.ChoiceField(
        choices=[],
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Membership No."
    )

    birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label="Birth"
    )

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
            'birth',  # added date here
        ]
        widgets = {
            'postal_address': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # First empty placeholder option
        choices = [("", "-- Chagua No ya Mwanachama --")]

        # Populate membership_no options from UserDetail
        for u in UserDetail.objects.all():
            label = f"{u.user.first_name} - {u.membership_no}"
            choices.append((u.membership_no, label))

        self.fields['membership_no'].choices = choices
        
        

class MedicalForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(
        queryset=Medicine_SalesForm.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select w-100',
            'size': '8'
        }),
        required=False
    )

    class Meta:
        model = Medical
        fields = [
            'ref_no', 'date', 'office_name', 'id_number', 'name', 'sex', 'dob',
            'weight', 'height', 'doctor_summary', 'avoid_reduce', 'eat_most',
            'products', 'doctor_signature', 'charges'
        ]

        widgets = {
            'ref_no': forms.TextInput(attrs={'class': 'line-input', 'readonly': True}),
            'office_name': forms.TextInput(attrs={'class': 'line-input'}),
            'id_number': forms.TextInput(attrs={'class': 'line-input', 'readonly': True}),
            'name': forms.TextInput(attrs={'class': 'line-input', 'readonly': True}),
            'sex': forms.TextInput(attrs={'class': 'line-input', 'readonly': True}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'line-input'}),
            'dob': forms.TextInput(attrs={'class': 'line-input', 'readonly': True}),
            'weight': forms.NumberInput(attrs={'class': 'line-input'}),
            'height': forms.NumberInput(attrs={'class': 'line-input'}),
            'doctor_summary': forms.Textarea(attrs={'class': 'line-textarea'}),
            'avoid_reduce': forms.Textarea(attrs={'class': 'summary-textarea'}),
            'eat_most': forms.Textarea(attrs={'class': 'summary-textarea'}),
            'doctor_signature': forms.TextInput(attrs={'class': 'line-input'}),
            'charges': forms.TextInput(attrs={'class': 'line-input'}),
        }

class MemberPaymentForm(forms.ModelForm):
    
    class Meta:
        model = MemberPayment
        fields = [
            "membership_no",
            "member_name",
            "total_pv",
            "money",
            "month",
            "status",
        ]

        widgets = {
            "membership_no": forms.TextInput(attrs={"class": "form-control"}),
            "member_name": forms.TextInput(attrs={"class": "form-control"}),
            "total_pv": forms.NumberInput(attrs={"class": "form-control"}),
            "money": forms.NumberInput(attrs={"class": "form-control"}),
            "month": forms.TextInput(attrs={"class": "form-control", "placeholder": "December 2025"}),
            "status": forms.TextInput(attrs={"class": "form-control"}),
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
        
        


# ---------------- Shop Form ----------------
class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
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
                'placeholder': 'Enter shop title or info name...'
            }),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Enter shop description...'
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
            'image': 'Shop Image',
            'video': 'Shop Video',
        }
        
        

# ---------------- Meeting Form ----------------
class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
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
                'placeholder': 'Enter Meeting title or info name...'
            }),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Enter Meeting description...'
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
            'image': 'Meeting Image',
            'video': 'Meeting Video',
        }
        
        
        

# ---------------- Branch Form ----------------
class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
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
                'placeholder': 'Enter branch title or info name...'
            }),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Enter branch description...'
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
            'image': 'Branch Image',
            'video': 'Branch Video',
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
            'medicine_name',
            'code',
            'unit',
            'medicine_type',
            'medicine_cost',
            'medicine_pv',
        ]

        widgets = {
            'medicine_name': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'unit': forms.Select(attrs={
                'class': 'form-control'
            }),
            'medicine_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'medicine_cost': forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }),
            'medicine_pv': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter PV points'
            }),
        }

        labels = {
            'medicine_name': 'Medicine Name',
            'code': 'Medicine Code',
            'unit': 'Medicine Unit',
            'medicine_type': 'Medicine Type',
            'medicine_cost': 'Medicine Cost',
            'medicine_pv': 'Medicine PV Points',
        }

        
# class AboutForm(forms.ModelForm):
#     class Meta:
#         model = About
#         fields = ['firstname', 'lastname', 'image', 'description', 'mobileno', 'company_rank']
#         widgets = {
#             'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
#             # 'rank': forms.Select(choices=About.RANK_CHOICES),
#         }
#         labels = {
#             'firstname': 'First Name',
#             'lastname': 'Last Name',
#             'image': 'Profile Image',
#             'description': 'Description',
#             'mobileno': 'Mobile Number',
#             'company_rank': 'Rank',
#         }
        
        
class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = ['firstname', 'lastname', 'image', 'description', 'mobileno', 'company_rank']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'company_rank': forms.Select(attrs={'class': 'form-select border border-info'}),
        }
        labels = {
            'firstname': 'First Name',
            'lastname': 'Last Name',
            'image': 'Profile Image',
            'description': 'Description',
            'mobileno': 'Mobile Number',
            'company_rank': 'Company Rank',
        }

    def __init__(self, *args, **kwargs):
        self.instance_about = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)

    def clean_mobileno(self):
        mobileno = self.cleaned_data.get('mobileno')
        qs = About.objects.filter(mobileno=mobileno)
        if self.instance_about:
            qs = qs.exclude(pk=self.instance_about.pk)
        if qs.exists():
            raise forms.ValidationError("This mobile number is already registered in About.")
        return mobileno


#for leave comments
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        
#start comments section forms
class DiseaseCommentForm(forms.ModelForm):
    class Meta:
        model = DiseaseComment
        fields = ['comment']

class MedicineCommentForm(forms.ModelForm):
    class Meta:
        model = MedicineComment
        fields = ['comment']
    
class CheckupCommentForm(forms.ModelForm):
    class Meta:
        model = CheckupComment
        fields = ['comment']

class BusinessplanCommentForm(forms.ModelForm):
    class Meta:
        model = BusinessplanComment
        fields = ['comment']
        
class BusinesslevelCommentForm(forms.ModelForm):
    class Meta:
        model = BusinesslevelComment
        fields = ['comment']
        


#userdetail form
# USEREDIT_COMPANY_RANK_CHOICES = [
#     ('', ''),
#     ('director', 'Director'),
#     ('vice_director', 'Vice Director'),
#     ('business_teacher', 'Business Teacher'),
#     ('manager', 'Manager'),
#     ('doctor', 'Doctor'),
#     ('it_officer', 'IT Officer'),
#     ('supervisor', 'Supervisor'),
#     ('reception', 'Reception'),
#     ('accountant', 'Accountant'),
# ]
class UserDetailForm(forms.ModelForm):

    class Meta:
        model = UserDetail
        fields = ['profile_image', 'mobile_contact', 'gender','age','region','postal_address','company_rank','membership_no']
        widgets = {
            'profile_image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            # 'company_rank' : forms.ChoiceField(choices= USEREDIT_COMPANY_RANK_CHOICES, required=False),
        }
        labels = {
            'mobile_contact': 'Mobile Contact',
            'gender' : 'gender' ,
            'age' : 'age',
            'region' : 'region',
            'postal_address' : 'postal address',
            'company_rank' : 'company rank' ,
            'membership_no' : 'memmbership No',
        }

#start solve forget passowrds and reset strong passwords
class ForgotPasswordForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    mobile_contact = forms.CharField(max_length=15)
    membership_no = forms.CharField(max_length=8)
    
    fields = ['first_name', 'last_name','mobile_contact', 'membership_no']
    
    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        mobile_contact = cleaned_data.get('mobile_contact')
        membership_no = cleaned_data.get('membership_no')

        # Check if User exists with the provided first_name, last_name, and email
        try:
            user = User.objects.get(first_name=first_name, last_name=last_name)
        except User.DoesNotExist:
            raise forms.ValidationError("No matching user found with the provided details.")
        
        # Check if UserDetail exists with the provided mobile_contact and matches the user
        try:
            user_detail = UserDetail.objects.get(user=user, mobile_contact=mobile_contact, membership_no=membership_no)
        except UserDetail.DoesNotExist:
            raise forms.ValidationError("No matching details from provided mobile contact or membership No .")
        
        self.cleaned_data['user'] = user
        return self.cleaned_data

class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    fields = ['new_password', 'confirm_password']
    labels = {
            'new_password': 'New Password',
            'confirm_password': 'Confirm Password',
            }
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data
