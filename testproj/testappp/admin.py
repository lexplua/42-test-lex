from django.contrib import admin
from testproj.testappp.models import BioModel, RequestModel, DBLogRecord


class BioModelAdmin(admin.ModelAdmin):
    pass


class RequestModelAdmin(admin.ModelAdmin):
    list_display = ('priority', 'body')


class DBLogRecordAdmin(admin.ModelAdmin):
    pass

admin.site.register(BioModel, BioModelAdmin)
admin.site.register(RequestModel, RequestModelAdmin)
admin.site.register(DBLogRecord, DBLogRecordAdmin)
