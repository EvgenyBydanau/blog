from django.contrib import admin
from .models import Country
from accounts.models import User


class CountryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Country, CountryAdmin)


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)