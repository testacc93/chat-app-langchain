from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from langchain.llms import OpenAI
import json
from decouple import config
class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        async_to_sync(self.channel_layer.group_add)('programmers',self.channel_name)
        self.send({
        'type':'websocket.accept'
    })

    def websocket_receive(self, event):
        async_to_sync(self.channel_layer.group_send)('programmers', {
            'type':'chat.message',
            'message':event['text']
        })

    def websocket_disconnect(self, event):
        print('websocker disconnect', event)

    def chat_message(self, event):
        import os
        os.environ['OPENAI_API_KEY'] = config('OPENAI_API_KEY')
        
        model = OpenAI(temperature=0.6)
        question = json.loads(event['message'])['msg']
        res = model(question)
        res_dict = json.loads(event['message'])
        res_dict['msg'] = res
        res_str = json.dumps(res_dict)
        
        self.send({
        'type':'websocket.send',
        'text':res_str
        })
