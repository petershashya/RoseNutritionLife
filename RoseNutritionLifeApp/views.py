from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.template.loader import render_to_string
from django.http import JsonResponse,HttpResponse,HttpRequest,HttpResponseRedirect
from .models import (
    UserDetail,Disease ,Medicine, CheckUp, BusinessPlan, 
    BusinessLevel,Medicine_SalesForm, CheckUp_SalesForm,PatientForm ,
    Advertisement,Shop,Branch,Meeting,Log,About,Viewer,
    DiseaseComment,MedicineComment,CheckupComment,BusinessplanComment,BusinesslevelComment,Viewer ,Comment
)
from .forms import (
    MedicineForm, CheckUpForm, BusinessPlanForm, BusinessLevelForm,
    SuperUserRegistrationForm, MemberRegistrationForm, ViewerRegistrationForm ,
    DiseaseForm, MedicineForm, CheckUpForm, BusinessPlanForm, BusinessLevelForm, 
    CheckUpSalesForm, MedicineSalesForm ,PatientModelForm, 
    CheckUpSalesForm, MedicineSalesForm,AdvertisementForm,ShopForm,BranchForm,MeetingForm,AboutForm,
    DiseaseCommentForm,MedicineCommentForm,CheckupCommentForm,BusinessplanCommentForm,BusinesslevelCommentForm,
    ForgotPasswordForm,ResetPasswordForm,UserDetailForm, CommentForm,
)

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from datetime import datetime
from django.utils import timezone
from django.db.models import Sum
import pytz
from django.core.paginator import Paginator
from django.utils.timesince import timesince
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash

import csv
from io import BytesIO
# ReportLab imports
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# Other imports
import xlsxwriter
import base64
import json
import textwrap


def home(request):
    #start count logs for views
    log, created = Log.objects.get_or_create(
            user_id=None
        )
    if not created:
            log.home_page_count += 1
    log.save()
    
    # Get the first posted (earliest) item for each table
    first_disease = Disease.objects.order_by("date_created").first()
    first_medicine = Medicine.objects.order_by("date_created").first()
    first_checkup = CheckUp.objects.order_by("date_created").first()
    first_business_plan = BusinessPlan.objects.order_by("date_created").first()
    first_business_level = BusinessLevel.objects.order_by("date_created").first()
    abouts=About.objects.all()
    it_officer_rank = get_it_officer_rank(request.user)
    request_id=request.user.id
    
    #comments = Comment.objects.select_related('user').order_by('-id')
    comments_qs = (
    Comment.objects
    .select_related('user', 'user__user_detail')
    .filter(confirmed=False)
    .order_by('-id')
    )

    comments = [
        {
            "id": c.id,
            "username": c.user.username if c.user else "Anonymous",
            "profile_image": (
                c.user.user_detail.profile_image.url
                if c.user and hasattr(c.user, 'user_detail') and c.user.user_detail.profile_image
                else ""
            ),
            "first_name": c.user.first_name,
            "last_name": c.user.last_name,
            "comment": c.comment,
            "date_created": c.date_created,
            "user_id": c.user.id,
        }
        for c in comments_qs
    ]

    context = {
        "disease": first_disease,
        "medicine": first_medicine,
        "checkup": first_checkup,
        "business_plan": first_business_plan,
        "business_level": first_business_level,
        "abouts" : abouts,
        "comments" : comments,
        "it_officer_rank":it_officer_rank,
        "request_id" : request_id,
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
    it_officer_rank = get_it_officer_rank(request.user)
    context = {
        "disease_page_obj": paginate_and_prepare(request, Disease.objects.all(), "disease_page"),
        "medicine_page_obj": paginate_and_prepare(request, Medicine.objects.all(), "medicine_page"),
        "checkup_page_obj": paginate_and_prepare(request, CheckUp.objects.all(), "checkup_page"),
        "bp_page_obj": paginate_and_prepare(request, BusinessPlan.objects.all(), "bp_page"),
        "bl_page_obj": paginate_and_prepare(request, BusinessLevel.objects.all(), "bl_page"),
        "it_officer_rank" : it_officer_rank,
    }
    return render(request, "service.html", context)


def advertisement(request):
    disease_imgs=Disease.objects.all()
    medicine_imgs=Medicine.objects.all()
    checkup_imgs=CheckUp.objects.all()
    
    disease_videos=Disease.objects.all()
    medicine_videos=Medicine.objects.all()
    checkup_videos=CheckUp.objects.all()
    
    context = {
        "disease_imgs" : disease_imgs,
        "medicine_imgs" : medicine_imgs,
        "checkup_imgs" : checkup_imgs,
        
        "disease_videos" : disease_videos,
        "medicine_videos" : medicine_videos,
        "checkup_videos" : checkup_videos,
    }
    
    return render(request, 'advertisement.html', context)


def posture_details(request, model_type, item_id):
    model_map = {
        'disease': Disease,
        'medicine': Medicine,
        'checkup': CheckUp,
        'businessplan': BusinessPlan,
        'businesslevel': BusinessLevel,
    }

    model_class = model_map.get(model_type.lower())
    if not model_class:
        messages.error(request, "Invalid posture type selected.")
        return redirect('/')

    obj = get_object_or_404(model_class, id=item_id)

    context = {
        'object': obj,
        'model_type': model_type,
    }

    return render(request, 'posture_modal.html', context)


def video_details(request, model_type, item_id):
    model_map = {
        'disease': Disease,
        'medicine': Medicine,
        'checkup': CheckUp,
        'businessplan': BusinessPlan,
        'businesslevel': BusinessLevel,
    }

    model_class = model_map.get(model_type.lower())
    if not model_class:
        messages.error(request, "Invalid video type selected.")
        return redirect('/')

    obj = get_object_or_404(model_class, id=item_id)

    context = {
        'object': obj,
        'model_type': model_type,
    }

    return render(request, 'video_modal.html', context)



def lists_details(request, model_type):
    model_map = {
        'disease': Disease,
        'medicine': Medicine,
        'checkup': CheckUp,
        'businessplan': BusinessPlan,
        'businesslevel': BusinessLevel,
    }

    model_class = model_map.get(model_type.lower())
    if not model_class:
        messages.error(request, "Invalid lists type selected.")
        return redirect('/')

    objs = model_class.objects.all()

    context = {
        'objects': objs,
        'model_type': model_type,
    }

    return render(request, 'lists_modal.html', context)



def list_details(request, model_type, item_id):
    model_map = {
        'disease': Disease,
        'medicine': Medicine,
        'checkup': CheckUp,
        'businessplan': BusinessPlan,
        'businesslevel': BusinessLevel,
    }

    model_class = model_map.get(model_type.lower())
    if not model_class:
        messages.error(request, "Invalid List type selected.")
        return redirect('/')

    obj = get_object_or_404(model_class, id=item_id)

    context = {
        'object': obj,
        'model_type': model_type,
    }

    return render(request, 'list_modal.html', context)



def business_details(request, model_type, item_id):
    model_map = {
        'businessplan': BusinessPlan,
        'businesslevel': BusinessLevel,
    }

    model_class = model_map.get(model_type.lower())
    if not model_class:
        messages.error(request, "Invalid business type selected.")
        return redirect('/')

    obj = get_object_or_404(model_class, id=item_id)

    context = {
        'object': obj,
        'model_type': model_type,
    }

    return render(request, 'business_modal.html', context)



def advertisement_details(request, model_type):
    model_map = {
        'shop': Shop,
        'branch': Branch,
        'meeting': Meeting,
        'advertisement': Advertisement,
    }

    model_class = model_map.get(model_type.lower())
    if not model_class:
        messages.error(request, "Invalid advertisement type selected.")
        return redirect('/')

    objs = model_class.objects.all()

    context = {
        'objects': objs,
        'model_type': model_type,
    }

    return render(request, 'advertisement_modal.html', context)


def advertisement_tables(request, model_type):
    model_map = {
        'shoptable': Shop,
        'branchtable': Branch,
        'meetingtable': Meeting,
        'otheradstable': Advertisement,
        'abouttable': About,
        'commenttable': Comment,
    }

    model_class = model_map.get(model_type.lower())
    if not model_class:
        messages.error(request, "Invalid table type selected.")
        return redirect('/')

    objs = model_class.objects.all()

    # Auto select related user + user_detail when model has FK user
    if hasattr(model_class, 'user'):
        objs = objs.select_related('user', 'user__user_detail')

    enriched = []

    for obj in objs:
        data = {"object": obj}

        # Add user + user_detail fields ONLY if model has user FK
        if hasattr(obj, 'user'):
            user = getattr(obj, 'user', None)

            data.update({
                "user_id": user.id if user else None,
                "username": user.username if user else None,
                "first_name": user.first_name if user else None,
                "last_name": user.last_name if user else None,
                "profile_image": (
                    user.user_detail.profile_image.url
                    if user and hasattr(user, "user_detail") and user.user_detail.profile_image
                    else None
                ),
                "user_detail": (
                    user.user_detail if user and hasattr(user, "user_detail") else None
                ),
            })

        enriched.append(data)

    context = {
        "objects": enriched,
        "objs_count": objs.count(),
        "model_type": model_type,
    }

    if model_class == Shop :
        return render(request, 'shoptable_modal.html', context)
    if model_class == Branch :
        return render(request, 'branchtable_modal.html', context)
    if model_class == Meeting :
        return render(request, 'meetingtable_modal.html', context)
    if model_class == Advertisement :
        return render(request, 'advertisementtable_modal.html', context)
    if model_class == About :
        return render(request, 'abouttable_modal.html', context)
    if model_class == Comment :
        return render(request, 'commenttable_modal.html', context)
    
    

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
    if user_rank not in ['manager', 'doctor','it_officer']:
        messages.error(request, "You do not have permission to post a disease.")
        return redirect('/')

    if request.method == 'POST':
        form = DiseaseForm(request.POST, request.FILES)
        if form.is_valid():
            disease_name = form.cleaned_data['disease_name']
            description = form.cleaned_data['description']
            profile_image = form.cleaned_data.get('profile_image')
            image = form.cleaned_data.get('image')
            video = form.cleaned_data.get('video')

            # Check duplicate: same user posting same disease with same details
            existing_disease = Disease.objects.filter(
                user=request.user,
                disease_name__iexact=disease_name,
                description__iexact=description,
                profile_image=profile_image,
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
    if user_rank not in ['manager', 'doctor','it_officer']:
        messages.error(request, "You do not have permission to post a medicine.")
        return redirect('/')

    if request.method == 'POST':
        form = MedicineForm(request.POST, request.FILES)
        if form.is_valid():
            medicine_name = form.cleaned_data['medicine_name']
            description = form.cleaned_data['description']
            profile_image = form.cleaned_data.get('profile_image')
            image = form.cleaned_data.get('image')
            video = form.cleaned_data.get('video')

            existing = Medicine.objects.filter(
                user=request.user,
                medicine_name__iexact=medicine_name,
                description__iexact=description,
                profile_image =profile_image,
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
    if user_rank not in ['manager', 'doctor','it_officer']:
        messages.error(request, "You do not have permission to post a checkup.")
        return redirect('/')

    if request.method == 'POST':
        form = CheckUpForm(request.POST, request.FILES)
        if form.is_valid():
            checkup_name = form.cleaned_data['checkup_name']
            description = form.cleaned_data['description']
            profile_image = form.cleaned_data.get('profile_image')
            image = form.cleaned_data.get('image')
            video = form.cleaned_data.get('video')

            existing = CheckUp.objects.filter(
                user=request.user,
                checkup_name__iexact=checkup_name,
                description__iexact=description,
                profile_image = profile_image,
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
    if user_rank not in ['manager', 'business_teacher','it_officer']:
        messages.error(request, "You do not have permission to post a business plan.")
        return redirect('/')

    if request.method == 'POST':
        form = BusinessPlanForm(request.POST, request.FILES)
        if form.is_valid():
            description = form.cleaned_data['description']
            profile_image = form.cleaned_data.get('profile_image')
            image = form.cleaned_data.get('image')
            video = form.cleaned_data.get('video')

            existing = BusinessPlan.objects.filter(
                user=request.user,
                description__iexact=description,
                profile_image = profile_image,
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
    if user_rank not in ['manager', 'business_teacher','it_officer']:
        messages.error(request, "You do not have permission to post a business level.")
        return redirect('/')

    if request.method == 'POST':
        form = BusinessLevelForm(request.POST, request.FILES)
        if form.is_valid():
            level_name = form.cleaned_data['level_name']
            description = form.cleaned_data['description']
            profile_image = form.cleaned_data.get('profile_image')
            image = form.cleaned_data.get('image')
            video = form.cleaned_data.get('video')

            existing = BusinessLevel.objects.filter(
                user=request.user,
                level_name__iexact=level_name,
                description__iexact=description,
                profile_image = profile_image,
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
    if user_rank not in ['director','vice_director','manager','reception','supervisor','it_officer']:
        messages.error(request, "You do not have permission to register a patient.")
        return redirect('/')

    if request.method == 'POST':
        form = PatientModelForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            mobile_no = form.cleaned_data['mobile_no']
            membership_no = form.cleaned_data.get('membership_no')

            # Check if membership_no exists in UserDetail
            member_exists = UserDetail.objects.filter(membership_no=membership_no).exists()
            if not member_exists:
                messages.error(request, f"Member with membership number '{membership_no}' not found.")
                return redirect('/')

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

# def post_patient(request):
#     user_rank = getattr(request.user.user_detail, 'company_rank', '').lower()
#     if user_rank not in ['director', 'vice_director', 'manager', 'reception', 'supervisor', 'it_officer']:
#         messages.error(request, "You do not have permission to register a patient.")
#         return redirect('/')

#     if request.method == 'POST':
#         form = PatientModelForm(request.POST)
#         if form.is_valid():
#             full_name = form.cleaned_data['full_name']
#             mobile_no = form.cleaned_data['mobile_no']
#             membership_no = form.cleaned_data.get('membership_no')

#             # Check if membership_no exists in UserDetail
#             member_exists = UserDetail.objects.filter(mobile_contact=membership_no).exists()
#             if not member_exists:
#                 messages.error(request, f"Member with membership number '{membership_no}' not found.")
#                 return redirect('/')

#             # Check if this patient already exists for this user
#             existing = PatientForm.objects.filter(
#                 user=request.user,
#                 full_name__iexact=full_name,
#                 mobile_no=mobile_no
#             ).exists()
#             if existing:
#                 messages.warning(request, "You have already registered this patient.")
#                 return redirect('/')

#             # Save patient
#             patient = form.save(commit=False)
#             patient.user = request.user
#             user_tz = pytz.timezone('Africa/Dar_es_Salaam')
#             patient.date_created = datetime.now(tz=user_tz)
#             patient.date_modified = datetime.now(tz=user_tz)
#             patient.save()
#             messages.success(request, "Patient registered successfully.")
#             return redirect('/')
#         else:
#             messages.error(request, "There was an error with your submission.")
#             return redirect('/')
#     else:
#         form = PatientModelForm()
#         return render(request, 'patient_form.html', {'patient_form': form})

    
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
    

# ---------------- shopt View ----------------
def post_shop(request):
    #If you want role-based restrictions, adjust here
    user_rank = getattr(request.user.user_detail, 'company_rank', '').lower()
    if user_rank not in ['vice_director','manager','reception','supervisor','business_teacher','doctor','it_officer']:
        messages.error(request, "You do not have permission to post an shop.")
        return redirect('/')

    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES)
        if form.is_valid():
            infoname = form.cleaned_data['infoname']
            description = form.cleaned_data['description']
            location = form.cleaned_data['location']
            image = form.cleaned_data.get('image')
            video = form.cleaned_data.get('video')

            # Prevent duplicate posts
            existing = Shop.objects.filter(
                user=request.user,
                infoname__iexact=infoname,
                description__iexact=description,
                location__iexact=location,
                image=image,
                video=video
            ).exists()

            if existing:
                messages.warning(request, "You have already posted this shop.")
                return redirect('/')

            shop = form.save(commit=False)
            shop.user = request.user
            user_tz = pytz.timezone('Africa/Dar_es_Salaam')
            shop.date_created = datetime.now(tz=user_tz)
            shop.date_modified = datetime.now(tz=user_tz)
            shop.save()

            messages.success(request, "Shop added successfully.")
            return redirect('/')
        else:
            messages.error(request, "There was an error with your submission.")
            return redirect('/')
    else:
        form = ShopForm()
        return render(request, 'shop_form.html', {'shop_form': form})
    



# ---------------- Meeting View ----------------
def post_meeting(request):
    #If you want role-based restrictions, adjust here
    user_rank = getattr(request.user.user_detail, 'company_rank', '').lower()
    if user_rank not in ['director','vice_director','manager','reception','supervisor','business_teacher','doctor','it_officer']:
        messages.error(request, "You do not have permission to post an meeting.")
        return redirect('/')

    if request.method == 'POST':
        form = MeetingForm(request.POST, request.FILES)
        if form.is_valid():
            infoname = form.cleaned_data['infoname']
            description = form.cleaned_data['description']
            location = form.cleaned_data['location']
            image = form.cleaned_data.get('image')
            video = form.cleaned_data.get('video')

            # Prevent duplicate posts
            existing = Meeting.objects.filter(
                user=request.user,
                infoname__iexact=infoname,
                description__iexact=description,
                location__iexact=location,
                image=image,
                video=video
            ).exists()

            if existing:
                messages.warning(request, "You have already posted this meeting.")
                return redirect('/')

            meeting = form.save(commit=False)
            meeting.user = request.user
            user_tz = pytz.timezone('Africa/Dar_es_Salaam')
            meeting.date_created = datetime.now(tz=user_tz)
            meeting.date_modified = datetime.now(tz=user_tz)
            meeting.save()

            messages.success(request, "Meeting added successfully.")
            return redirect('/')
        else:
            messages.error(request, "There was an error with your submission.")
            return redirect('/')
    else:
        form = MeetingForm()
        return render(request, 'meeting_form.html', {'meeting_form': form})
    
    

# ---------------- Branch View ----------------
def post_branch(request):
    #If you want role-based restrictions, adjust here
    user_rank = getattr(request.user.user_detail, 'company_rank', '').lower()
    if user_rank not in ['director','vice_director','manager','reception','supervisor','business_teacher','doctor','it_officer']:
        messages.error(request, "You do not have permission to post an branch.")
        return redirect('/')

    if request.method == 'POST':
        form = BranchForm(request.POST, request.FILES)
        if form.is_valid():
            infoname = form.cleaned_data['infoname']
            description = form.cleaned_data['description']
            location = form.cleaned_data['location']
            image = form.cleaned_data.get('image')
            video = form.cleaned_data.get('video')

            # Prevent duplicate posts
            existing = Branch.objects.filter(
                user=request.user,
                infoname__iexact=infoname,
                description__iexact=description,
                location__iexact=location,
                image=image,
                video=video
            ).exists()

            if existing:
                messages.warning(request, "You have already posted this branch.")
                return redirect('/')

            branch = form.save(commit=False)
            branch.user = request.user
            user_tz = pytz.timezone('Africa/Dar_es_Salaam')
            branch.date_created = datetime.now(tz=user_tz)
            branch.date_modified = datetime.now(tz=user_tz)
            branch.save()

            messages.success(request, "Branch added successfully.")
            return redirect('/')
        else:
            messages.error(request, "There was an error with your submission.")
            return redirect('/')
    else:
        form = AdvertisementForm()
        return render(request, 'branch_form.html', {'branch_form': form})
    
    
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


# ---------------- About View ----------------
@login_required
def post_about(request, about_id=None):
    user_rank = getattr(request.user.user_detail, 'company_rank', '').lower()
    if user_rank not in ["manager", "doctor", "it_officer"]:
        messages.error(request, "You do not have permission to manage About.")
        return redirect('/')

    about_instance = get_object_or_404(About, id=about_id, user=request.user) if about_id else None

    if request.method == "POST":
        form = AboutForm(request.POST, request.FILES, instance=about_instance)
        if form.is_valid():
            about = form.save(commit=False)
            about.user = request.user
            tz = pytz.timezone("Africa/Dar_es_Salaam")
            now = datetime.now(tz)
            about.date_created = about_instance.date_created if about_instance else now
            about.date_modified = now
            about.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": True})
            messages.success(request, "About saved successfully.")
            return redirect('/')
        else:
            # Show exact form errors
            errors = form.errors.as_json()
            print("AboutForm errors:", errors)  # Debug
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": False, "errors": errors})
            messages.error(request, f"Form submission error: {form.errors}")
            return render(request, "about_form_modal.html", {"about_form": form, "about_instance": about_instance})

    else:
        form = AboutForm(instance=about_instance)
        return render(request, "about_form.html", {"about_form": form, "about_instance": about_instance})


    

def analysis(request):
    patients=PatientForm.objects.all()
    members=User.objects.all()
    medicines=Medicine.objects.all()
    checkups=CheckUp.objects.all()
    # viewers=Viewer.objects.all()
    
    patient_count=patients.count()
    member_count=members.count()
    medicine_count=medicines.count()
    checkup_count=checkups.count()
    # viewer_count=viewers.count()
    
    it_officer_rank = get_it_officer_rank(request.user)
    
    context = {
        "patient_count": patient_count,
        "member_count" : member_count,
        "medicine_count" : medicine_count,
        "checkup_count" : checkup_count,
        "it_officer_rank" : it_officer_rank,
        # "viewer_count" : viewer_count,
    }
    
    
    return render(request, 'analysis.html',context)



#start showing charts modals
def show_chart(request, type):
    """
    Returns JSON data for Chart.js visualization.
    """

    # Base counts
    user_count = User.objects.count()
    patient_count = PatientForm.objects.count()
    medicine_count = Medicine.objects.count()
    checkup_count = CheckUp.objects.count()

    # Gender counts
    male_users = UserDetail.objects.filter(gender='M').count()
    female_users = UserDetail.objects.filter(gender='F').count()

    male_patients = PatientForm.objects.filter(gender='M').count()
    female_patients = PatientForm.objects.filter(gender='F').count()

    # Population chart: send labels, ages, and genders separately
    population_qs = PatientForm.objects.values('id', 'age', 'gender')
    population_labels = [f"ID-{p['id']}" for p in population_qs]
    population_ages = [p['age'] for p in population_qs]
    population_genders = [p['gender'] for p in population_qs]

    # Response data
    data = {
        #"models": ["Users", "Patients", "Medicines", "Checkups"],
        "models": ["Wanachama", "Wagonjwa", "Madawa", "Vipimo"],
        "ids": [user_count, patient_count, medicine_count, checkup_count],
        "stack_data": {
            "male": [male_users, male_patients, 0, 0],
            "female": [female_users, female_patients, 0, 0],
        },
        "pie_data": [user_count, patient_count, medicine_count, checkup_count],
        "population": {
            "labels": population_labels,
            "ages": population_ages,
            "genders": population_genders
        }
    }

    return JsonResponse(data)


#Print chart views imaages
def print_chart_pdf(request):
    """
    Receives chart data (title, description, image)
    and returns a generated PDF with a soft background color
    even if the chart has transparent areas.
    """
    if request.method == "POST":
        data = json.loads(request.body)
        title = data.get("title", "Chart View")
        description = data.get("description", "")
        image_data = data.get("image")

        if not image_data:
            return JsonResponse({"error": "No chart image provided."}, status=400)

        # Decode base64 chart image
        image_bytes = base64.b64decode(image_data.split(",")[1])
        image = ImageReader(BytesIO(image_bytes))

        # Create PDF canvas
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        # Title
        p.setFont("Helvetica-Bold", 16)
        p.drawCentredString(width / 2, height - 100, title)

        # --- Define background color ---
        bg_color = colors.Color(226/255, 240/255, 233/255)  # rgb(226, 240, 233)

        # --- Chart box dimensions ---
        chart_width, chart_height = 420, 260
        chart_x = (width - chart_width) / 2
        chart_y = height - 430

        # --- Draw background area for the chart (prevents black) ---
        p.setFillColor(bg_color)
        p.roundRect(chart_x - 10, chart_y - 10, chart_width + 20, chart_height + 20, 10, fill=True, stroke=False)

        # --- Optional: add white rectangle to ensure smooth contrast ---
        p.setFillColor(colors.white)
        p.rect(chart_x, chart_y, chart_width, chart_height, fill=True, stroke=False)

        # --- Draw chart image centered on top ---
        p.drawImage(image, chart_x, chart_y, chart_width, chart_height, mask='auto')

        # --- Draw description text ---
        p.setFont("Helvetica-Bold", 13)
        p.setFillColor(colors.black)
        p.drawString(60, chart_y - 40, "Maelezo ya Utafiti:")

        p.setFont("Helvetica", 12)
        wrapped_lines = textwrap.wrap(description, width=90)
        y_position = chart_y - 60

        for line in wrapped_lines:
            p.drawString(80, y_position, line)
            y_position -= 18

        p.showPage()
        p.save()

        # Return PDF response
        pdf_value = buffer.getvalue()
        buffer.close()

        response = HttpResponse(pdf_value, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{title}.pdf"'
        return response

    return JsonResponse({"error": "Invalid request"}, status=400)



# --------- Comment Model Mapping ---------
COMMENTMODEL_MAP = {
    "disease": (DiseaseComment, DiseaseCommentForm, Disease, "show_comment.html", "delete_comment.html"),
    "medicine": (MedicineComment, MedicineCommentForm, Medicine, "show_comment.html", "delete_comment.html"),
    "checkup": (CheckupComment, CheckupCommentForm, CheckUp, "show_comment.html", "delete_comment.html"),
    "businessplan": (BusinessplanComment, BusinessplanCommentForm, BusinessPlan, "show_comment.html", "delete_comment.html"),
    "businesslevel": (BusinesslevelComment, BusinesslevelCommentForm, BusinessLevel, "show_comment.html", "delete_comment.html"),
}

@login_required
def post_modelcomment(request, model, object_id):
    if model not in COMMENTMODEL_MAP:
        return JsonResponse({"error": "Invalid model type"}, status=400)

    CommentModel, FormClass, ParentModel, template, _ = COMMENTMODEL_MAP[model]
    instance = get_object_or_404(ParentModel, id=object_id)
    user = instance.user

    comments = CommentModel.objects.filter(**{model: instance}).order_by('-date_created')

    comment_details = [
        {
            "id": c.id,
            "username": c.user.username if c.user else "Anonymous",
            "profile_image": (
                c.user.user_detail.profile_image.url
                if c.user and hasattr(c.user, 'user_detail') and c.user.user_detail.profile_image
                else ""
            ),
            "comment": c.comment,
            "date_created": c.date_created,
        }
        for c in comments
    ]

    if request.method == "POST":
        form = FormClass(request.POST)
        if form.is_valid():
            comment_text = form.cleaned_data["comment"].strip()
            if CommentModel.objects.filter(**{model: instance, "user": request.user, "comment__iexact": comment_text}).exists():
                return JsonResponse({"error": "You have already posted this comment."}, status=400)

            new_comment = form.save(commit=False)
            new_comment.user = request.user
            setattr(new_comment, model, instance)
            new_comment.save()
            messages.success(request, "Comment posted successfully.")
            return JsonResponse({"success": True})

        return JsonResponse({"errors": form.errors}, status=400)

    form = FormClass()
    html = render_to_string(
        template,
        {"form": form, "model_comment": comment_details, "model_name": model, "model": instance, "user": user},
        request,
    )
    return HttpResponse(html)



# ---------------------- DELETE COMMENT ----------------------
# --------- EDIT AND DELETE OBJECTS --------
# Allowed ranks for deletion
ALLOWED_RANKS = ["director", "it_officer"]

def has_deletecomment_permission(user):
    """
    Only superusers or users with allowed ranks can delete comments.
    """
    return user.is_superuser or getattr(user, "company_rank", "").lower() in ALLOWED_RANKS


@login_required
@user_passes_test(has_deletecomment_permission)
def delete_modelcomment(request, model, object_id):
    ModelClass, _, _, _, template = COMMENTMODEL_MAP[model]
    instance = get_object_or_404(ModelClass, id=object_id)
    if request.method == "POST":
        instance.delete()
        messages.success(request, f"{model.capitalize()} comment deleted successfully.")
        return JsonResponse({"success": True})
    html = render_to_string(template, {"object": instance, "model": model }, request)
    return HttpResponse(html)





#post comment
COMMENT_MAP = {
    "comment": (CommentForm, Comment, "delete_comment.html"),
}

@login_required
def post_comment(request, model):

    if model not in COMMENT_MAP:
        messages.error(request, "Aina ya maoni sio sahihi.")
        return redirect('/')

    FormClass, CommentModel, template = COMMENT_MAP[model]

    if request.method == "POST":
        form = FormClass(request.POST)

        if form.is_valid():
            comment_text = form.cleaned_data["comment"].strip()

            # Prevent duplicate
            if CommentModel.objects.filter(
                user=request.user,
                comment__iexact=comment_text
            ).exists():
                messages.error(request, "Umeshapost maoni haya tayari.")
                return redirect('/')

            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()

            messages.success(request, "Maoni yako yametumwa kikamilifu!")
            return redirect('/')

        # Form invalid
        messages.error(request, "Tafadhari jaza maelezo yote sahihi.")
        return redirect('/')

    messages.error(request, "Ombi sio sahihi.")
    return redirect('/')


ALLOWED_RANKS = ["director", "it_officer"]

def has_deletecomment_permission(user):
    return user.is_superuser or getattr(user, "company_rank", "").lower() in ALLOWED_RANKS

@login_required
@user_passes_test(has_deletecomment_permission)
def delete_comment(request, model, object_id):

    if model not in COMMENT_MAP:
        return JsonResponse({"error": "Invalid model type"}, status=400)

    FormClass, ModelClass, template = COMMENT_MAP[model]
    instance = get_object_or_404(ModelClass, id=object_id)

    # DELETE request through AJAX
    if request.method == "POST":
        instance.delete()
        messages.error(request, "Umefanikiwa kufuta ujumbe.")
        return JsonResponse({"success": True})

    # Return delete modal HTML for preview
    html = render_to_string(template, {"object": instance, "model": model}, request)
    return JsonResponse({"html": html})



ALLOWED_RANKS = ["director", "it_officer"]
def has_confirmcomment_permission(user):
    rank = getattr(user, "user_detail", None)
    if rank:
        rank = getattr(user.user_detail, "company_rank", "").lower()
    return user.is_superuser or rank in ALLOWED_RANKS

@login_required
@user_passes_test(has_confirmcomment_permission)
def show_confirm_comment_modal(request):
    """
    Returns the confirm_comment modal HTML
    Expects GET parameters:
    - item_id
    - item_type
    - action ('confirm-item' or 'unconfirm-item')
    """
    item_id = request.GET.get('item_id')
    item_type = request.GET.get('item_type')
    action = request.GET.get('action')

    if item_type == 'comment' and item_id:
        comment = get_object_or_404(Comment, id=item_id)
        text = "Are you sure you want to confirm this comment?" if action == 'confirm-item' else "Are you sure you want to unconfirm this comment?"
        return render(request, "confirm_comment.html", {
            "comment": comment,
            "text": text,
            "action": action
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


@login_required
@user_passes_test(has_confirmcomment_permission)
def confirm_comment(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        comment = get_object_or_404(Comment, id=item_id)
        comment.confirmed = True
        comment.save()
        return JsonResponse({'status': 'success', 'message': 'Comment confirmed'})


@login_required
@user_passes_test(has_confirmcomment_permission)
def unconfirm_comment(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        comment = get_object_or_404(Comment, id=item_id)
        comment.confirmed = False
        comment.save()
        return JsonResponse({'status': 'success', 'message': 'Comment unconfirmed'})



def sharedcontent_details(request, model_type, item_id):
    model_map = {
        'diseaseimage': Disease,
        'medicineimage': Medicine,
        'checkupimage': CheckUp,
        'businessplanimage': BusinessPlan,
        'businesslevelimage': BusinessLevel,
    }

    model_class = model_map.get(model_type.lower())
    if not model_class:
        model_map = {
        'diseasevideo': Disease,
        'medicinevideo': Medicine,
        'checkupvideo': CheckUp,
        'businessplanvideo': BusinessPlan,
        'businesslevelvideo': BusinessLevel,
        }
        model_class = model_map.get(model_type.lower())
        if not model_class:
            messages.error(request, "Invalid share type selected.")
            return redirect('/')

        obj = get_object_or_404(model_class, id=item_id)
        context = {
            'object': obj,
            'model_type': model_type,
        }
        return render(request, 'sharedvideo_details.html', context)

    obj = get_object_or_404(model_class, id=item_id)
    context = {
        'object': obj,
        'model_type': model_type,
    }
    return render(request, 'sharedposture_details.html', context)


# def sharedvideo_details(request, model_type, item_id):
#     model_map = {
#         'diseasevideo': Disease,
#         'medicinevideo': Medicine,
#         'checkupvideo': CheckUp,
#         'businessplanvideo': BusinessPlan,
#         'businesslevelvideo': BusinessLevel,
#     }

#     model_class = model_map.get(model_type.lower())
#     if not model_class:
#         messages.error(request, "Invalid video type selected.")
#         return redirect('/')

#     obj = get_object_or_404(model_class, id=item_id)

#     context = {
#         'object': obj,
#         'model_type': model_type,
#     }

#     return render(request, 'sharedvideo_details.html', context)




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
                messages.success(request, "Leader registered successfully.")
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
            form = ViewerRegistrationForm(request.POST, request.FILES)
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



#start able login actions to users
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




#function for check it_officer_rank
def get_it_officer_rank(user):
    """
    Returns 'it_officer' if:
    - user.user_detail.company_rank == 'it_officer'
    Otherwise returns None.
    """
    
    # Safely get company_rank from UserDetail
    user_detail = getattr(user, "user_detail", None)

    if user_detail:
        #rank = getattr(user_detail, "company_rank", "").lower()
        rank = getattr(user_detail, "company_rank", "")
        if rank == "it_officer":
            return "it_officer"
        
        if rank == "director":
            return "director"

    return None


#start superuser accounts
def is_superuser(user):
    return user.is_superuser

def check_superuser(user):
    return user.is_superuser
@user_passes_test(check_superuser, login_url='member_account')
@login_required
def account(request):
    # aboutdetail = About.objects.order_by("company_rank").first()
    userdetails = UserDetail.objects.get(user=request.user)
    user = User.objects.get(username=request.user)
    diseases= Disease.objects.all()
    medicines= Medicine.objects.all()
    checkups= CheckUp.objects.all()
    businesslevels= BusinessLevel.objects.all()
    businessplans= BusinessPlan.objects.all()
    patients= PatientForm.objects.all()
    about_detail = About.objects.get(user=request.user)
    usersdetails=UserDetail.objects.all()
    comments=Comment.objects.all()

    now = timezone.now()
    one_week_ago = now - timezone.timedelta(weeks=1)

    # Active users (last login within a week)
    active_users = User.objects.filter(last_login__gte=one_week_ago, is_active=True)
    active_users_count = active_users.count()

    # Non-staff (normal) users
    non_staff_users = User.objects.filter(is_staff=False, is_superuser=False)
    non_staff_users_count = non_staff_users.count()

    # Staff (superusers)
    staff_users = User.objects.filter(is_staff=True, is_superuser=True)
    staff_users_count = staff_users.count()
    
    #all users
    users = User.objects.all()
    users_count = users.count()
    
    diseases_count=diseases.count()
    medicines_count=medicines.count()
    checkups_count=checkups.count()
    businesslevel_count=businesslevels.count()
    businessplan_count=businessplans.count()
    patient_count=patients.count()
    comment_count=comments.count()
    
    it_officer_rank = get_it_officer_rank(request.user)
    

    # Homepage logs total
    homepage_logs = Log.objects.aggregate(total=Sum('home_page_count'))['total'] or 0

    if request.method == 'POST':
        if 'delete_selected' in request.POST:
            user_ids = request.POST.getlist('selected_users')
            User.objects.filter(id__in=user_ids).delete()
            return redirect('account')

    context = {
        "user": user,
        "users": users,
        "users_count": users_count,
        "userdetail": userdetails,
        "usersdetails": usersdetails,
        "diseases": diseases,
        "medicines":medicines,
        "checkups": checkups,
        "businesslevels": businesslevels,
        "businessplans": businessplans,
        "patients": patients,
        "comments" : comments,
        "diseases_count":diseases_count,
        "medicines_count":medicines_count,
        "checkups_count":checkups_count,
        "businessplan_count":businessplan_count,
        "businesslevel_count":businesslevel_count,
        "patient_count":patient_count,
        "comment_count" : comment_count,
        "homepage_logs": homepage_logs,
        "about_detail":about_detail,
        "staff_users": staff_users,
        "non_staff_users": non_staff_users,
        "active_users_count": active_users_count,
        "non_staff_users_count": non_staff_users_count,
        "staff_users_count": staff_users_count,
        "it_officer_rank" : it_officer_rank,
    }
    return render(request, "account.html", context)


def member_account(request):
    # if Viewer.objects.get(user=request.user) :
    #     viewerdetails=Viewer.objects.get(user=request.user)
    #     context = {
    #         "viewer_detail" : viewerdetails,
    #     }
    #     return render(request, "viewer_account.html", context)

    userdetails = UserDetail.objects.get(user=request.user)
    user = User.objects.get(username=request.user)
    
    context = {
        "user": user,
        "userdetail": userdetails,
    }
    return render(request, "member_account.html", context)

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            request.session['reset_user_id'] = user.id
            messages.success(request, "verification successfully.")
            return redirect('reset_password')
    else:
        form = ForgotPasswordForm()
    return render(request, 'password_forget.html', {'form': form})


def reset_password(request):
    if 'reset_user_id' not in request.session:
        return redirect('forgot_password')
    
    user_id = request.session['reset_user_id']
    user = User.objects.get(id=user_id)
    
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user.password = make_password(new_password)
            user.save()
            del request.session['reset_user_id']
            messages.success(request, "password update successfully.")
            return redirect('login')
    else:
        form = ResetPasswordForm()
    
    return render(request, 'password_reset.html', {'form': form})


#--------- EDIT AND DELETE OBJECTS --------
ALLOWED_RANKS = ["director", "vice_director", "manager", "it_officer"]
def has_edit_permission(user):
    return user.is_superuser or getattr(user, "company_rank", "").lower() in ALLOWED_RANKS

MODEL_MAP = {
    "disease": (Disease, DiseaseForm, "edit_disease.html", "delete_modal.html"),
    "medicine": (Medicine, MedicineForm, "edit_medicine.html", "delete_modal.html"),
    "checkup": (CheckUp, CheckUpForm, "edit_checkup.html", "delete_modal.html"),
    "patient": (PatientForm, PatientModelForm, "edit_patient.html", "delete_modal.html"),
    "businessplan": (BusinessPlan, BusinessPlanForm, "edit_businessplan.html", "delete_modal.html"),
    "businesslevel": (BusinessLevel, BusinessLevelForm, "edit_businesslevel.html", "delete_modal.html"),
    "userdetail": (UserDetail, SuperUserRegistrationForm, "edit_businesslevel.html", "delete_modal.html"),
    "shoptable": (Shop, ShopForm, "edit_shop.html", "delete_modal.html"),
    "branchtable": (Branch, BranchForm, "edit_branch.html", "delete_modal.html"),
    "meetingtable": (Meeting, MeetingForm, "edit_meeting.html", "delete_modal.html"),
    "otheradstable": (Advertisement, AdvertisementForm, "edit_advertisement.html", "delete_modal.html"),
    "abouttable": (About, AboutForm, "edit_about.html", "delete_modal.html"),
    "commenttable": (Comment, CommentForm, "edit_comment.html", "delete_modal.html"),
}

# ---------------------- EDIT OBJECT ----------------------
@login_required
@user_passes_test(has_edit_permission)
def edit_object(request, model, object_id):
    ModelClass, FormClass, template, _ = MODEL_MAP[model]
    instance = get_object_or_404(ModelClass, id=object_id)

    if request.method == "POST":
        form = FormClass(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, f"{model.capitalize()} updated successfully.")
            return JsonResponse({"success": True})
        return JsonResponse({"errors": form.errors}, status=400)

    else:
        form = FormClass(instance=instance)
        html = render_to_string(template, {"form": form, "object": instance, "model": model}, request)
        return HttpResponse(html)

# ---------------------- DELETE OBJECT ----------------------
@login_required
@user_passes_test(has_edit_permission)
def delete_object(request, model, object_id):
    ModelClass, _, _, template = MODEL_MAP[model]
    instance = get_object_or_404(ModelClass, id=object_id)

    if request.method == "POST":
        instance.delete()
        messages.success(request, f"{model.capitalize()} deleted successfully.")
        return JsonResponse({"success": True})

    html = render_to_string(template, {"object": instance, "model": model }, request)
    return HttpResponse(html)



# ---------------------- EDIT OBJECT ----------------------
@login_required
@user_passes_test(has_edit_permission)
def edit_about(request, model, object_id):
    user = request.user
    
    # Get the About object for the logged-in user to access rank
    try:
        about_user = About.objects.get(user=user)
        user_rank = about_user.company_rank
    except About.DoesNotExist:
        user_rank = None  # Fallback if About not found

    # Get model/form/template from mapping
    ModelClass, FormClass, template, _ = MODEL_MAP.get(model, (None, None, None, None))
    if not ModelClass:
        return JsonResponse({"error": "Invalid model"}, status=400)

    # Get instance to edit
    instance = get_object_or_404(ModelClass, id=object_id)

    if request.method == "POST":
        form = FormClass(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, f"{model.capitalize()} updated successfully.")
            return JsonResponse({"success": True})
        # Return form errors if invalid
        return JsonResponse({"errors": form.errors}, status=400)

    # GET request
    form = FormClass(instance=instance)
    html = render_to_string(
        template,
        {
            "form": form,
            "object": instance,
            "model": model,
            "rank": user_rank  # Pass the current user's rank
        },
        request
    )
    return HttpResponse(html)


#start edit my account
@login_required
def edit_myaccount(request):
    user = request.user
    user_detail = get_object_or_404(UserDetail, user=user)

    if request.method == 'POST':
        if user.is_superuser:
            user_form = SuperUserRegistrationForm(request.POST, request.FILES, instance=user)
        else:
            user_form = MemberRegistrationForm(request.POST, request.FILES, instance=user)
        user_detail_form = UserDetailForm(request.POST, request.FILES, instance=user_detail)

        if user_form.is_valid() and user_detail_form.is_valid():
            user = user_form.save(commit=False)

            # Handle password change
            password = user_form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.save()

            # Save details form
            user_detail_form.save()

            # Keep session active
            update_session_auth_hash(request, user)
            messages.success(request, "Your details have been updated successfully.")
            return redirect('/')
        else:
            messages.error(request, "Error updating your details. Please check all fields.")
    else:
        if user.is_superuser:
            user_form = SuperUserRegistrationForm(instance=user)
        else:
            user_form = MemberRegistrationForm(instance=user)
        user_detail_form = UserDetailForm(instance=user_detail)

    context = {
        'user_form': user_form,
        'user_detail_form': user_detail_form,
        'is_superuser': user.is_superuser,
        'password_placeholder': ''
    }

    return render(
        request,
        'edit_superuser.html' if user.is_superuser else 'edit_member.html',
        context
    )


# --------- EDIT AND DELETE USERS --------
ALLOWEDUSEREDIT_RANKS = ["director", "it_officer"]

def has_useredit_permission(user):
    try:
        return user.is_superuser or user.user_detail.company_rank.lower() in ALLOWEDUSEREDIT_RANKS
    except:
        return user.is_superuser

@login_required
@user_passes_test(has_useredit_permission)
def edit_user(request, model, object_id):
    """
    Generic user edit view for superuser or member.
    Works with AJAX modal and supports URL: edit_user/<str:model>/<int:object_id>/
    """
    # For now, we only support editing users
    user = get_object_or_404(User, id=object_id)
    user_detail = get_object_or_404(UserDetail, user=user)

    if request.method == 'POST':
        if user.is_superuser:
            user_form = SuperUserRegistrationForm(request.POST, request.FILES, instance=user)
        else:
            user_form = MemberRegistrationForm(request.POST, request.FILES, instance=user)
        user_detail_form = UserDetailForm(request.POST, request.FILES, instance=user_detail)

        if user_form.is_valid() and user_detail_form.is_valid():
            user_obj = user_form.save(commit=False)
           
            # Handle password change
            new_password = user_form.cleaned_data.get('password')
            if new_password:
                user_obj.set_password(new_password)
            user_obj.save()
           
            # Save UserDetail
            user_detail_form.save()

            # Update session if editing yourself
            if request.user.id == user.id and new_password:
                update_session_auth_hash(request, user_obj)

            messages.success(request, "User details updated successfully.")

            # If AJAX request, return JSON success
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
           
            return HttpResponseRedirect('/')  # redirect after normal POST
        else:
            # AJAX error
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': user_form.errors.as_json()})
            messages.error(request, "Error updating user details. Please check all fields.")
    else:
        # GET request: show modal form
        if user.is_superuser:
            user_form = SuperUserRegistrationForm(instance=user)
        else:
            user_form = MemberRegistrationForm(instance=user)
        user_detail_form = UserDetailForm(instance=user_detail)

        context = {
            'user_form': user_form,
            'user_detail_form': user_detail_form,
            'model': model,
            'object': user,
        }

        return render(request, 'edit_user.html', context)

@login_required
@user_passes_test(has_useredit_permission)
def delete_user(request, model, object_id):
    """
    Generic user delete view.
    Works with AJAX modal and supports URL: delete_user/<str:model>/<int:object_id>/
    """
    user = get_object_or_404(User, id=object_id)

    if request.method == 'POST':
        # Optional: Prevent self-delete
        if request.user.id == user.id:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': "You cannot delete yourself."})
            messages.error(request, "You cannot delete yourself.")
            return HttpResponseRedirect('/')

        user.delete()

        messages.success(request, f"User '{user.username}' has been deleted successfully.")

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})

        return HttpResponseRedirect('/')  # redirect after normal POST

    else:
        # GET request: return modal confirmation
        context = {
            'model': model,
            'object': user,
        }
        return render(request, 'delete_user.html', context)





#start print documents
PRINTMODEL_MAP = {
    "disease": Disease,
    "medicine": Medicine,
    "checkup": CheckUp,
    "patient": PatientModelForm,
    "businesslevel": BusinessLevel,
    "businessplan": BusinessPlan,
    "userdetail": UserDetail,
}

@login_required
def export_generic_details(request, model, format):
    """Generic Export System for CSV, Excel, and PDF"""
    # Restrict by rank (if your UserDetail model has rank field)
    try:
        rank = request.user.user_detail.company_rank
    except Exception:
        rank = None

    if rank not in ['director', 'vice_director', 'manager', 'it_officer']:
        return JsonResponse({'error': 'You do not have permission to export data.'}, status=403)

    # Check model
    if model not in MODEL_MAP:
        return JsonResponse({'error': 'Invalid model.'}, status=400)

    ModelClass = PRINTMODEL_MAP[model]
    objects = ModelClass.objects.all()

    # Extract field names automatically
    field_names = [field.name for field in ModelClass._meta.fields]

    # ================= CSV EXPORT =================
    if format == "csv":
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="{model}_details.csv"'

        writer = csv.writer(response)
        writer.writerow([f.capitalize() for f in field_names])

        for obj in objects:
            row = [getattr(obj, field) for field in field_names]
            writer.writerow(row)

        return response

    # ================= EXCEL EXPORT =================
    elif format == "excel":
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        worksheet = workbook.add_worksheet(model.capitalize())

        # Header row
        for col_num, field in enumerate(field_names):
            worksheet.write(0, col_num, field.capitalize())

        # Data rows
        for row_num, obj in enumerate(objects, start=1):
            for col_num, field in enumerate(field_names):
                worksheet.write(row_num, col_num, str(getattr(obj, field)))

        workbook.close()

        response = HttpResponse(
            output.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f'attachment; filename="{model}_details.xlsx"'
        return response

    # ================= PDF EXPORT =================
    elif format == "pdf":
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{model}_details.pdf"'

        # Use landscape if many columns
        doc = SimpleDocTemplate(response, pagesize=landscape(letter),
                                leftMargin=0.5*inch, rightMargin=0.5*inch,
                                topMargin=0.5*inch, bottomMargin=0.5*inch)

        elements = []

        # Styles
        styles = getSampleStyleSheet()
        styleN = ParagraphStyle(
            'NormalWrap',
            parent=styles['Normal'],
            fontSize=9,
            leading=11,
            alignment=0,   # Left alignment
        )

        # Headers
        headers = [Paragraph(f"<b>{f.capitalize()}</b>", styleN) for f in field_names]
        data = [headers]

        # Data rows
        for obj in objects:
            row = [Paragraph(str(getattr(obj, field)) or "", styleN) for field in field_names]
            data.append(row)

        # Column widths (fit page)
        page_width = landscape(letter)[0] - doc.leftMargin - doc.rightMargin
        num_cols = len(field_names)
        col_widths = [page_width / num_cols for _ in range(num_cols)]

        table = Table(data, colWidths=col_widths, repeatRows=1, hAlign='LEFT')

        # Table style
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f17c90")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Left align content
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Top align
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#f8f8f8")),
        ]))

        elements.append(table)
        doc.build(elements)
        return response

    else:
        return JsonResponse({'error': 'Invalid export format.'}, status=400)








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