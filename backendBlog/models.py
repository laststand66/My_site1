from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


from django.dispatch import Signal



class MainUser(AbstractUser):
    can_delete_other_comments = models.BooleanField(default=False, db_index=True, verbose_name='Can delete all users coments?')
    about_me = models.CharField(max_length=255, blank=True, null=True)
    displayed_email = models.CharField(max_length=50, blank=True, null=True)

    class Meta(AbstractUser.Meta):
        pass


class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title

STATUS = (
    (0, 'Draft'),
    (1, 'Publish')
)

class Article(models.Model):
    title = models.CharField(max_length=255, unique = True, verbose_name='article title')
    slug = models.SlugField(max_length=255, unique=True, default='Some_string')
    overview = models.TextField(blank=False, verbose_name='article preview on frontpage')
    content = models.TextField(blank=False, verbose_name='article main text')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='date published')
    thumbnail = models.ImageField(blank=True, upload_to='thumbnails')
    status = models.IntegerField(choices=STATUS, default=0)
    categories = models.ManyToManyField(Category, blank=True, related_name='articles')
    likes = models.ManyToManyField(MainUser, related_name='likes', blank=True)
    favorite = models.ManyToManyField(MainUser, related_name='favorited', blank=True)


    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()




user_registrated = Signal(providing_args=['instance'])

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    name = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
