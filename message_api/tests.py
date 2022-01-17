import json
from django.test import TestCase, Client
from .serializers import MessageSerializer
from .models import Message
from django.urls import reverse
from rest_framework import status

# Create your tests here.

client = Client()

class GetSingleMessageTest(TestCase):
    def setUp(self):
        self.message_one = Message.objects.create(message_content="aaaAAAaaa#$ %AAaaa")

    def test_get_valie_single_message(self):
        response = client.get(
            reverse('message',kwargs={'message_id': self.message_one.message_id})
        )
        message = Message.objects.get(pk=self.message_one.pk)
        serializer = MessageSerializer(message)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_invalid_single_message(self):
        response = client.get(
            reverse('message', kwargs={'message_id': 9999})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class GetAllMessageTest(TestCase):
    def setUp(self):
        self.message_one = Message.objects.create(message_content="aaaAAAaaa#$ %AAaaa")
        self.message_two = Message.objects.create(message_content="baaAAAaaa#$ %AAaaa")
        self.message_three = Message.objects.create(message_content="caaAAAaaa#$ %AAaaa")
        self.message_four = Message.objects.create(message_content="daaAAAaaa#$ %AAaaa")
        self.message_five = Message.objects.create(message_content="eaaAAAaaa#$ %AAaaa")
        self.message_six = Message.objects.create(message_content="faaAAAaaa#$ %AAaaa")

    def test_get_all_messages(self):
        response = client.get(reverse('message_list'))
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CreateNewMessageTest(TestCase):
    def setUp(self):
        self.valid_palindrome_payload = {
            "message_content": "bbbBBBbb#   %$@#$bbBB Bbb#@!#$bbb"
        }
        self.valid_not_palindrome_payload = {
            "message_content": "dafsf@#AFsad  sfadFSAF@#R!#!#$asdfg{Fdsafsaf{Asd23r w#$@#$$FDS "
        }
        self.invalid_payload = {}
    
    def test_create_valid_palindrome_message(self):
        response = client.post(
            reverse('message_list'),
            data=json.dumps(self.valid_palindrome_payload),
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['is_palindrome'], True)
    
    def test_create_valid_not_palindrome_message(self):
        response = client.post(
            reverse('message_list'),
            data=json.dumps(self.valid_not_palindrome_payload),
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['is_palindrome'], False)

    def test_create_invalid_message(self):
        response = client.post(
            reverse('message_list'),
            data=json.dumps(self.invalid_payload),
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleMessage(TestCase):
    def setUp(self):
        self.message_one = Message.objects.create(message_content="aaaAAAaaa#$ %AAaaa")
        self.message = self.message_one

    def test_valid_delete_puppy(self):
        response = client.delete(
            reverse('message', kwargs={'message_id': self.message_one.message_id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_delete_puppy(self):
        response = client.delete(
            reverse('message', kwargs={'message_id': 9999})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class UpdateSingleMessageTest(TestCase):
    def setUp(self):
        self.message_one = Message.objects.create(message_content="aaaAAAaaa#$ %AAaaa")
        self.message_two = Message.objects.create(message_content="baaAAAaaa#$ %AAaaa")
        self.valid_palindrome_payload = {
            'message_content': "aaaAAAaaa#$ %AAaaa"
        }
        self.valid_not_palindrome_payload = {
            'message_content': "baaAAAaaa#$ %AAaaa"
        }
        self.invalid_payload = {}
    
    def test_valid_not_palindrome_update(self):
        response = client.patch(
            reverse('message',kwargs={'message_id': self.message_one.message_id}),
            data = json.dumps(self.valid_not_palindrome_payload),
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['message_content'], self.valid_not_palindrome_payload['message_content'])
        self.assertEqual(response.data['data']['is_palindrome'], False)

    def test_valid_palindrome_update(self):
        response = client.patch(
            reverse('message', kwargs={'message_id': self.message_two.message_id}),
            data = json.dumps(self.valid_palindrome_payload),
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['message_content'], self.valid_palindrome_payload['message_content'])
        self.assertEqual(response.data['data']['is_palindrome'], True)
    
    def test_invalid_update(self):
        response = client.patch(
            reverse('message', kwargs={'message_id': self.message_two.message_id}),
            data = json.dumps(self.invalid_payload),
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)