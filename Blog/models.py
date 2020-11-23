from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(
        verbose_name="Slug",
        allow_unicode=True,
        unique=True, default="")

    def save(self, *args, **kwargs):
        if not self.slug: self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    # The related_name attribute allows us to name the attribute that we use for the relation from the related object
    # back to this one we have a Foreign key relation that establishes a many-to-one relationship with the Post
    # model, since every comment will be made on a post and each post will have multiple comments.

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
