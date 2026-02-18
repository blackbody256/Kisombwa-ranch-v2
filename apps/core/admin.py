from django.contrib import admin

from .models import Ranch, Staff, SyncQueue, User

admin.site.register(User)
admin.site.register(Ranch)
admin.site.register(Staff)
admin.site.register(SyncQueue)
