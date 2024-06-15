from django.db import models

# Bio models
class Bio(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.get_bio_snippet()
    
    def get_bio_snippet(self):
        return (self.text[:30] + '...') if len(self.text)>30 else self.text

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

# Publication model
class Publication(models.Model):
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=200)
    publication_date = models.DateField()
    publication_link = models.URLField(blank=True)
    journal = models.CharField(max_length=255, blank=True)
    conference = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title

# PublicationLink model
class PublicationLink(models.Model):
    publication = models.ForeignKey(Publication, related_name='links', on_delete=models.CASCADE)
    url = models.URLField()

    def __str__(self):
        return self.url