from django.contrib import admin
from testproj.testappp.models import BioModel


class BioModelAdmin(admin.ModelAdmin):
    pass

admin.site.register(BioModel,BioModelAdmin)