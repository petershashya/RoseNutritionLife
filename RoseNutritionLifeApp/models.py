from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

# Validator function for image and video file formats
# ---------------- Validators ----------------
def validate_image_file(value):
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    ext = value.name.split('.')[-1].lower()
    if f'.{ext}' not in allowed_extensions:
        raise ValidationError(f'Unsupported file extension. Allowed: {", ".join(allowed_extensions)}')

def validate_video_file(value):
    allowed_extensions = ['.mp4', '.mov', '.avi', '.mkv']
    ext = value.name.split('.')[-1].lower()
    if f'.{ext}' not in allowed_extensions:
        raise ValidationError(f'Unsupported file extension. Allowed: {", ".join(allowed_extensions)}')

class UserDetail(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    COMPANY_RANK_CHOICES = [
        ('director', 'Director'),
        ('vice_director', 'Vice Director'),
        ('business_teacher', 'Business Teacher'),
        ('manager', 'Manager'),
        ('doctor', 'Doctor'),
        ('it_officer', 'IT Officer'),
    	('secretary', 'Secretary'),
    	('stationary', 'Stationary'),
        ('reception', 'Reception'),
        ('accountant', 'Accountant'),
    	('pharmacist','Pharmacist' ),
        ('discipline','Discipline' ),
        ('advisor','Advisor' ),
    	('video_grapher', 'Video Grapher')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_detail')
    profile_image = models.ImageField(
        upload_to='userdetail/images/',
        blank=True,
        validators=[validate_image_file]
    )
    mobile_contact = models.CharField(max_length=15, unique=True)  # Not null
    #email = models.EmailField(blank=True, null=True)  #Nullable
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=False, null=False)#Not null
    age = models.PositiveIntegerField(blank=False, null=False) #Not Null
    region = models.CharField(max_length=100)  # Not null
    postal_address = models.CharField(max_length=255, blank=True, null=True)  # Nullable
    company_rank = models.CharField(max_length=50, choices=COMPANY_RANK_CHOICES, blank=True, null=True)
    membership_no = models.CharField(max_length=50, blank=False, null=False, unique=True)  # For SuperUser & Member

    def __str__(self):
        return f'{self.user.first_name} - {self.membership_no}'


class Viewer(models.Model):
    profile_image = models.ImageField(
        upload_to='viewerdetail/images/',
        blank=True,
        validators=[validate_image_file]
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='viewer_detail')
    full_name = models.CharField(max_length=255)
    mobile_contact = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True) #Nullable
    religion = models.CharField(max_length=100)
    postal_address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.full_name} - Viewer'


# ---------------- Disease Model ----------------
class Disease(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="diseases")
    disease_name = models.CharField(max_length=255)
    description = models.TextField()
    symptoms = models.TextField()
    causes = models.TextField()
    treatment = models.TextField()
    additional_comment = models.TextField(blank=True, null=True)

    # Image & Video fields (refactored like Song model)
    profile_image = models.ImageField(
        upload_to="disease/profile_images/",
        blank=True,
        null=True,
        validators=[validate_image_file]
    )
    image = models.ImageField(
        upload_to="disease/images/",
        blank=True,
        null=True,
        validators=[validate_image_file]
    )
    video = models.FileField(
        upload_to="disease/videos/",
        blank=True,
        null=True,
        validators=[validate_video_file]
    )

    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.disease_name

# ---------------- Medicine Model ----------------
class Medicine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="medicines")
    medicine_name = models.CharField(max_length=200)
    description = models.TextField()
    solution = models.TextField()
    additional_comment = models.TextField(blank=True, null=True)
    dose = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    profile_image = models.ImageField(
        upload_to="medicine/profile_images/",
        blank=True,
        null=True,
        validators=[validate_image_file]
    )
    image = models.ImageField(
        upload_to="medicine/images/",
        blank=True,
        null=True,
        validators=[validate_image_file]
    )
    video = models.FileField(
        upload_to="medicine/videos/",
        blank=True,
        null=True,
        validators=[validate_video_file]
    )

    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.medicine_name

# ---------------- CheckUp Model ----------------
class CheckUp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="checkups")
    checkup_name = models.CharField(max_length=200)
    description = models.TextField()
    treatment = models.TextField()
    solution = models.TextField()
    additional_comment = models.TextField(blank=True, null=True)
    dose = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)


    profile_image = models.ImageField(
        upload_to="checkup/profile_images/",
        blank=True,
        null=True,
        validators=[validate_image_file]
    )
    image = models.ImageField(
        upload_to="checkup/images/",
        blank=True,
        null=True,
        validators=[validate_image_file]
    )
    video = models.FileField(
        upload_to="checkup/videos/",
        blank=True,
        null=True,
        validators=[validate_video_file]
    )

    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.checkup_name

# ---------------- BusinessPlan Model ----------------
class BusinessPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="business_plans")
    description = models.TextField()
    sales_and_marketing = models.TextField()
    business_member = models.TextField()
    pv_points = models.TextField()
    additional_comment = models.TextField(blank=True, null=True)


    profile_image = models.ImageField(
        upload_to="businessplan/profile_images/",
        blank=True,
        null=True,
        validators=[validate_image_file]
    )
    image = models.ImageField(
        upload_to="businessplan/images/",
        blank=True,
        null=True,
        validators=[validate_image_file]
    )
    video = models.FileField(
        upload_to="businessplan/videos/",
        blank=True,
        null=True,
        validators=[validate_video_file]
    )

    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Business Plan - {self.user.username}"

# ---------------- BusinessLevel Model ----------------
class BusinessLevel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="business_levels")
    level_name = models.CharField(max_length=200)
    description = models.TextField()
    additional_comment = models.TextField(blank=True, null=True)


    profile_image = models.ImageField(
        upload_to="businesslevel/profile_images/",
        blank=True,
        null=True,
        validators=[validate_image_file]
    )
    image = models.ImageField(
        upload_to="businesslevel/images/",
        blank=True,
        null=True,
        validators=[validate_image_file]
    )
    video = models.FileField(
        upload_to="businesslevel/videos/",
        blank=True,
        null=True,
        validators=[validate_video_file]
    )

    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.level_name

# Patient Form Model ----------------
class PatientForm(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patients")
    full_name = models.CharField(max_length=255)
    age = models.PositiveIntegerField(blank=False, null=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    mobile_no = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    region = models.CharField(max_length=100)
    postal_address = models.CharField(max_length=255, blank=True, null=True)

    # CHARFIELD — NOT FK
    membership_no = models.CharField(max_length=50, blank=False, null=False)
    # NEW DATE FIELD
    birth = models.DateField(default="2000-01-01")

    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Patient: {self.full_name}"


# ---------------- Advertisement Model ----------------
class Advertisement(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="advertisements"
    )
    infoname = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to="advertisement/images/",
        blank=True,
        null=True,
        validators=[validate_image_file]
    )
    video = models.FileField(
        upload_to="advertisement/videos/",
        blank=True,
        null=True,
        validators=[validate_video_file]
    )
    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Advertisement - {self.infoname} ({self.user.username})"
    
    
    # ---------------- Shop Model ----------------
class Shop(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shops"
    )
    infoname = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to="shop/images/",
        blank=True,
        null=True,
        validators=[validate_image_file]
    )
    video = models.FileField(
        upload_to="shop/videos/",
        blank=True,
        null=True,
        validators=[validate_video_file]
    )
    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Shop - {self.infoname} ({self.user.username})"
    
    
# ---------------- Meeting Model ----------------
class Meeting(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="meetings"
    )
    infoname = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to="meeting/images/",
        blank=True,
        null=True,
        validators=[validate_image_file]
    )
    video = models.FileField(
        upload_to="meeting/videos/",
        blank=True,
        null=True,
        validators=[validate_video_file]
    )
    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Meeting - {self.infoname} ({self.user.username})"
    
    
# ---------------- Branch Model ----------------
class Branch(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="branchs"
    )
    infoname = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to="branch/images/",
        blank=True,
        null=True,
        validators=[validate_image_file]
    )
    video = models.FileField(
        upload_to="branch/videos/",
        blank=True,
        null=True,
        validators=[validate_video_file]
    )
    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Branch - {self.infoname} ({self.user.username})" 


# ---------------- CheckUp Sales Model ----------------
class CheckUp_SalesForm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="checkup_sales")
    checkup = models.ForeignKey(CheckUp, on_delete=models.CASCADE, related_name="sales")  # checkupId
    checkup_name = models.CharField(max_length=200)  # store checkup name
    checkup_type = models.CharField(max_length=255)
    checkup_cost = models.DecimalField(max_digits=10, decimal_places=2)

    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # auto-fill fields from CheckUp model
        if self.checkup:
            self.checkup_name = self.checkup.checkup_name
            self.checkup_type = self.checkup.dose  # using 'dose' as type
            self.checkup_cost = self.checkup.cost
        super().save(*args, **kwargs)

    def __str__(self):
        return f"CheckUp Sale: {self.checkup_name} - {self.checkup_cost}"

# ---------------- Medicine Sales Model ----------------
class Medicine_SalesForm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="medicine_sales")

    # New fields
    code = models.CharField(max_length=50, blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)

    # Fields stored directly from the form
    medicine_name = models.CharField(max_length=200)
    medicine_type = models.CharField(max_length=255)
    medicine_cost = models.DecimalField(max_digits=10, decimal_places=2)
    medicine_pv = models.PositiveIntegerField()

    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Nothing auto-fills because there is no FK to Medicine table
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Medicine Sale: {self.medicine_name} - {self.medicine_cost}"

class Medical(models.Model):
    ref_no = models.CharField(max_length=50)
    date = models.DateField(null=True, blank=True)
    office_name = models.CharField(max_length=255)
    id_number = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    sex = models.CharField(max_length=1)
    dob = models.CharField(max_length=50,null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    doctor_summary = models.TextField(blank=True)
    avoid_reduce = models.TextField(blank=True)
    eat_most = models.TextField(blank=True)
    doctor_signature = models.TextField(blank=True)
    charges = models.CharField(max_length=50, default='30,000/=')
    
    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Medical Form - {self.name} ({self.ref_no})"
    
    
class MedicalMessage(models.Model):
    medical = models.ForeignKey(Medical, on_delete=models.CASCADE, related_name="messages")
    message = models.TextField()

    expires_at = models.DateTimeField()  # 24 hours from creation
    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(auto_now=True)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"Message for {self.medical.name} ({self.medical.id_number})"

    
class MedicineProduct(models.Model):
    medical = models.ForeignKey("Medical", on_delete=models.CASCADE, related_name="medicine_products")

    # From Medical form
    membership_no = models.CharField(max_length=50, blank=True, null=True)
    patient_no = models.CharField(max_length=50, blank=True, null=True)

    # New fields
    code = models.CharField(max_length=50, blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    qty = models.PositiveIntegerField(null=True, blank=True)

    # From Medicine_SalesForm
    medicine = models.ForeignKey(Medicine_SalesForm, on_delete=models.CASCADE)
    medicine_name = models.CharField(max_length=200)
    medicine_pv = models.PositiveIntegerField()
    medicine_cost = models.DecimalField(max_digits=10, decimal_places=2)
    medicine_totalcost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    confirm_payment = models.BooleanField(default=False)

    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.medicine_name} ({self.medicine_pv} PV)"


class MemberPayment(models.Model):
    membership_no = models.CharField(max_length=50)
    member_name = models.CharField(max_length=255)
    total_pv = models.PositiveIntegerField()
    money = models.DecimalField(max_digits=12, decimal_places=2)
    month = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default="paid")

    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.member_name} ({self.membership_no}) - {self.money}"


class PaymentProduct(models.Model):
    payment = models.ForeignKey(
        MemberPayment,
        on_delete=models.CASCADE,
        related_name="payment_products"
    )

    # Product details
    medicine = models.ForeignKey(Medicine_SalesForm, on_delete=models.CASCADE)
    medicine_name = models.CharField(max_length=200)
    medicine_pv = models.PositiveIntegerField()
    medicine_cost = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.PositiveIntegerField(null=True, blank=True)

    # NEW FIELDS (allow null first)
    patient_name = models.CharField(max_length=255, null=True, blank=True)
    patient_id = models.CharField(max_length=50, null=True, blank=True)

    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.medicine_name} ({self.medicine_pv} PV)"



class Log(models.Model):
    user_id = models.IntegerField(null=True, blank=True)
    home_page_count = models.PositiveIntegerField(default=0)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Home: {self.home_page_count} - {self.user.username if self.user else 'Anonymous'}"


# Custom validators for image files
class About(models.Model):
    COMPANY_RANK_CHOICES = [
        ('director', 'Director'),
        ('vice_director', 'Vice Director'),
        ('business_teacher', 'Business Teacher'),
        ('manager', 'Manager'),
        ('doctor', 'Doctor'),
        ('it_officer', 'IT Officer'),
    	('secretary', 'Secretary'),
    	('stationary', 'Stationary'),
        ('reception', 'Reception'),
        ('accountant', 'Accountant'),
    	('pharmacist','Pharmacist' ),
        ('discipline','Discipline' ),
        ('advisor','Advisor' ),
    	('video_grapher', 'Video Grapher')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='about')  
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    image = models.ImageField(upload_to='about/images/', blank=True, null=False, validators=[validate_image_file])
    description = models.TextField(blank=True, null=True)
    mobileno = models.CharField(max_length=15, blank=True, null=True)
    company_rank = models.CharField(max_length=50, choices=COMPANY_RANK_CHOICES, blank=True, null=True)
    
    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.firstname} {self.lastname} - {self.company_rank}'
    
    
#for leave comments
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='comments')
    comment = models.TextField()
    confirmed = models.BooleanField(default=False, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment[:20]
    
    
#tables for storing comments
# Disease comment model
class DiseaseComment(models.Model):
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='disease_comments')
    comment = models.TextField()
    confirmed = models.BooleanField(default=False, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment[:20]
    

# Medicine comment model
class MedicineComment(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='medicine_comments')
    comment = models.TextField()
    confirmed = models.BooleanField(default=False, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment[:20]

# Checkup comment model
class CheckupComment(models.Model):
    checkup = models.ForeignKey(CheckUp, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='checkup_comments')
    comment = models.TextField()
    confirmed = models.BooleanField(default=False, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment[:20]

# Businessplan comment model
class BusinessplanComment(models.Model):
    businessplan = models.ForeignKey(BusinessPlan, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='businessplan_comments')
    comment = models.TextField()
    confirmed = models.BooleanField(default=False, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment[:20]

# Businesslevel comment model
class BusinesslevelComment(models.Model):
    businesslevel = models.ForeignKey(BusinessLevel, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='businesslevel_comments')
    comment = models.TextField()
    confirmed = models.BooleanField(default=False, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment[:20]
