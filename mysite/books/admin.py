from django.contrib import admin
from books.models import Author,Publisher,Book

# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    list_display=('first_name','last_name','email')


admin.site.register(Publisher)
admin.site.register(Author,AuthorAdmin)
admin.site.register(Book)
