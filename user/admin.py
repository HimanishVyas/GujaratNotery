from django.contrib import admin
from user.models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(District)
admin.site.register(MemberShip)
admin.site.register(Logs)