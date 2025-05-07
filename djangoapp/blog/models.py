from django.db import models
from utils.rands import slugify_new
from django.contrib.auth.models import User

# Create your models here.

# MODEL TAGS
class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    name = models.CharField(max_length=255)
    # Tipo um id 
    slug = models.SlugField(
        unique=True, default=None,
        null= True, blank=True, max_length=255,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name, 4)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


# MODEL CATEGORY
class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True, default=None,
        null=True, blank=True, max_length=255,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name, 4)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


# MODEL PAGE
class Page(models.Model):
    title = models.CharField(max_length=65,)
    slug = models.SlugField(
        unique=True, default="",
        null=True, blank=True, max_length=255,
    )
    is_published = models.BooleanField(default=False)
    content = models.TextField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title, 4)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

# MODEL POST
class Post(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    title = models.CharField(max_length=65)
    slug = models.SlugField(unique=True, default="", null=True, blank=True, max_length=255,)
    excerpt = models.CharField(max_length=150)
    is_published = models.BooleanField(default=False )
    content = models.TextField()
    cover = models.ImageField(upload_to= 'date/web/media/%Y/%m', blank=True, default='')
    cover_in_post_content = models.BooleanField( default=True, help_text='Se marcado, exibirá a capa dentro do post')

    created_at = models.DateTimeField(auto_now_add= True)
    # user.post_set.all() -> query set
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        blank=True, null=True, related_name='post_created_by'
    )
    updated_at = models.DateTimeField(auto_now=True)
    # user.post_set.all() -> query set
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        blank=True, null=True, related_name='post_updated_by'
    )
    category = models.ForeignKey( Category, on_delete=models.SET_NULL , null=True, blank=True, ) 
    tags = models.ManyToManyField(Tag, blank=True, default='')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title, 4)
        return super().save(*args, **kwargs)
    
    
    