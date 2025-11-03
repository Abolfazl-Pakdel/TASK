# from django.db import models

# Create your models here.
# from django.db import models

# class Mockup(models.Model):
#     image = models.ImageField(upload_to='mockups/')
#     text = models.CharField(max_length=100)
#     result = models.ImageField(upload_to='results/', null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.text
from django.db import models

class Mockup(models.Model):
    text = models.CharField(max_length=255)
    font = models.CharField(max_length=50, default='arial', blank=True)
    text_color = models.CharField(max_length=10, default='#000000')
    shirt_color = models.CharField(max_length=20, default='white')
    image = models.ImageField(upload_to='mockups/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text} ({self.shirt_color})"
