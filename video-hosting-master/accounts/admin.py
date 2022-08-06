from django.contrib import admin
from .models import ProfileData


class ProfileAdminUser(admin.ModelAdmin):
    list_display = ['username', 'telephone']
    list_display_links = ('username', )
    list_filter = ('username__username', 'username__email',)  # добавляем примитивные фильтры в нашу админку
    search_fields = ('username__username', 'username__email', 'telephone',)  # тут всё очень похоже на фильтры из запросов в базу


admin.site.register(ProfileData, ProfileAdminUser)
