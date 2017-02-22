from datetime import datetime, timezone, timedelta

from django.contrib import admin, messages

from .models import Feed, FeedSource
from .tasks import rss_parser


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = ('display_title', 'author', 'published_date')
    list_filter = ('published_date', 'source')
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


@admin.register(FeedSource)
class FeedSourceAdmin(admin.ModelAdmin):
    list_display = ('url', )
    actions = ['run_rss_parser']

    def run_rss_parser(self, request, queryset):
        '''
        Action to parse feed source by celery task.
        '''
        for feed_source in queryset:
            rss_parser.delay(feed_source.url)

            self.message_user(
                request,
                'Feed source "{}" has successfully started to parse.'.format(
                    feed_source
                ),
                level=messages.SUCCESS
            )
    run_rss_parser.short_description = 'Parse selected feed sources'
