from nonebot import on_keyword
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import MessageSegment, Message
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
import re
import requests
from PIL import Image
from io import BytesIO
from .Anime2Sketch import interface


c2s = on_keyword(['线稿'], rule = to_me(), priority=15)
@c2s.handle()
async def c2s_handle(bot: Bot, event: Event, state: T_State):
    raw_msg = str(event.get_message())
    pattern = "url=.*?\]"
    urls = re.findall(pattern, raw_msg)
    message = Message()
    message.append(MessageSegment.at(event.user_id))
    if (urls == []):
        await c2s.finish(message + "没有图片捏~")
    for url in urls:
        response = requests.get(url[4:-1])
        color = Image.open(BytesIO(response.content))
        sketch = interface.color2sketch(color)
        img_buffer = BytesIO()
        sketch.save(img_buffer, format='png')
        message.append(MessageSegment.image(img_buffer))
    await c2s.send(message)
