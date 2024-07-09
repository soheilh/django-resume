from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError

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
    visible = models.BooleanField(default=True)
    visit_count = models.IntegerField(default=0)
    content = RichTextField(default='')

    def __str__(self):
        return f"{ self.title} | { self.catagories} | { self.status}"

    class Meta:
        ordering = ['-publish']

# Model for Comment
class Comment(models.Model):
    email = models.EmailField(max_length=255)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name="replies", null=True, blank=True)
    depth = models.PositiveIntegerField(default=0)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    COMMENT_STATUS = (
        ('w', 'Waiting'),
        ('a', 'Accepted'),
        ('r', 'Rejected'),
    )
    status = models.CharField(max_length=1, choices=COMMENT_STATUS, default='a')

    def validate_depth(self):
        if self.depth is not None and self.depth >= 3:
            raise ValidationError("Maximum depth of comments reached.")

    def __str__(self):
        return self.body[0:50]
    
    # Override the save method to perform validation before saving
    def save(self, *args, **kwargs):
        self.validate_depth()
        super().save(*args, **kwargs)
