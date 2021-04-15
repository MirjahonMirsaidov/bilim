from django.contrib import admin
from .models import *

# Register your models here.


from rest_framework.authtoken.admin import TokenAdmin
TokenAdmin.raw_id_fields = ['user']

admin.site.register(Subject)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Help)
admin.site.register(Thank)


