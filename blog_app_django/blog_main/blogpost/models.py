from django.db import models
from django.contrib.auth.models import User

class PostModel(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/',blank=True, null=True )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def comment_count(self):
        return self.comments.all().count()

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ('-date_created', )
    
    

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length = 200)

    def __str__(self) -> str:
        return self.content