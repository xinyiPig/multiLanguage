import requests
import json
import random


def randomNum(num):
    str = ""
    for i in range(num):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        str += ch
    return str


def send_message(phoneNumber):
    code = randomNum(6)
    resp = requests.post("http://sms-api.luosimao.com/v1/send.json",
                         auth=("api", "key-9183cb6cec9b2f63a5b1fa380399f453"),
                         data={
                             "mobile": phoneNumber,
                             "message": "您的验证码是%s，请尽快完成验证。【凯归科技】" % (code)
                         }, timeout=3, verify=False)
    result = json.loads(resp.content.decode('utf-8'))
    return result,code
