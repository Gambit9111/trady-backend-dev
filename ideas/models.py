from django.db import models
from authentication.models import Profile
import uuid
from django.urls import reverse


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']


class Image(models.Model):
    image = models.ImageField(upload_to='images/ideas/')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.image.name

    def get_absolute_url(self):
        return reverse('image-detail', args=[str(self.id)])