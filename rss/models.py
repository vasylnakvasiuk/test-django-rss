from django.db import models


class FeedSource(models.Model):
    '''
    Source model for RSS feeds.
    '''
    url = models.URLField()

    def __str__(self):
        return self.url


class Feed(models.Model):
    '''
    Feed model.
    '''
    feed_id = models.CharField(max_length=300)
    source = models.ForeignKey(FeedSource, related_name='feeds')
    title = models.CharField(max_length=30)
    author = models.CharField(max_length=100)
    summary = models.TextField(blank=True)
    published_date = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('feed_id', 'source')

    def __str__(self):
        return self.title
