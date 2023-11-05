import json
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print("SOCKET CONNECTED")
        self.accept()
    def receive(self, text_data):
        print("RECIEVED")
        print(text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        self.send(text_data=json.dumps({
            "message" : message,
        }))
    def disconnect(self, code):
        pass
    
