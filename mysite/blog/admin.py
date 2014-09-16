from django.contrib import admin
from blog.models import blog

# Register your models here.
class blogAdmin(admin.ModelAdmin):
    list_display=('subject','author','content','post_time')
    search_fields = ('subject', 'author','content')
    list_filter=('post_time',)
    ordering = ('-post_time',)
admin.site.register(blog,blogAdmin)
