from django.db import models

# Create your models here.
class Episode(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    pub_date = models.DateTimeField()
    link = models.URLField()
    img_url = models.URLField()
    podcast_name = models.CharField(max_length=20)
    guid = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return f'{self.podcast_name} : {self.title}'
    
    
    
    
