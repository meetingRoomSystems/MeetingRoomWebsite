from django.contrib import admin
from .models import UserInfo

# admin customization
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['username','fullname','loggedIn','role']

admin.site.register(UserInfo,UserInfoAdmin)
