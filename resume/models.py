from django.db import models
from django.core.validators import RegexValidator
from django.utils.html import strip_tags
import html
from ckeditor.fields import RichTextField

# Bio models
class Bio(models.Model):
    text = RichTextField()

    def __str__(self):
        return self.get_bio_snippet()
    
    def get_bio_snippet(self):
        return (html.unescape(strip_tags(self.text))[:50] + '...') if len(self.text)>50 else html.unescape(strip_tags(self.text))

# University models
class University(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

# Advisor models
class Advisor(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

# Education model
class Education(models.Model):
    university = models.ForeignKey(University, related_name='educations', on_delete=models.DO_NOTHING, blank=True, null=True)
    major = models.CharField(max_length=100)
    start = models.DateField()
    end = models.DateField()
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
        return f"{self.major} at {self.university.title}"

# Authors models
class Author(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

# LinkType model
class LinkType(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, 
        validators=[
            RegexValidator(
                regex='^#[0-9A-Fa-f]{6}$', 
                message='Enter a valid hex color code (e.g., #FFFFFF).'
            )
        ],
        help_text='Enter a valid hex color code (e.g., #FFFFFF).'
    )

# Publication model
class Publication(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, related_name='publication')
    publication_date = models.DateField()
    journal = models.CharField(max_length=255, blank=True)
    conference = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title

# PublicationLink model
class PublicationLink(models.Model):
    publication = models.ForeignKey(Publication, related_name='links', on_delete=models.CASCADE)
    url = models.URLField()
    type = models.ManyToManyField(LinkType, related_name='links')

    def __str__(self):
        return self.url

# Institution model
class Institution(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Experience model
class Experience(models.Model):
    title = models.CharField(max_length=255)
    institution = models.ManyToManyField(Institution, related_name='experiences', blank=True)
    supervisors = models.ManyToManyField(Advisor, related_name='experiences', blank=True)
    research = RichTextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} at {self.institution.name}"

    @property
    def duration(self):
        if self.end_date:
            return self.end_date.year - self.start_date.year
        else:
            return None

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
