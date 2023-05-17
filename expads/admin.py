from django.contrib import admin

from .models import Category,Expatad,ExpatImage,Countrycode,CityCode,LocationCode,SubLocationCode,Purpose,Contactme,Interested


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')
admin.site.register(Category, CategoryAdmin)



class ExpatadAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'countrycode','citycode','purpose', 'locationcode','sublocationcode','area','areameasurement', 'landmark','contactno','zipcode', 'price','Description','is_active','cover_photo')
admin.site.register(Expatad, ExpatadAdmin)


class ExpatImageAdmin(admin.ModelAdmin):
    list_display = ('expatads', 'images')
admin.site.register(ExpatImage, ExpatImageAdmin)

class ContactmeAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'contactno','email','Description','is_fallowed')
admin.site.register(Contactme, ContactmeAdmin)

class InterestedAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'contactno','email','Description','is_fallowed')
admin.site.register(Interested, InterestedAdmin)


admin.site.register(Countrycode)
admin.site.register(Purpose)
admin.site.register(CityCode)
admin.site.register(LocationCode)
admin.site.register(SubLocationCode)
