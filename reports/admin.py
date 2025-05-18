from django.contrib import admin
from .models import Report, Category, Comments, District

admin.site.register(Report)
admin.site.register(Category)
admin.site.register(Comments)
admin.site.register(District)

# Register your models here.
