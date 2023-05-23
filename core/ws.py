import json
from time import sleep

from channels.generic.websocket import (AsyncJsonWebsocketConsumer,
                                        JsonWebsocketConsumer, async_to_sync)

from core.utility import *


class GptResponseGenerator(JsonWebsocketConsumer):
    def connect(self):
        # 파라미터 값으로 채팅 룸을 구별
        print("GPT RESPONSE CONNECT")
        # print(self.scope['headers'])
        self.room_name = "GPT_ROOM"
        self.room_group_name = 'talk_%s' % self.room_name

        # 룸 그룹에 참가
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        hello_message = "안녕하세요"
        self.send_output_text(hello_message)

        hello_message_audio_url = get_audio_file_url_using_polly(
            hello_message)
        self.send_audio_url(hello_message_audio_url)
        self.send_finish_signal()

    def disconnect(self, close_code):
        print("DISCONNECT GPT RESPONSE")
        # 룸 그룹 나가기
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # 웹소켓으로부터 메세지 받음

    def receive(self, text_data):
        print("RECEIVE!!!")
        data = json.loads(text_data)
        audio_file = data.get('audio_file', None)
        audio_data = decode_audio(audio_file)
        save_audio(audio_data, create_input_file_name())
        text_gotten_by_input_data = generate_text(audio_data)
        self.send_input_text(text_gotten_by_input_data)
        print('SENT1')
        messages = []  # TO DO : messages by user DB (using ROOM_NAME)
        messages = add_user_message_to_messages(
            messages, text_gotten_by_input_data)
        for sentence in get_sentences_by_chatgpt(messages):
            messages = add_assistant_message_to_messages(messages, sentence)
            self.send_output_text(sentence)
            print('SEND OUTPUT TEXT')
            output_audio_url = get_audio_file_url_using_polly(sentence)
            self.send_audio_url(output_audio_url)
            print("SEND AUDIO URL")

        self.send_finish_signal()

    # 룸 그룹으로부터 메세지 받음
    def send_input_text(self, text):
        print("INPUT TEXT")
        # 웹소켓으로 메세지 보냄
        self.send(text_data=json.dumps({
            "type": "input_text",
            "content": text
        }))

    def send_output_text(self, text):
        print("OUTPUT TEXT")
        self.send(text_data=json.dumps({
            "type": "output_text",
            "content": text
        }))

    def send_finish_signal(self):
        print("OUTPUT TEXT")
        self.send(text_data=json.dumps({
            "type": "finish_signal",
            "content": "FINISH!"
        }))

    def send_audio_url(self, audio_url):
        print("AUDIO URL")
        # 웹소켓으로 메세지 보냄
        self.send(text_data=json.dumps({
            "type": "audio_url",
            "content": audio_url
        }))


class ChatConsumer(JsonWebsocketConsumer):
    def connect(self):
        # 파라미터 값으로 채팅 룸을 구별
        print("CONNECT!!!")
        # print(self.scope['headers'])
        self.room_name = "DEFUALT_ROOM"
        self.room_group_name = 'chat_%s' % self.room_name

        self.accept()
        # 룸 그룹에 참가
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        print(self.channel_name)

        sleep(1)

        async_to_sync(self.channel_layer.send)(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': "SSIBAL!"
            }
        )

        sleep(1)

        async_to_sync(self.channel_layer.send)(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': "SAEGGIYA"
            }
        )

    def disconnect(self, close_code):
        print("DISCONNECT!!!")
        # 룸 그룹 나가기
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # 웹소켓으로부터 메세지 받음
    def receive(self, text_data):
        print("RECEIVE!!!")
        print(text_data)
        data_json = json.loads(text_data)
        message = data_json.get('message', None)
        data = data_json.get('data', None)
        print("MESSAGE : ", message)
        print('DATA', data)
        reversing_data = message or data
        # 룸 그룹으로 메세지 보냄
        async_to_sync(self.channel_layer.send)(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': reversing_data[::-1]
            }
        )

    # 룸 그룹으로부터 메세지 받음
    def chat_message(self, event):
        print("CHAT_MESSAGE!!!")
        message = event['message']
        print("REVERSE_MESSAGE : ", message)

        self.send(text_data=json.dumps({
            'message': message
        }))
