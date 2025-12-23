from django.urls import path
from .views import (
    home ,services ,reception ,doctor, pharmacy, advertisement,analysis ,payment,account ,
    member_account,memberdetail,
    
    #post function
    post_disease,post_medicine, post_checkup ,
    post_businessplan, post_businesslevel,post_patient,
    post_patient, post_checkup_sales, post_medicine_sales ,post_advertisement ,
    post_shop,post_branch,post_meeting, post_about,edit_about, post_medicine_sales,
    
    #medical
    medical_form,view_medical,print_medical,ajax_patient_search,ajax_medical_search,ajax_pharmacy_search,
    
    #medical payments
    view_medicalpayment,toggle_medical_payment,view_member_payment,print_member_payment,view_medicine_form,
    
    #members and payments
    view_member_pending , save_member_payment, ajax_payment_search,ajax_pending_search,ajax_user_search,calculate_money,
    
    #for templates
    posture_details, video_details,lists_details,list_details,business_details,
    advertisement_details,advertisement_tables,
    
    #auth function
    login ,register ,login_view, logout_view,forgot_password,reset_password,
    
    #edit and delete tables
    edit_object,delete_object,
    edit_user,
    delete_user, edit_myaccount,
    
    #post and delete comment
    post_modelcomment, delete_modelcomment,
    
    #leave comments
    post_comment, delete_comment,
    
    #confirm and unconfirm comment
    confirm_comment,unconfirm_comment,show_confirm_comment_modal,
    
    #print for excel, csv and pdf
    export_generic_details,
    
    show_chart,print_chart_pdf,
    
    sharedcontent_details,
)

urlpatterns = [
    path('', home, name='home'),
    path('services/', services, name='services'),
    path('reception/', reception, name='reception'),
    path('doctor/', doctor, name='doctor'),
    path('pharmacy/', pharmacy, name='pharmacy'),
    path('advertisement/', advertisement, name='advertisement'),
    path('analysis/', analysis, name='analysis'),
    path('payment/', payment, name='payment'),
    path('account/', account, name='account'),
    path('memberdetail/', memberdetail, name='memberdetail'),
    path('member_account/', member_account, name='member_account'),
    
    #medical
    path('medical_form/<int:patient_id>/', medical_form, name='medical_form'),
    path('view_medical/<int:medical_id>/', view_medical, name='view_medical'),
    path('print-medical/<int:medical_id>/', print_medical, name='print_medical'),
    path('view-medicine/<str:medical_id>/', view_medicine_form, name='view_medicine_form'),
    path('ajax/patient-search/', ajax_patient_search, name='ajax_patient_search'),
    path('ajax/medical-search/', ajax_medical_search, name='ajax_medical_search'),
    path('ajax/pharmacy-search/', ajax_pharmacy_search, name='ajax_pharmacy_search'),
    path( 'ajax/user-search/', ajax_user_search, name='ajax_user_search'),

    
    #medical payments
    path("payment/medical/<int:medical_id>/", view_medicalpayment, name="view_medicalpayment"),
    path('ajax/toggle-medical-payment/<int:product_id>/', toggle_medical_payment, name='toggle_medical_payment'),
    
    #show and save members and payemnts
    path("payment/", payment, name="payment"),
    path("payment/member/<str:membership_no>/", view_member_pending, name="view_member_pending"),
    path("calculate_money/", calculate_money, name="calculate_money"),
    path("payment/member_payment/<str:membership_no>/", view_member_payment, name="view_member_payment"),
    path('print-member-payment/<str:membership_no>/', print_member_payment, name='print_member_payment'), 
    path("payment/save/", save_member_payment, name="save_member_payment"),
    path('ajax/payment_-search/', ajax_payment_search, name='ajax_payment__search'),
    path('ajax/pending_-search/', ajax_pending_search, name='ajax_pending__search'),
 
    #for posts models details
    path('post_disease/', post_disease, name='post_disease'),
    path('post_medicine/', post_medicine, name='post_medicine'),
    path('post_checkup/', post_checkup, name='post_checkup'),
    path('post_businessplan/', post_businessplan, name='post_businessplan'),
    path('post_businesslevel/', post_businesslevel, name='post_businesslevel'),
    path('post_advertisement/', post_advertisement, name='post_advertisement'),
    path('post_shop/', post_shop, name='post_shop'),
    path('post_meeting/', post_meeting, name='post_meeting'),
    path('post_branch/', post_branch, name='post_branch'),
    
    path('post_about/',post_about, name='post_about'),
    path('edit_about/<str:model>/<int:object_id>/', edit_about, name='edit_about'),

    #for posts sales models
    path('post_patient/', post_patient , name='post_patient'),
    path('post_checkup_sales/', post_checkup_sales, name='post_checkup_sales'),
    path('post_medicine_sales/', post_medicine_sales, name='post_medicine_sales'),
    
    #for templates modals
    path('ajax/posture-details/<str:model_type>/<int:item_id>/', posture_details, name='posture_details'),
    path('ajax/video-details/<str:model_type>/<int:item_id>/', video_details, name='video_details'),
    path('ajax/lists-details/<str:model_type>/', lists_details, name='lists_details'),
    path('ajax/list-details/<str:model_type>/<int:item_id>/', list_details, name='list_details'),
    path('ajax/business-details/<str:model_type>/<int:item_id>/', business_details, name='business_details'),
    path('ajax/advertisement-details/<str:model_type>/', advertisement_details, name='advertisement_details'),
    path('ajax/advertisement-tables/<str:model_type>/', advertisement_tables, name='advertisement_tables'),
    
    # # Auth
    path('register_viewer/', register, name='register_viewer'),
    path('register_admin/', register, name='register_admin'),
    path('register_member/', register, name='register_member'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('edit/', edit_myaccount, name='edit_user_details'),
    
    #forgot and reset passwords
    path('login/forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/', reset_password, name='reset_password'),
    
    #edit and delete tables
    path('edit/<str:model>/<int:object_id>/', edit_object, name='generic_edit'),
    path('delete/<str:model>/<int:object_id>/', delete_object, name='generic_delete'),
    path('edit_user/<str:model>/<int:object_id>/', edit_user, name='edit_user'),
    path('delete_user/<str:model>/<int:object_id>/', delete_user, name='delete_user'),
    
    #models comments section
    path('generic_postcomment/<str:model>/<int:object_id>/', post_modelcomment, name='generic_postcomment'),
    path('generic_deletecomment/<str:model>/<int:object_id>/', delete_modelcomment, name='generic_deletecomment'),
    
    #post comments
    path("post_comment/<str:model>/", post_comment, name="post_comment"),
    path('delete_comment/<str:model>/<int:object_id>/', delete_comment, name='delete_comment'),
      

    path('show-confirm-modal/', show_confirm_comment_modal, name='show-confirm-modal'),
    path('confirm-item/', confirm_comment, name='confirm-item'),
    path('unconfirm-item/', unconfirm_comment, name='unconfirm-item'),


    #prints csv,excel and pdf
    path('export/<str:model>/<str:format>/', export_generic_details, name='export_generic_details'),
    
    path('ajax/show_chart/<str:type>/', show_chart, name='show_chart'),
    
    path('print_chart_pdf/', print_chart_pdf, name='print_chart_pdf'),
    
    path('sharedcontent/<str:model_type>/<int:item_id>/<int:user_id>/', sharedcontent_details, name='shared_details'),
        
]
