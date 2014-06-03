from django.db import models

# Create your models here.
class Problem(models.Model):
    class Meta:
        verbose_name = 'Problem'
        verbose_name_plural = 'Problems'

    title = models.CharField(blank=True, max_length=150)
    image = models.ImageField(blank=True, upload_to="problems")

    def __unicode__(self):
        return self.title
    