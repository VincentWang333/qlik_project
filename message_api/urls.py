from django.urls import path
from .views import MessageViewSet

urlpatterns = [
    path('messages/', MessageViewSet.as_view(), name='message_list'),
    path('messages/<str:message_id>', MessageViewSet.as_view(), name='message')
]