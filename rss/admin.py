from datetime import datetime, timezone, timedelta

from django.contrib import admin

from .models import Feed


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = ('display_title', 'author', 'published_date')
    list_filter = ('published_date',)
    ordering = ('-published_date',)

    def display_title(self, obj):
        '''
        Customized title with highlight.
        '''
        feed_timedelta = datetime.now(timezone.utc) - obj.published_date
        result_str = '{}'
        if feed_timedelta >= timedelta(days=1):
            result_str = '<span style="color: red">{}</span>'
        return result_str.format(obj.title)
    display_title.short_description = 'Title'
    display_title.allow_tags = True
