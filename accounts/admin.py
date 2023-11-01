from django.contrib import admin
from .models import CustomUser, Account, JoinClubForm

# Register your models here.
admin.site.register(Account)
admin.site.register(CustomUser)
admin.site.register(JoinClubForm)
