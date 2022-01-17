from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .serializers import MessageSerializer
from .models import Message
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class MessageViewSet(APIView):

    #GET /messages/<message_id>
    #GET /messages/
    def get(self, request, message_id = None):
        if message_id:
            message = get_object_or_404(Message, message_id = message_id)
            serializer = MessageSerializer(message)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializers = Message.objects.all()
        messages_serializer = MessageSerializer(serializers, many=True)
        return Response(messages_serializer.data, status=status.HTTP_200_OK)

    #DELETE /messages/<message_id>
    def delete(self, request, message_id = None):
        if not message_id:
            return Response({"status": "error", "data": "No message detail is provided"}, status=status.HTTP_400_BAD_REQUEST)
        target_message = get_object_or_404(Message, message_id = message_id)
        target_message.delete()
        return Response({"status": "success", "data": "Message Deleted"})

    #POST /messages/
    def post(self, request):
        if 'message_content' not in request.data:
            return Response({"status": "error", "data": "No message content is provided"}, status=status.HTTP_400_BAD_REQUEST)
        message_is_palidrome = palindrome_validator(request.data['message_content'])
        request.data['is_palindrome'] = message_is_palidrome
        serializer = MessageSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    #PATCH /messages/<message_id>
    def patch(self, request, message_id=None):
        if not message_id:
            return Response({"status": "error", "data": "No message detail is provided"}, status=status.HTTP_400_BAD_REQUEST)
        if 'message_content' not in request.data:
            return Response({"status": "error", "data": "No message content is provided"}, status=status.HTTP_400_BAD_REQUEST)
        message = get_object_or_404(Message, message_id = message_id)
        new_message_is_palidrome = palindrome_validator(request.data['message_content'])
        request.data['is_palindrome'] = new_message_is_palidrome
        serializer = MessageSerializer(message, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})


def palindrome_validator(message_content):
    message_content.replace(" ", "")
    alphanumeric_filter = filter(str.isalnum, message_content)
    alphanumeric_string = "".join(alphanumeric_filter)
    alphanumeric_string = alphanumeric_string.lower()
    if len(alphanumeric_string) == 0 or len(alphanumeric_string) == 1:
        return True
    si = 0
    ti = len(alphanumeric_string)-1
    while si <= ti:
        if alphanumeric_string[si] != alphanumeric_string[ti]:
            return False
        si += 1
        ti -= 1
    return True
    
    



