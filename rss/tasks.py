import ssl
import logging

import feedparser
from dateutil.parser import parse
from celery import shared_task
from django.core.exceptions import ValidationError

from .models import Feed, FeedSource


def _save_feeds(raw_feed, feed_source):
    '''
    Helper to create feed in database.
    '''
    get_params = dict(
        feed_id=raw_feed['id'],
        source=feed_source
    )
    update_params = dict(
        title=raw_feed['title'],
        author=raw_feed['author'],
        summary=raw_feed['summary'],
        published_date=parse(raw_feed['published'])
    )

    created = False
    try:
        # Do nothing, if feed is already exists.
        feed = Feed.objects.get(**get_params)
    except Feed.DoesNotExist:
        feed = Feed(**get_params, **update_params)
        try:
            feed.full_clean()
        except ValidationError as e:
            logging.warning('Feed has title with large length.')
            for msg in e.messages:
                logging.warning(msg)
        else:
            feed.save()
            created = True
    return created


@shared_task(ignore_result=True)
def rss_parser(source_url):
    # TODO: Hack to easly strip ssl. Fix that later.
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context

    feed_source, _ = FeedSource.objects.get_or_create(url=source_url)
    feeds = feedparser.parse(source_url)
    count = 0
    for raw_feed in feeds['entries'][10:]:
        count += _save_feeds(raw_feed, feed_source)
    logging.info('Successfully saved to DB {} feeds.'.format(count))
