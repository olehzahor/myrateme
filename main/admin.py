from django.contrib import admin
from main.models import Mark, Profile, MarkAdmin

admin.site.register(Mark, MarkAdmin)
admin.site.register(Profile)