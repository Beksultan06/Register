from django.contrib import admin
from apps.users.models import User, SessionAuth

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username']

admin.site.register(SessionAuth) 