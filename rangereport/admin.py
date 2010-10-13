from django.contrib import admin
from rangedogs.rangereport.models import *
from django.contrib.auth.models import User

admin.site.register(UserProfile)
admin.site.register(Gun)
admin.site.register(Caliber)
admin.site.register(Handload)
admin.site.register(Report)
admin.site.register(GunReport)
admin.site.register(Comment)
