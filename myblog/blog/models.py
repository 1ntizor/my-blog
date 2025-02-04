from django.db import models

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('tech', 'Technologies'),
        ('life', 'Life'),
        ('edu', 'Education'),
    ]
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='tech')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment from: {self.author} to {self.post.title}"  