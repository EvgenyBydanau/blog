from django.contrib import admin
from .models import Country, Comment, UserPhone, City
from accounts.models import User


class CountryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Country, CountryAdmin)


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)


class CommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Comment, CommentAdmin)


class UserPhoneAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserPhone, UserPhoneAdmin)


class CityAdmin(admin.ModelAdmin):
    pass


admin.site.register(City, CityAdmin)