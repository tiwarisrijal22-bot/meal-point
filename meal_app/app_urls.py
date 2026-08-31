from django.contrib import  admin
from django.urls import path
from.import views
urlpatterns = [
   path("",views.home,name="home_page"),
     path("about_us/",views.about_us,name="aboutpage"),
     path("contact_us/",views.contact_us,name="contactpage"),
     path("customer_feedback/",views.customer_feedback,name="feedbackpage"),
     path("customer_login/",views.customer_login,name="loginpage"),
     path("customer_registration/", views.customer_registration, name="registrationpage"),
     path("customer_home/",views.customer_home,name="homepage"),
     path("edit_profile/", views.edit_profile, name="edit_profile"),
     path("manager_login/",views.manager_login,name="managerloginpage"),
     path("manager_detail/",views.manager_detail,name="managerdetailpage"),
     path("manager_home/",views.manager_home,name="managerhomepage"),
     path("customer_logout/",views.customer_logout,name="customer_logout_page"),
     path("manager_logout/",views.manager_logout,name="manager_logout_page"),
     path("weekly_meal_schedule/", views.weekly_meal_schedule, name="schedulepage"),
     path("all_review/",views.all_review,name="reviewpage"),
     path("food/",views.food,name="foodpage"),
     path('purchase_plan/<int:id>/', views.purchase_plan, name="purchase_plan"),
     path("make_payment/", views.make_payement, name="make_payment"),
     path("mybooking_status/", views.mybooking_status, name="mybooking_status_page"),
     path("all_booking/", views.all_bookings, name="all_booking_page"),
     path("faq/", views.faq, name="faqpage"),
     path('ai_assistant/',views.ai_assistant,name="ai_assistant_page"),
     path('api/ai-chat/',views.ai_chat,name="ai_chat_page"),  
]
