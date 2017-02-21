from django.contrib import admin

from .models import Feed


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    list_filter = ('published_date',)
    ordering = ('-published_date',)
