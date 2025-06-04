from django.contrib import admin
from .models import *
from django.contrib.admin import ModelAdmin

# Register your models here.
admin.site.site_header = "Sanyu Hospital Admin"
admin.site.site_title = "Sanyu Hospital Admin Portal"

admin.site.index_title = "Welcome to the Sanyu Hospital Admin Portal"
admin.site.register(MedicalOutreach, ModelAdmin)
admin.site.register(news, ModelAdmin)
admin.site.register(services, ModelAdmin)
admin.site.register(Donor, ModelAdmin)
admin.site.register(Doctor, ModelAdmin)
admin.site.register(BankDs, ModelAdmin)
# admin.site.register(Calls, ModelAdmin)
# admin.site.register(BookEventInvitation, ModelAdmin)
# admin.site.register(CallRequest, ModelAdmin)
# admin.site.register(Donation, ModelAdmin)           
# admin.site.register(Volunteer, ModelAdmin)
# admin.site.register(VolunteerRequest, ModelAdmin)
# admin.site.register(VolunteerInvitation, ModelAdmin)
admin.site.register(Service)


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    prepopulated_fields = {"slug": ("title",)}


    from django.contrib import admin
from .models import Slide, Speciality

admin.site.register(Slide)
admin.site.register(Speciality)
admin.site.register(Event)
admin.site.register(Payments)
admin.site.register(Departments)