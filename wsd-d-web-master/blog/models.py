from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class RawFromApi(models.Model):
    article_id = models.CharField(unique=True, max_length=50, blank=True, null=True)
    title = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    likes_count = models.IntegerField(blank=True, null=True)
    comments_count = models.IntegerField(blank=True, null=True)
    tags_str = models.CharField(max_length=100, blank=True, null=True)
    user_id = models.CharField(max_length=50, blank=True, null=True)
    user_permanent_id = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
    html = models.TextField(blank=True, null=True)
    tokens = models.TextField(blank=True, null=True)
    similar_articles = models.TextField(blank=True, null=True)
    topic_id = models.IntegerField(blank=True, null=True)
    similar_articles_vec60 = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'raw_from_api'


class ArticleVector(models.Model):
    article_id = models.CharField(unique=True, max_length=50, blank=True, null=True)
    vector = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'article_vector'

class ArticleSimilarArticles(models.Model):
    article_id = models.CharField(max_length=50, blank=True, null=True)
    similar_article_id = models.CharField(max_length=50, blank=True, null=True)
    distance = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'article_similar_articles'


