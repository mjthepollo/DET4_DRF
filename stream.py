import csv
import time

from papago import translate

from core.setup import openai

# send a ChatCompletion request to count to 100

message_lists = [
    "안녕 ChatGPT야!",
    "머신러닝이 뭐야?",
    "chatGPT 너는 뭘 할 수 있니?",
    "죽고싶어?",
    "주펄찜 레시피 알려줘.",
]

translated_message_lists = []

stream_response_time_lists = []
non_stream_response_time_lists = []
stream_answer_lists = []
non_stream_answer_lists = []


def use_stream_answer(message):
    stream_start_time = time.time()
    response_stream = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'user', 'content': message}
        ],
        stream=True  # again, we set stream=True
    )
# create variables to collect the stream of chunks
    collected_chunks = []
    collected_messages = []
    # iterate through the stream of events
    for chunk in response_stream:
        # chunk_time = time.time() - stream_start_time  # calculate the time delay of the chunk
        collected_chunks.append(chunk)  # save the event response
        chunk_message = chunk['choices'][0]['delta']  # extract the message
        collected_messages.append(chunk_message)  # save the message
        # print(f"Message received {chunk_time:.2f} seconds after request: {chunk_message}")  # print the delay and text
    # print the time delay and text received
    full_reply_content = ''.join([m.get('content', '')
                                 for m in collected_messages]).strip()
    spent_time = time.time() - stream_start_time
    print(f"(Stream)Messge: {message}")
    print(f"(Stream)Full conversation received: {full_reply_content}")
    print(
        f"(Stream)Full response received {spent_time:.2f} seconds after request")
    stream_response_time_lists.append(spent_time)
    stream_answer_lists.append(full_reply_content)


def use_non_stream_answer(message):
    non_stream_start_time = time.time()
    response_not_stream = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'user', 'content': message}
        ],
    )
    spent_time = (time.time() - non_stream_start_time)
    non_stream_response_time_lists.append(spent_time)
    non_stream_answer = response_not_stream.choices[0].message.content.strip()
    non_stream_answer_lists.append(non_stream_answer)

    print(f"(Non-Stream)Message: {message}")
    print(f"(Non-Stream)Full conversation received:\n{non_stream_answer}")
    print(
        f"(Non-Stream)Full response received {spent_time:.2f} seconds after request")


for message in message_lists:
    translated_massage = translate(message)
    translated_message_lists.append(translated_massage)
    use_stream_answer(message)
    use_non_stream_answer(message)
    use_stream_answer(translated_massage)
    use_non_stream_answer(translated_massage)


# ---------------------TO CSV--------------------------------


def time_to_2f(time):
    return "{:.2f}".format(time)


with open('output_compare.csv', mode='w', newline='') as csv_file:
    # Create a CSV writer object
    csv_writer = csv.writer(csv_file)
    header_row = ["Input", "Stream-output", "Stream-response-time", "Non-stream-output", "Non-stream-response-time",
                  "Translated Input", "Stream-output", "Stream-response-time", "Non-stream-output", "Non-stream-response-time"]
    row_lists = [header_row]
    for i in range(len(message_lists)):
        row = []
        row.append(message_lists[i])
        row.append(stream_answer_lists[2*i])
        row.append(time_to_2f(stream_response_time_lists[2*i]))
        row.append(non_stream_answer_lists[2*i])
        row.append(time_to_2f(non_stream_response_time_lists[2*i]))
        row.append(translated_message_lists[i])
        row.append(stream_answer_lists[2*i+1])
        row.append(time_to_2f(stream_response_time_lists[2*i+1]))
        row.append(non_stream_answer_lists[2*i+1])
        row.append(time_to_2f(non_stream_response_time_lists[2*i+1]))
        row_lists.append(row)

    # Write data to CSV file
    for row in row_lists:
        csv_writer.writerow(row)
