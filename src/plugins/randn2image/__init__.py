import random
from nonebot.plugin import on_keyword
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.rule import to_me
from .stylegan2 import interface
from io import BytesIO

r2i = on_keyword(['头像'], rule = to_me(), priority=15)
@r2i.handle()
async def r2i_handle(bot: Bot, event: Event):
    rnd = random.randint(0, 2**32-1)
    img = interface.rand2img(rnd)
    img_buffer = BytesIO()
    img.save(img_buffer, format='png')
    await r2i.send(Message(MessageSegment.at(event.user_id) + MessageSegment.image(img_buffer)))