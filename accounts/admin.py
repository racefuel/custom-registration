from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile

# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "date_joined",
        "is_admin",
        "is_staff",
    )
    search_fields = ("email", "first_name", "last_name")  #
    readonly_fields = ("date_joined", "last_login")

    filter_horizontal = ()
    list_filter = ()
    fieldsets = []
    fields = ()
    add_fieldsets = ((None, {"fields": ("email", "password1", "password2")}),)
    ordering = ("email",)


admin.site.register(User, AccountAdmin)
admin.site.register(Profile)
