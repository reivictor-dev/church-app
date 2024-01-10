from django.db import models
from stdimage.models import StdImageField
from django.contrib.auth.models import User
from django.db.models import signals
from django.template.defaultfilters import slugify
# Create your models here.


class Base(models.Model):
    created = models.DateField('Data de criação', auto_now=True)
    updated = models.DateField('Data de atualização', auto_now=True)

    class Meta:
        abstract = True


# Extends BASE with createdAt and updatedAt. If a need to pick up it later I can.
class Posts(Base):
    user_post = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True)
    title = models.CharField('title', max_length=40, blank=False)
    body_post = models.CharField('body_post', max_length=200, blank=False)
    image = StdImageField(upload_to='post_image',
                          variations={'thumb': (200, 200)}, blank=True)
    link = models.CharField('link', max_length=300, blank=True)
    slug = models.SlugField('Slug', max_length=100, blank=True, editable=False)

    def __str__(self):
        return self.title

    @property
    def get_username(self):
        return self.user_post.username


def posts_pre_save(signal, instance, sender, **kwargs):
    instance.slug = slugify(instance.title)


signals.pre_save.connect(posts_pre_save, sender=Posts)
