from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .models import (
    UserDetail,Disease ,Medicine, CheckUp, BusinessPlan, 
    BusinessLevel,Medicine_SalesForm, CheckUp_SalesForm,PatientForm ,Advertisement
)
from .forms import (
    MedicineForm, CheckUpForm, BusinessPlanForm, BusinessLevelForm,
    SuperUserRegistrationForm, MemberRegistrationForm, ViewerRegistrationForm ,
    DiseaseForm, MedicineForm, CheckUpForm, BusinessPlanForm, BusinessLevelForm, 
    CheckUpSalesForm, MedicineSalesForm ,PatientModelForm, 
    CheckUpSalesForm, MedicineSalesForm,AdvertisementForm
)

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
import pytz
from django.core.paginator import Paginator
from django.utils.timesince import timesince
from django.shortcuts import render


def home(request):
    # Get the first posted (earliest) item for each table
    first_disease = Disease.objects.order_by("date_created").first()
    first_medicine = Medicine.objects.order_by("date_created").first()
    first_checkup = CheckUp.objects.order_by("date_created").first()
    first_business_plan = BusinessPlan.objects.order_by("date_created").first()
    first_business_level = BusinessLevel.objects.order_by("date_created").first()

    context = {
        "disease": first_disease,
        "medicine": first_medicine,
        "checkup": first_checkup,
        "business_plan": first_business_plan,
        "business_level": first_business_level,
    }
    return render(request, "index.html", context)




def paginate_and_prepare(request, queryset, page_param):
    """
    Reusable pagination + truncate description to 25 chars
    """
    paginator = Paginator(queryset.order_by("date_created"), 10)
    page_number = request.GET.get(page_param)
    page_obj = paginator.get_page(page_number)

    for obj in page_obj:
        # Add time since posted
        if hasattr(obj, "date_created"):
            obj.time_since_posted = timesince(obj.date_created)

        # Truncate description field if exists
        if hasattr(obj, "description") and obj.description:
            if len(obj.description) > 25:
                obj.short_description = obj.description[:25] + "..."
            else:
                obj.short_description = obj.description
        else:
            obj.short_description = ""

    return page_obj

def services(request):
    context = {
        "disease_page_obj": paginate_and_prepare(request, Disease.objects.all(), "disease_page"),
        "medicine_page_obj": paginate_and_prepare(request, Medicine.objects.all(), "medicine_page"),
        "checkup_page_obj": paginate_and_prepare(request, CheckUp.objects.all(), "checkup_page"),
        "bp_page_obj": paginate_and_prepare(request, BusinessPlan.objects.all(), "bp_page"),
        "bl_page_obj": paginate_and_prepare(request, BusinessLevel.objects.all(), "bl_page"),
    }
    return render(request, "service.html", context)


def advertisment(request):
    return render(request, 'advertisement.html')



# Utility to check user rank
def get_user_rank(user):
    try:
        return user.userdetails.company_rank  # assuming OneToOne relation with User
    except UserDetail.DoesNotExist:
        return None

# ----------------- POST VIEWS WITH PERMISSIONS -----------------

@login_required
def post_disease(request):
    # Only Manager or Doctor can post
    user_rank = getattr(request.user.user_detail, 'company_rank', '').lower()
    if user_rank not in ['manager', 'doctor']:
        messages.error(request, "You do not have permission to post a disease.")
        return redirect('/')

    if request.method == 'POST':
        form = DiseaseForm(request.POST, request.FILES)
        if form.is_valid():
            disease_name = form.cleaned_data['disease_name']
            description = form.cleaned_data['description']
            image = form.cleaned_data.get('image')
            video = form.cleaned_data.get('video')

            # Check duplicate: same user posting same disease with same details
            existing_disease = Disease.objects.filter(
                user=request.user,
                disease_name__iexact=disease_name,
                description__iexact=description,
                image=image,
                video=video
            ).exists()
            if existing_disease:
                messages.warning(request, "You have already posted this disease.")
                return redirect('/')

            # Save disease
            disease = form.save(commit=False)
            disease.user = request.user

            # Set timezone
            user_tz = pytz.timezone('Africa/Dar_es_Salaam')
            disease.date_created = datetime.now(tz=user_tz)
            disease.date_modified = datetime.now(tz=user_tz)

            disease.save()
            messages.success(request, "Disease added successfully.")
            return redirect('/')
        else:
            messages.error(request, "There was an error with your submission.")
            return redirect('/')
    else:
        disease_form = DiseaseForm()
        return render(request, 'disease_form.html', {'disease_form': disease_form})



# ---------------- Medicine View ----------------
def post_medicine(request):
    user_rank = getattr(request.user.user_detail, 'company_rank', '').lower()
    if user_rank not in ['manager', 'doctor']:
        messages.error(request, "You do not have permission to post a medicine.")
        return redirect('/')

    if request.method == 'POST':
        form = MedicineForm(request.POST, request.FILES)
        if form.is_valid():
            medicine_name = form.cleaned_data['medicine_name']
            description = form.cleaned_data['description']
            image = form.cleaned_data.get('image')
            video = form.cleaned_data.get('video')

            existing = Medicine.objects.filter(
                user=request.user,
                medicine_name__iexact=medicine_name,
                description__iexact=description,
                image=image,
                video=video
            ).exists()
            if existing:
                messages.warning(request, "You have already posted this medicine.")
                return redirect('/')

            medicine = form.save(commit=False)
            medicine.user = request.user
            user_tz = pytz.timezone('Africa/Dar_es_Salaam')
            medicine.date_created = datetime.now(tz=user_tz)
            medicine.date_modified = datetime.now(tz=user_tz)
            medicine.save()
            messages.success(request, "Medicine added successfully.")
            return redirect('/')
        else:
            messages.error(request, "There was an error with your submission.")
            return redirect('/')
    else:
        form = MedicineForm()
        return render(request, 'medicine_form.html', {'medicine_form': form})


# ---------------- CheckUp View ----------------
def post_checkup(request):
    user_rank = getattr(request.user.user_detail, 'company_rank', '').lower()
    if user_rank not in ['manager', 'doctor']:
        messages.error(request, "You do not have permission to post a checkup.")
        return redirect('/')

    if request.method == 'POST':
        form = CheckUpForm(request.POST, request.FILES)
        if form.is_valid():
            checkup_name = form.cleaned_data['checkup_name']
            description = form.cleaned_data['description']
            image = form.cleaned_data.get('image')
            video = form.cleaned_data.get('video')

            existing = CheckUp.objects.filter(
                user=request.user,
                checkup_name__iexact=checkup_name,
                description__iexact=description,
                image=image,
                video=video
            ).exists()
            if existing:
                messages.warning(request, "You have already posted this checkup.")
                return redirect('/')

            checkup = form.save(commit=False)
            checkup.user = request.user
            user_tz = pytz.timezone('Africa/Dar_es_Salaam')
            checkup.date_created = datetime.now(tz=user_tz)
            checkup.date_modified = datetime.now(tz=user_tz)
            checkup.save()
            messages.success(request, "CheckUp added successfully.")
            return redirect('/')
        else:
            messages.error(request, "There was an error with your submission.")
            return redirect('/')
    else:
        form = CheckUpForm()
        return render(request, 'checkup_form.html', {'checkup_form': form})


# ---------------- BusinessPlan View ----------------
def post_businessplan(request):
    user_rank = getattr(request.user.user_detail, 'company_rank', '').lower()
    if user_rank not in ['manager', 'business_teacher']:
        messages.error(request, "You do not have permission to post a business plan.")
        return redirect('/')

    if request.method == 'POST':
        form = BusinessPlanForm(request.POST, request.FILES)
        if form.is_valid():
            description = form.cleaned_data['description']
            image = form.cleaned_data.get('image')
            video = form.cleaned_data.get('video')

            existing = BusinessPlan.objects.filter(
                user=request.user,
                description__iexact=description,
                image=image,
                video=video
            ).exists()
            if existing:
                messages.warning(request, "You have already posted this business plan.")
                return redirect('/')

            plan = form.save(commit=False)
            plan.user = request.user
            user_tz = pytz.timezone('Africa/Dar_es_Salaam')
            plan.date_created = datetime.now(tz=user_tz)
            plan.date_modified = datetime.now(tz=user_tz)
            plan.save()
            messages.success(request, "Business Plan added successfully.")
            return redirect('/')
        else:
            messages.error(request, "There was an error with your submission.")
            return redirect('/')
    else:
        form = BusinessPlanForm()
        return render(request, 'businessplan_form.html', {'businessplan_form': form})


# ---------------- BusinessLevel View ----------------
def post_businesslevel(request):
    user_rank = getattr(request.user.user_detail, 'company_rank', '').lower()
    if user_rank not in ['manager', 'business_teacher']:
        messages.error(request, "You do not have permission to post a business level.")
        return redirect('/')

    if request.method == 'POST':
        form = BusinessLevelForm(request.POST, request.FILES)
        if form.is_valid():
            level_name = form.cleaned_data['level_name']
            description = form.cleaned_data['description']
            image = form.cleaned_data.get('image')
            video = form.cleaned_data.get('video')

            existing = BusinessLevel.objects.filter(
                user=request.user,
                level_name__iexact=level_name,
                description__iexact=description,
                image=image,
                video=video
            ).exists()
            if existing:
                messages.warning(request, "You have already posted this business level.")
                return redirect('/')

            level = form.save(commit=False)
            level.user = request.user
            user_tz = pytz.timezone('Africa/Dar_es_Salaam')
            level.date_created = datetime.now(tz=user_tz)
            level.date_modified = datetime.now(tz=user_tz)
            level.save()
            messages.success(request, "Business Level added successfully.")
            return redirect('/')
        else:
            messages.error(request, "There was an error with your submission.")
            return redirect('/')
    else:
        form = BusinessLevelForm()
        return render(request, 'businesslevel_form.html', {'businesslevel_form': form})


# ---------------- Patient View ----------------
def post_patient(request):
    user_rank = getattr(request.user.user_detail, 'company_rank', '').lower()
    if user_rank not in ['director','vice_director','manager','reception','supervisor']:
        messages.error(request, "You do not have permission to register a patient.")
        return redirect('/')

    if request.method == 'POST':
        form = PatientModelForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            mobile_no = form.cleaned_data['mobile_no']

            existing = PatientForm.objects.filter(
                user=request.user,
                full_name__iexact=full_name,
                mobile_no=mobile_no
            ).exists()
            if existing:
                messages.warning(request, "You have already registered this patient.")
                return redirect('/')

            patient = form.save(commit=False)
            patient.user = request.user
            user_tz = pytz.timezone('Africa/Dar_es_Salaam')
            patient.date_created = datetime.now(tz=user_tz)
            patient.date_modified = datetime.now(tz=user_tz)
            patient.save()
            messages.success(request, "Patient registered successfully.")
            return redirect('/')
        else:
            messages.error(request, "There was an error with your submission.")
            return redirect('/')
    else:
        form = PatientModelForm()
        return render(request, 'patient_form.html', {'patient_form': form})

    
# ---------------- Advertisement View ----------------
def post_advertisement(request):
    #If you want role-based restrictions, adjust here
    user_rank = getattr(request.user.user_detail, 'company_rank', '').lower()
    if user_rank not in ['director','vice_director','manager','reception','supervisor','business_teacher','doctor','it_officer']:
        messages.error(request, "You do not have permission to post an advertisement.")
        return redirect('/')

    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES)
        if form.is_valid():
            infoname = form.cleaned_data['infoname']
            description = form.cleaned_data['description']
            location = form.cleaned_data['location']
            image = form.cleaned_data.get('image')
            video = form.cleaned_data.get('video')

            # Prevent duplicate posts
            existing = Advertisement.objects.filter(
                user=request.user,
                infoname__iexact=infoname,
                description__iexact=description,
                location__iexact=location,
                image=image,
                video=video
            ).exists()

            if existing:
                messages.warning(request, "You have already posted this advertisement.")
                return redirect('/')

            advertisement = form.save(commit=False)
            advertisement.user = request.user
            user_tz = pytz.timezone('Africa/Dar_es_Salaam')
            advertisement.date_created = datetime.now(tz=user_tz)
            advertisement.date_modified = datetime.now(tz=user_tz)
            advertisement.save()

            messages.success(request, "Advertisement added successfully.")
            return redirect('/')
        else:
            messages.error(request, "There was an error with your submission.")
            return redirect('/')
    else:
        form = AdvertisementForm()
        return render(request, 'advertisement_form.html', {'advertisement_form': form})
    
    
    
# ---------------- CheckUp Sales View ----------------
def post_checkup_sales(request):
    user_rank = getattr(request.user.user_detail, 'company_rank', '').lower()
    if user_rank not in ['manager', 'doctor']:
        messages.error(request, "You do not have permission to record a medicine sale.")
        return redirect('/')

    if request.method == 'POST':
        form = CheckUpSalesForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            exists = CheckUp_SalesForm.objects.filter(
                user=request.user,
                checkup=data['checkup']  # check uniqueness by checkupId
            ).exists()
            if exists:
                messages.warning(request, "You have already recorded a sale for this checkup.")
                return redirect('/')

            sale = form.save(commit=False)
            sale.user = request.user
            user_tz = pytz.timezone('Africa/Dar_es_Salaam')
            sale.date_created = datetime.now(tz=user_tz)
            sale.date_modified = datetime.now(tz=user_tz)
            sale.save()
            messages.success(request, "CheckUp Sale recorded successfully.")
            return redirect('/')
        messages.error(request, "There was an error with your submission.")
        return redirect('/')
    form = CheckUpSalesForm()
    return render(request, 'checkup_sales_form.html', {'checkup_sales_form': form})


# ---------------- Medicine Sales View ----------------
def post_medicine_sales(request):
    user_rank = getattr(request.user.user_detail, 'company_rank', '').lower()
    if user_rank not in ['manager', 'doctor']:
        messages.error(request, "You do not have permission to record a medicine sale.")
        return redirect('/')

    if request.method == 'POST':
        form = MedicineSalesForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            exists = Medicine_SalesForm.objects.filter(
                user=request.user,
                medicine=data['medicine']  # check uniqueness by medicineId
            ).exists()
            if exists:
                messages.warning(request, "You have already recorded a sale for this medicine.")
                return redirect('/')

            sale = form.save(commit=False)
            sale.user = request.user
            user_tz = pytz.timezone('Africa/Dar_es_Salaam')
            sale.date_created = datetime.now(tz=user_tz)
            sale.date_modified = datetime.now(tz=user_tz)
            sale.save()
            messages.success(request, "Medicine Sale recorded successfully.")
            return redirect('/')
        messages.error(request, "There was an error with your submission.")
        return redirect('/')
    form = MedicineSalesForm()
    return render(request, 'medicine_sales_form.html', {'medicine_sales_form': form})
    

def analysis(request):
    return render(request, 'analysis.html')

def comment(request):
    return render(request, 'comment.html')

def account(request):
    return render(request, 'account.html')


###START REGISTER AND LOGIN AUTHORZATION
def register(request):
    if request.method == 'POST':
        # SuperUser
        if 'register_admin' in request.POST:
            form = SuperUserRegistrationForm(request.POST, request.FILES)
            if form.is_valid():
                admin = form.save(commit=False)
                admin.is_staff = True
                admin.is_superuser = True
                admin.save()
                form.save(commit=True)
                messages.success(request, "Admin registered successfully.")
                return redirect('login')
            else:
                return render(request, 'register_admin.html', {'admin_form': form})

        # Member
        elif 'register_member' in request.POST:
            form = MemberRegistrationForm(request.POST, request.FILES)
            if form.is_valid():
                member = form.save()
                messages.success(request, "Member registered successfully.")
                return redirect('login')
            else:
                return render(request, 'register.html', {'member_form': form})

        # Viewer
        elif 'register_viewer' in request.POST:
            form = ViewerRegistrationForm(request.POST)
            if form.is_valid():
                viewer = form.save()
                messages.success(request, "Viewer registered successfully.")
                return redirect('login')
            else:
                return render(request, 'register_viewer.html', {'viewer_form': form})

    else:
        admin_form = SuperUserRegistrationForm()
        member_form = MemberRegistrationForm()
        viewer_form = ViewerRegistrationForm()

    if request.resolver_match.url_name == 'register_admin':
        return render(request, 'register_admin.html', {'admin_form': admin_form})
    elif request.resolver_match.url_name == 'register_member':
        return render(request, 'register.html', {'member_form': member_form})
    else:  # register_viewer
        return render(request, 'register_viewer.html', {'viewer_form': viewer_form})

def login_view(request):
    form = AuthenticationForm()

    if request.method == 'POST':
        login_method = request.POST.get('login_method')
        login_input = request.POST.get('login_input')
        password = request.POST.get('password')

        user = None
        if login_method == 'username':
            user = authenticate(request, username=login_input, password=password)
        elif login_method == 'email':
            try:
                user_obj = User.objects.get(email=login_input)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
        elif login_method == 'mobile':
            # Check UserDetail
            from .models import UserDetail, Viewer
            try:
                user_detail = UserDetail.objects.get(mobile_contact=login_input)
                user = authenticate(request, username=user_detail.user.username, password=password)
            except UserDetail.DoesNotExist:
                # Check Viewer
                try:
                    viewer_detail = Viewer.objects.get(mobile_contact=login_input)
                    user = authenticate(request, username=viewer_detail.user.username, password=password)
                except Viewer.DoesNotExist:
                    user = None

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect('/')
        else:
            messages.error(request, "Invalid login credentials.")

    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')




# def post_medicine_sales(request):
#     user_rank = getattr(request.user.user_detail, 'company_rank', '').lower()
#     if user_rank not in ['company manager', 'doctor']:
#         messages.error(request, "You do not have permission to record a medicine sale.")
#         return redirect('/')

#     if request.method == 'POST':
#         form = MedicineSalesForm(request.POST)
#         if form.is_valid():
#             medicine_type = form.cleaned_data['medicine_type']
#             medicine_cost = form.cleaned_data['medicine_cost']

#             existing = Medicine_SalesForm.objects.filter(
#                 user=request.user,
#                 medicine_type__iexact=medicine_type,
#                 medicine_cost=medicine_cost
#             ).exists()
#             if existing:
#                 messages.warning(request, "You have already recorded this medicine sale.")
#                 return redirect('/')

#             sale = form.save(commit=False)
#             sale.user = request.user
#             user_tz = pytz.timezone('Africa/Dar_es_Salaam')
#             sale.date_created = datetime.now(tz=user_tz)
#             sale.date_modified = datetime.now(tz=user_tz)
#             sale.save()
#             messages.success(request, "Medicine Sale recorded successfully.")
#             return redirect('/')
#         else:
#             messages.error(request, "There was an error with your submission.")
#             return redirect('/')
#     else:
#         form = MedicineSalesForm()
#         return render(request, 'medicine_sales_form.html', {'medicine_sales_form': form})