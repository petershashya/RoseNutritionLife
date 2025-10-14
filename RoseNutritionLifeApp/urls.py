from django.urls import path
from .views import (
    home ,comment , services ,advertisment ,analysis ,account ,  
    
    #post function
    post_disease,post_medicine, post_checkup ,
    post_businessplan, post_businesslevel,post_patient,
    post_patient, post_checkup_sales, post_medicine_sales ,post_advertisement ,
    
    #auth function
    login ,register ,login_view, logout_view,
)

urlpatterns = [
    path('', home, name='home'),
    path('comment/', comment, name='comment'),
    path('services/', services, name='services'),
    path('advertisment/', advertisment, name='advertisment'),
    path('analysis/', analysis, name='analysis'),
    path('account/', account, name='account'),
    
    path('post_disease/', post_disease, name='post_disease'),
    path('post_medicine/', post_medicine, name='post_medicine'),
    path('post_checkup/', post_checkup, name='post_checkup'),
    path('post_businessplan/', post_businessplan, name='post_businessplan'),
    path('post_businesslevel/', post_businesslevel, name='post_businesslevel'),
    path('post_advertisement/', post_advertisement, name='post_advertisement'),
    path('post_patient/', post_patient , name='post_patient'),
    path('post_checkup_sales/', post_checkup_sales, name='post_checkup_sales'),
    path('post_medicine_sales/', post_medicine_sales, name='post_medicine_sales'),
    
    # # Auth
    path('register/', register, name='register'),
    path('register_admin/', register, name='register_admin'),
    path('register_member/', register, name='register_member'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
