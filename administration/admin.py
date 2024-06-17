from django.contrib import admin
from administration import models
from import_export.admin import ImportExportModelAdmin
# Register your models here.
admin.site.register(models.profile)
admin.site.register(models.doctor, ImportExportModelAdmin)
admin.site.register(models.camp_details, ImportExportModelAdmin)
admin.site.register(models.camp_services, ImportExportModelAdmin)
admin.site.register(models.appointment, ImportExportModelAdmin)