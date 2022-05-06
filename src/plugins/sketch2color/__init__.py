from nonebot import on_keyword
from nonebot.adapters.onebot.v11 import MessageSegment, Message
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me
import re
import requests
from PIL import Image
from io import BytesIO
from .SGRUnet import interface

s2c = on_keyword(['上色'], rule = to_me(), priority=15)
@s2c.handle()
async def s2c_handle(bot: Bot, event: Event, state: T_State):
    raw_msg = str(event.get_message())
    pattern = "url=.*?\]"
    urls = re.findall(pattern, raw_msg)
    message = Message()
    message.append(MessageSegment.at(event.user_id))
    if (urls == []):
        await s2c.finish(message + "没有图片捏~")
    print(urls)
    for url in urls:
        response = requests.get(url[4:-1])
        color = Image.open(BytesIO(response.content))
        sketch = interface.sketch2color(color)
        img_buffer = BytesIO()
        sketch.save(img_buffer, format='png')
        message.append(MessageSegment.image(img_buffer))
    await s2c.send(message)