
import json
import ssl
import urllib.request

client_id = "_8gBiObRwfXtrkGoN_cg"  # 개발자센터에서 발급받은 Client ID 값
client_secret = "LOplcDXplV"  # 개발자센터에서 발급받은 Client Secret 값
context = ssl._create_unverified_context()


def translate(message):
    data = "source=ko&target=en&text=" + message
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(
        request, data=data.encode("utf-8"), context=context)
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        translated_message = json.loads(response_body.decode(
            'utf-8'))["message"]["result"]["translatedText"]
        return translated_message
    else:
        print("Error Code:" + rescode)
        raise Exception("Error Code:" + rescode)
