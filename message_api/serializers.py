from email import message
from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = [
            'message_id',
            'message_content',
            'is_palindrome',
            'last_modified'
        ]