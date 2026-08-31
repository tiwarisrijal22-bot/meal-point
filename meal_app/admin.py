from django.contrib import admin

# Register your models here.
from .models import Feedback, Contact, CustomerDetail,ManagerDetail,MealPlan,Payment,UpiDetail
class FeedbackAdmin(admin.ModelAdmin):
    list_display=["name","email","rating","review","date"]
class ContactAdmin(admin.ModelAdmin):
    list_display=["name","email","phone","question","contact_date"]
class CustomerDetailAdmin(admin.ModelAdmin):
    list_display=["name","email","phone","profile_pic"]
class ManagerDetailAdmin(admin.ModelAdmin):
    list_display=["name","email","phone","city","address","profile_pic",]
class MealPlanAdmin(admin.ModelAdmin):
    list_display=["plan_name","meals_included","duration","cost","plan_image",]
class PaymentAdmin(admin.ModelAdmin):
    list_display=["customer","plan","amount","booking_date","payment_status","transaction_id",]
class UpiDetailAdmin(admin.ModelAdmin):
    list_display = ["upiid"]
admin.site.register(Feedback,FeedbackAdmin)
admin.site.register(Contact,ContactAdmin)
admin.site.register(CustomerDetail,CustomerDetailAdmin)
admin.site.register(ManagerDetail,ManagerDetailAdmin)
admin.site.register(MealPlan,MealPlanAdmin)
admin.site.register(Payment,PaymentAdmin)
admin.site.register(UpiDetail, UpiDetailAdmin)

###customizing admin panel code##
admin.site.site_header="Meal Point admin login panel"
admin.site.site_title="Meal Point admin Dash Board"
admin.site.site_title="welcome to Meal Point portal"
admin.site.index_title="Meal Point admin dashboard"

