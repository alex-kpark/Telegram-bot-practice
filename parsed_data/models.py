from django.db import models

# Create your models here.

class BlogData(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField()

    #Admin에서 더 잘 보이도록 하기 위해서 체크
    def __str__(self):
        return self.title
