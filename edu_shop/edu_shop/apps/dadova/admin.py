# complete
from django.contrib import admin
from .models import *


admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Review)
admin.site.register(Type)
admin.site.register(Event)
admin.site.register(Cart)
admin.site.register(Balance)
admin.site.register(BoughtedCourse)