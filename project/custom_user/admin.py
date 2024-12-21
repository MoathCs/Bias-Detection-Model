from django.contrib import admin
from django_use_email_as_username.admin import BaseUserAdmin

from .models import User

from .models import Question

from .models import History



admin.site.register(User, BaseUserAdmin)

admin.site.register(Question)

admin.site.register(History)





