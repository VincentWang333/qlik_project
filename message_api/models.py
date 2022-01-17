from django.db import models

# Create your models here.

class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    message_content = models.TextField(default="")
    is_palindrome = models.BooleanField(default=False)
    last_modified = models.DateTimeField(auto_now=True)