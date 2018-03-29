# -*- coding: utf-8 -*-
import json
import requests
from wxpy import *


def auto_reply(text):
    url = "http://www.tuling123.com/openapi/api"
    api_key = "2a2e87519c1b4cf79e6441e5724232d3"
    payload = {
        "key": api_key,
        "info": text,
        "userid": "237418"
    }
    r = requests.post(url, data=json.dumps(payload))
    result = json.loads(r.content)
    return "[来自波波机器人的自动回复]" + result["text"]


bot = Bot(cache_path=True)
# my_friend = bot.friends()
my_friend = bot.groups()


@bot.register(my_friend)
def forward_message(msg):
    return auto_reply(msg.text)


embed()



