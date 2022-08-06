from django.contrib import admin
from .models import Media, MediaRating


class MediaAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'author', 'date_posted', 'current_rating']
    list_display_links = ('pk', 'title',)
    list_filter = ('title', 'author__username', 'date_posted')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('title', 'author__username')  # тут всё очень похоже на фильтры из запросов в базу


admin.site.register(Media, MediaAdmin)
admin.site.register(MediaRating)
