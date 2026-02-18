from django.contrib import admin

from .models import HerdCount, MovementLog, RFIDScanLog

admin.site.register(HerdCount)
admin.site.register(MovementLog)
admin.site.register(RFIDScanLog)
