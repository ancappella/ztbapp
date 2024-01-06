from django.contrib import admin

# Register your models here.

from api.models import BidInfo, ProjectList


admin.site.register(BidInfo)
admin.site.register(ProjectList)