from django.contrib import admin
from .models import PostModel,Comments




class PostModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_created', 'image')
    



admin.site.register(PostModel, PostModelAdmin)
admin.site.register(Comments)