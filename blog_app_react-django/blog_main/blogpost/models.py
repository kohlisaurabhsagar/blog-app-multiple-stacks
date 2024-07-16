from django.db import models
from django.conf import settings

class PostModel(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/',blank=True, null=True )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    
    @property
    def user_username(self):
        return self.user.username
    
    def comment_count(self):
        return self.comments.all().count()

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ('-date_created', )
    
    

class Comments(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length = 200)

    def __str__(self) -> str:
        return self.content
    
    @property
    def author_username(self):
        return self.author.username