from django.contrib import admin
from .models import User, UserProfile,Contactus
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'role', 'is_active')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class ContactusAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'mobileno','email','purpose','is_active','created_at','modified_at')
admin.site.register(Contactus, ContactusAdmin)


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)
