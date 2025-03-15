from django.contrib import admin
from .models import Books, Category 


admin.site.register(Books)
class BooksAdmin(admin.ModelAdmin):
    fields = "__all__"


admin.site.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = "__all__"