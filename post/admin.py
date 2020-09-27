from django.contrib import admin
from .models import Post,Image
# Register your models here.


class ImageInline(admin.TabularInline):
    model = Image

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [ImageInline]

    class Meta:
        model = Post
