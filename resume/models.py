from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.validators import RegexValidator
from django.utils.html import strip_tags
import html
from ckeditor.fields import RichTextField

# Bio models
class Bio(models.Model):
    text = RichTextField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.get_bio_snippet()
    
    def get_bio_snippet(self):
        return (html.unescape(strip_tags(self.text))[:50] + '...') if len(self.text)>50 else html.unescape(strip_tags(self.text))

# Institution model
class Institution(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Advisor models
class Advisor(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

# Education model
class Education(models.Model):
    institution = models.ForeignKey(Institution, related_name='educations', on_delete=models.DO_NOTHING, blank=True, null=True)
    major = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    gpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    gpa_base = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    advisors = models.ManyToManyField(Advisor, related_name='educations', blank=True)
    thesis = models.CharField(max_length=255, blank=True)
    thesis_score = models.CharField(max_length=4, blank=True)
    DEGREE_CHOICES = [
        ('DIP', 'Diploma'),
        ('BD', 'B.Sc.'),
        ('MD', 'M.Sc.'),
        ('PHD', 'Ph.D.'),
        ('POSTDOC', 'Postdoctoral'),
    ]
    DEGREE_RANKS = {
        'DIP': 1,
        'BD': 2,
        'MD': 3,
        'PHD': 4,
        'POSTDOC': 5,
    }
    degree = models.CharField(max_length=8, choices=DEGREE_CHOICES,default='DIP')
    degree_rank = models.PositiveIntegerField(editable=False, default=0)

    def save(self, *args, **kwargs):
        self.degree_rank = self.DEGREE_RANKS[self.degree]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.major} at {self.institution.name}"

# Authors models
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Journal Publication model
class JournalPublication(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, related_name='journal_publications')
    publication_date = models.DateField()
    journal_name = models.CharField(max_length=255)
    volume = models.CharField(max_length=50, blank=True, null=True)
    issue = models.CharField(max_length=50, blank=True, null=True)
    doi = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publication_date']

# Conference Publication model
class ConferencePublication(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, related_name='conference_publications')
    publication_date = models.DateField()
    conference_name = models.CharField(max_length=255)
    presentation_date = models.DateField(blank=True, null=True)
    conference_location = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publication_date']

# LinkType model
class LinkType(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, 
        validators=[RegexValidator(regex='^#[0-9A-Fa-f]{6}$', message='Enter a valid hex color code (e.g., #FFFFFF).')],
        help_text='Enter a valid hex color code (e.g., #FFFFFF).'
    )

    def __str__(self):
        return self.name

# Link model
class Link(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    publication = GenericForeignKey('content_type', 'object_id')
    type = models.ManyToManyField(LinkType, related_name='links')
    url = models.URLField()

    def __str__(self):
        return self.url

# Experience model
class Experience(models.Model):
    title = models.CharField(max_length=255)
    institutions = models.ManyToManyField(Institution, related_name='experiences', blank=True)
    supervisors = models.ManyToManyField(Advisor, related_name='experiences', blank=True)
    research = RichTextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} at {self.institutions.name}"

    @property
    def duration(self):
        if self.end_date:
            return self.end_date.year - self.start_date.year
        else:
            return None

    @property
    def date_display(self):
        if self.end_date:
            return f"{self.start_date.year} - {self.end_date.year}"
        return str(self.start_date.year)

# Achievement model
class Achievement(models.Model):
    title = RichTextField()
    start_date = models.IntegerField()
    end_date = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.get_title_snippet()

    def get_title_snippet(self):
        return html.unescape(strip_tags(self.title))

    @property
    def date_display(self):
        if self.end_date:
            return f"{self.start_date} - {self.end_date}"
        return str(self.start_date)

# SkillCategory model
class SkillCategory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Skill Categories'

    def __str__(self):
        return self.name

# Skill model
class Skill(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(SkillCategory, related_name='skills', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Activity model
class Activity(models.Model):
    title = models.CharField(max_length=100)
    institution = models.ForeignKey(Institution, related_name='activities', on_delete=models.DO_NOTHING, blank=True, null=True)
    description = RichTextField()
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        verbose_name_plural = "Activities"

    def __str__(self):
        return self.title
    
    @property
    def date_display(self):
        if self.end_date:
            return f"{self.start_date.year} - {self.end_date.year}"
        return str(self.start_date.year)
