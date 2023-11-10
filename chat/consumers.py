import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from Backend.models import Message , Team , User
import datetime 
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        
        self.room_name = self.scope["url_route"]["kwargs"]["id"]
        self.room_group_name = "chat_%s" % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        print("SOCKET CONNECTED")
        chats = []
        self.accept()
        t = Team.objects.get(id=self.room_name)
        for chat in t.chats.all():
            entry = {}
            entry["message"] = chat.message
            entry["sender"] = str(chat.sender.name)
            entry["timestamp"] = str(chat.timestamp)
            chats.append(json.dumps(entry))
        chats = chats[::-1]
        self.send(text_data=json.dumps(chats))
    
    def receive(self, text_data):
        print("RECIEVED")
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        id = text_data_json["id"]
        m = Message()
        u = User.objects.get(id=id)
        m.sender = u
        m.message = message
        m.timestamp = datetime.datetime.now() + datetime.timedelta(0,0,0,0,30,11)
        m.save()
        t = Team.objects.get(id=self.room_name)
        t.chats.add(m)
        t.save()
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message , "sender" : id , "timestamp" : str(m.timestamp)}
        )
    def chat_message(self, event):
        message = event["message"]
        id = event["sender"]
        print(event)
        chats = []
        # self.send(text_data=json.dumps({"message" : message , "id" : id , "timestamp" : event["timestamp"]}))
        t = Team.objects.get(id=self.room_name)
        for chat in t.chats.all():
            entry = {}
            entry["message"] = chat.message
            entry["sender"] = str(chat.sender.name)
            entry["timestamp"] = str(chat.timestamp)
            chats.append(json.dumps(entry))
        chats = chats[::-1]
        self.send(text_data=json.dumps(chats))
        # Send message to WebSocket
        
        
        
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
    
