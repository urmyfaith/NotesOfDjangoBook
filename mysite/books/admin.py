from django.contrib import admin
from books.models import Author,Publisher,Book

# Register your models here.

admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(Book)
