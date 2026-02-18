from django.contrib import admin

from .models import Mortality, Treatment, Vaccination

admin.site.register(Vaccination)
admin.site.register(Treatment)
admin.site.register(Mortality)
