from django.urls import path

from apps.chat.views import MessageSendView, RoomCreateView, RoomListView, RoomMessagesView

urlpatterns = [
    path("rooms/", RoomListView.as_view(), name="chat-rooms"),
    path("rooms/create/", RoomCreateView.as_view(), name="chat-room-create"),
    path("rooms/<int:room_id>/messages/", RoomMessagesView.as_view(), name="chat-messages"),
    path("rooms/<int:room_id>/messages/send/", MessageSendView.as_view(), name="chat-send"),
]
