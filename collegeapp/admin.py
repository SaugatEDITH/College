from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Appointment)
admin.site.register(Ourteam)
admin.site.register(Gallery)
admin.site.register(ApplyOnline)
admin.site.register(Contact)
admin.site.register(FAQ)
# !For Blog
class BlogAdmin(admin.ModelAdmin):
    exclude = ('slug',)

admin.site.register(Blog, BlogAdmin)

# !For notice
class NoticeAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    
admin.site.register(Notice, NoticeAdmin)

@admin.register(CountdownTimer)
class CountdownTimerAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'end_time')
    
@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'file', 'uploaded_at')
    search_fields = ('title',)