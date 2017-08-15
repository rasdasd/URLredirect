from django.contrib import admin
from smallurl.models import HashedURL, Redirect

# Register your models here.
admin.site.register(HashedURL)
admin.site.register(Redirect)
