import datetime
import json
import os
import time
from datetime import datetime
from io import BytesIO

from django.test import TestCase

from core.setup import BUCKET_NAME, openai, s3
from core.utility import (add_assistant_message_to_messages,
                          add_user_message_to_messages,
                          create_output_file_name, decode_audio, generate_text,
                          get_audio_file_url_using_polly,
                          get_message_by_chatgpt, save_audio, save_file_to_s3)

TEST_INPUT_JSON_PATH = "core/tests/src/test_input.json"
TEST_FILE_PATH = "core/tests/src/test.txt"


def check_file_in_s3_bucket(bucket_name, file_key):
    try:
        s3.head_object(Bucket=bucket_name, Key=file_key)
        print(f"File '{file_key}' exists in bucket '{bucket_name}'.")
        return True
    except s3.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            print(
                f"File '{file_key}' not found in bucket '{bucket_name}'.")
        else:
            print(
                f"Error checking file '{file_key}' in bucket '{bucket_name}': {e}")
        return False


class CoreUtilityTest(TestCase):

    def test_save_file_to_s3(self):
        with open(TEST_FILE_PATH, 'rb') as f:
            content = f.read()
        test_file = BytesIO(content)
        test_file.name = "test.txt"
        save_file_to_s3(test_file, test_file.name)
        assert check_file_in_s3_bucket(BUCKET_NAME, test_file.name)
        s3.delete_object(Bucket=BUCKET_NAME, Key=test_file.name)

    def test_decode_audio(self):
        with open(TEST_INPUT_JSON_PATH, 'r') as f:
            json_data = json.load(f)
        audio_data = decode_audio(json_data["audio"])
        audio_file = BytesIO(audio_data)
        audio_file.name = f'test_input.mp3'
        now_second = datetime.now().second
        test_output_name = f"core/tests/src/test_output_{now_second}.mp3"
        with open(test_output_name, "wb") as f:
            f.write(audio_data)
        assert os.path.exists(
            test_output_name), f"The file '{test_output_name}' does not exist"
        os.remove(test_output_name)

    def test_save_audio(self):
        with open(TEST_INPUT_JSON_PATH, 'r') as f:
            json_data = json.load(f)
        audio_data = decode_audio(json_data["audio"])
        test_file_name = create_output_file_name()
        save_audio(audio_data, test_file_name)
        assert check_file_in_s3_bucket(BUCKET_NAME, test_file_name)
        s3.delete_object(Bucket=BUCKET_NAME, Key=test_file_name)

    def test_generate_text(self):
        with open(TEST_INPUT_JSON_PATH, 'r') as f:
            json_data = json.load(f)
        audio_data = decode_audio(json_data["audio"])
        start_time = time.time()
        text = generate_text(audio_data)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("Generate Text By Audio Time elapsed: {:.2f} seconds".format(
            elapsed_time))
        assert "안녕하세요" in text

    def test_add_user_message_to_messages(self):
        existing_messages = [
            {"role": "system", "content": "This is just test"},
            {"role": "user", "content": "Hello World?!"},
            {"role": "assistant", "content": "GoodBye World!"}
        ]
        new_message = "Hello World! Again!"
        result_messages = add_user_message_to_messages(
            existing_messages, new_message)
        assert len(result_messages) == 4
        assert result_messages[3]["role"] == "user"
        assert result_messages[3]["content"] == new_message

    def test_add_assistant_message_to_messages(self):
        existing_messages = [
            {"role": "system", "content": "This is just test"},
            {"role": "user", "content": "Hello World?!"},
        ]
        new_message = "GoodBye World!"
        result_messages = add_assistant_message_to_messages(
            existing_messages, new_message)
        assert len(result_messages) == 3
        assert result_messages[2]["role"] == "assistant"
        assert result_messages[2]["content"] == new_message

    def test_get_message_by_chatgpt(self):
        test_quote = "Hello world!"
        start_time = time.time()
        send_messages = [
            {"role": "user", "content": f"THIS IS API_TEST! You must tell me '{test_quote}'"}]
        received_message = get_message_by_chatgpt(send_messages)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("Generate Text By CHATGPT elapsed: {:.2f} seconds".format(
            elapsed_time))
        assert received_message == test_quote

    def test_get_audio_file_url_using_polly(self):
        message = "안녕하세요"
        start_time = time.time()
        test_file_name = create_output_file_name()
        url = get_audio_file_url_using_polly(message)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("Generate AUDIO By POllY elapsed: {:.2f} seconds".format(
            elapsed_time))
        assert check_file_in_s3_bucket(BUCKET_NAME, test_file_name)
        print(
            f"GENERATED AUDIO File by POLLY URL: {url}\n(!!!!Deleted Very After Text!!!!)")
        s3.delete_object(Bucket=BUCKET_NAME, Key=test_file_name)
