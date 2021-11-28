from django.contrib import admin
from .models import Plan, UserProfile, Subscription

admin.site.register(UserProfile)
admin.site.register(Plan)
admin.site.register(Subscription)