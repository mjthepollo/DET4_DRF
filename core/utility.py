import base64
import datetime
from io import BytesIO

from core.setup import BUCKET_NAME, logger, openai, polly, polly_voice, s3


def save_file_to_s3(file, file_name):
    try:
        s3.upload_fileobj(file, BUCKET_NAME, file_name)
    except Exception as e:
        raise Exception(f"Error uploading to S3: {e}")


def decode_audio(encoded_audio_data):
    audio_data = base64.b64decode(encoded_audio_data)
    return audio_data


def create_file_time():
    now = datetime.datetime.now()
    return f'{now.year}_{now.month}_{now.day}_{now.hour}{now.minute}{now.second}.wav'


def create_input_file_name():
    return f"INPUT_{create_file_time()}"


def create_output_file_name():
    return f"OUTPUT_{create_file_time()}"


def save_audio(audio_data, file_name):
    audio_file = BytesIO(audio_data)
    try:
        save_file_to_s3(audio_file, file_name)
    except Exception as e:
        raise Exception("An Error Occur in SAVE AUDIO")


def generate_text(audio_data):
    now = datetime.datetime.now()
    audio_file = BytesIO(audio_data)
    # 의미없다
    audio_file.name = f"temp_{now.year}_{now.month}_{now.day}_{now.hour}{now.minute}{now.second}.wav"
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    text = transcript['text']
    logger.info(text)
    return text


def add_user_message_to_messages(messages, message):
    messages.append({"role": "user", "content": message})
    return messages


def add_assistant_message_to_messages(messages, message):
    messages.append({"role": "assistant", "content": message})
    return messages


def get_message_by_chatgpt(messages):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages)
    return completion.choices[0].message.content.strip()


def get_audio_file_url_using_polly(message):
    response = polly.synthesize_speech(
        Text=message, VoiceId=polly_voice, OutputFormat="mp3")
    audio_binary_data = response["AudioStream"].read()
    output_file_name = create_output_file_name()
    save_audio(audio_binary_data, output_file_name)
    url = s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": BUCKET_NAME, "Key": output_file_name},
        ExpiresIn=3600,
    )
    return url
