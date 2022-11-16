from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    message_text = models.CharField(max_length=70)
    pub_date = models.DateTimeField('date published')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default = 'Author')
    def __str__(self):
        return self.message_text
