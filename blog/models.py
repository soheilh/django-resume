from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField

# Model for Category
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

# Model for Post
class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=False, blank=False)
    # author = 
    slug = models.SlugField(max_length=120, unique=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField(to=Category, related_name="posts")
    thumb = models.ImageField(upload_to ='thumbs', default='thumbs/default.jpg')
    image = models.ImageField(upload_to ='images', default='images/default.jpg')
    STATUS_CHOICES = [
        ('d', 'Draft'),
        ('p', 'Published'),
        ('a', 'Archived'),
        ('pa', 'Pending Approval'),
        ('d', 'Deleted'),
    ]
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='p')
    content = RichTextField(default='')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publish']

