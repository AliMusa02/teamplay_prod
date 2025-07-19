from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()

# Create your models here.


class Posts(models.Model):
    content = models.TextField(
        _('content'), max_length=500, blank=False, null=False)
    post_pic = models.ImageField(
        null=True, blank=True, upload_to="images/", default='images/fallback.png')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-created_at']
