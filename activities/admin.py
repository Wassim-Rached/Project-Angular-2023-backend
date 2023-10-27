from django.contrib import admin
from .models import Activity,ActivityCategory,Category,ActivityLike,ActivityRegistration

# Register your models here.
admin.site.register(Activity)
admin.site.register(Category)

admin.site.register(ActivityRegistration)
admin.site.register(ActivityLike)
admin.site.register(ActivityCategory)
