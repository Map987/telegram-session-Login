# telegram-session-Login
https://github.com/Checkra2n/Telegram-QRCode 
### 仅获取session
```
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import qrcode
from PIL import Image
import telethon
from telethon import TelegramClient
from qrcode import QRCode, constants
from qrcode.image.pil import PilImage
import io
import os

# 创建二维码实例
qr = QRCode(
    version=1,
    error_correction=constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

def gen_qr(token: str, file_path: str):
    qr.clear()
    qr.add_data(token)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # 确保目录存在
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # 保存二维码图片
    img.save(file_path)

def display_url_as_qr(url):
    print(url)  # 打印URL
    # 假设您有一个方法来显示二维码，这里仅生成二维码图片
    file_path = '/storage/emulated/0/000/1/qr_code.jpg'
    gen_qr(url, file_path)
    print(f'QR code saved to {file_path}')

async def main(client: telethon.TelegramClient):
    if not client.is_connected():
        await client.connect()
    client.connect()
    qr_login = await client.qr_login()
    print(client.is_connected())
    r = False
    while not r:
        display_url_as_qr(qr_login.url)
        # 重要！您需要等待登录完成！
        try:
            r = await qr_login.wait(10)
        except:

            await qr_login.recreate()
TELEGRAM_API_ID= ""
TELEGRAM_API_HASH = ""

client = TelegramClient(StringSession(), TELEGRAM_API_ID, TELEGRAM_API_HASH)
client.loop.run_until_complete(main(client))

print("保留好这个session字符串，下次登录可以直接用这个字符串登录，不用再输入手机号和密码了：\n", client.session.save())
```

如果要打印图片，将 
https://github.com/Checkra2n/Telegram-QRCode
内添加

```
from telethon.sessions import StringSession
```
然后将 `client = TelegramClient("SessionName", TELEGRAM_API_ID, TELEGRAM_API_HASH)
client` 修改为 

```
client = TelegramClient(StringSession(), TELEGRAM_API_ID, TELEGRAM_API_HASH)
```
最后

```
print(client.session.save())
```
即可


## 下一次，不需要验证码

```
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import qrcode
from PIL import Image
import telethon
from telethon import TelegramClient
from qrcode import QRCode, constants
from qrcode.image.pil import PilImage
import io
import os


string = '1aaNk8EX-YRfwoRsebUkugFvht6DUPi_Q25UOCzOAqzc...' # 也就是上面 打印的client.session.save() 内容
with TelegramClient(StringSession(string), api_id, api_hash) as client:
client.loop.run_until_complete(client.send_message('me', 'Hi'))
```
或者下面的

```
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import qrcode
from PIL import Image
import telethon
from telethon import TelegramClient
from qrcode import QRCode, constants
from qrcode.image.pil import PilImage
import io
import os

string = '' #也就是上面 打印的client.session.save() 内容

TELEGRAM_API_ID= ""
TELEGRAM_API_HASH = ""


# 替换以下占位符为您的Telegram API ID和API HASH

session = StringSession(string)

# 创建TelegramClient实例
client = TelegramClient(session, TELEGRAM_API_ID, TELEGRAM_API_HASH)

async def main():
    # 连接到Telegram服务器
    await client.start()
    
    # 发送消息到自己的聊天
    await client.send_message('me', 'Hi')

# 运行主函数
client.loop.run_until_complete(main())

```

me是收藏夹

参考：
TelegramClient
https://docs.telethon.dev › sessions
Session Files — Telethon 1.36.0 documentation 

# 发送消息

```
from telethon import TelegramClient

# 替换以下变量为您的Telegram API凭证
API_ID = 'YOUR_API_ID'
API_HASH = 'YOUR_API_HASH'
# 替换以下变量为目标频道的ID
target_channel_id = '-100SOMETHING'  # 确保这是正确的频道ID

# 创建一个Telegram客户端实例
client = TelegramClient("session_name", API_ID, API_HASH)

async def main():
    # 连接到Telegram
    await client.start()
    print("🎉 Connected")

    # 指定本地文件的路径，确保路径中没有中文或空格
    local_file_path = '/storage/emulated/0/Pictures/Telegram/IMG_20240917_175622_207.jpg'  # 替换为您的本地文件路径

    # 尝试发送文件到目标频道
    try:
        await client.send_file(target_channel_id, local_file_path)
        print("File sent to the target channel.")
    except Exception as e:
        print(f"Failed to send file: {e}")

    # 保持客户端运行直到用户中断
    await client.run_until_disconnected()

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
```


```
 
from telethon import TelegramClient, events

# 替换以下变量为您的Telegram API凭证
API_ID = 'YOUR_API_ID'
API_HASH = 'YOUR_API_HASH'

# 创建一个Telegram客户端实例
client = TelegramClient("bot", API_ID, API_HASH)

async def main():
    # 连接到Telegram
    await client.start()
    print("🎉 Connected")

    # 注册一个事件处理器，监听所有新消息
 #   @client.on(events.NewMessage())
#    async def my_event_handler(event):
        # 打印所有对话（私聊、群组和频道）的名称和ID
        async for dialog in client.iter_dialogs():
            if dialog.is_group or dialog.is_channel:
                print(dialog.name, 'has ID', dialog.id)

    # 保持客户端运行直到用户中断
 #   await client.run_until_disconnected()

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
 
```

实时消息
```
import os
from telethon import TelegramClient, events

# 替换以下变量为您的Telegram API凭证和电话号码
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
your_phone_number = 'YOUR_PHONE_NUMBER'

# 替换以下变量为目标频道的ID
target_channel_id = 'TARGET_CHANNEL_ID'  # 例如: -1001234567890
source_channel_ids = ['SOURCE_CHANNEL_ID1', 'SOURCE_CHANNEL_ID2']  # 替换为源频道ID列表

# 创建一个Telegram客户端实例
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    # 连接到Telegram
    await client.start(your_phone_number)

    # 注册一个事件处理器，监听来自指定频道的新消息
    @client.on(events.NewMessage(chats=source_channel_ids))
    async def handler2(event):
        # 如果消息是分组的，则返回
        if event.grouped_id:
            return
        
        # 下载消息中的媒体文件
        filepath = await client.download_media(event)
        
        # 如果下载成功，打印文件路径
        if filepath:
            print(f"Media downloaded to {filepath}")
            
            # 将消息文本和下载的媒体文件发送到目标频道
            try:
                await client.send_message(target_channel_id, event.text, file=filepath)
                print("Message sent to target channel.")
            except Exception as e:
                print(f"Failed to send message: {e}")
        else:
            print("No media found to download.")

    # 保持客户端运行直到用户中断
    print("Listening for new messages from source channels...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
```

```
from telethon import TelegramClient
from telethon.sessions import StringSession

string = ''
TELEGRAM_API_ID= ""
TELEGRAM_API_HASH = ""

session = StringSession(string)

# 创建TelegramClient实例
client = TelegramClient(session, TELEGRAM_API_ID, TELEGRAM_API_HASH)

from telethon import TelegramClient

async def main():
  await client.start()
  async for dialog in client.iter_dialogs():
        print(dialog.name, 'has ID', dialog.id)
async with client:
    client.loop.run_until_complete(main())
```

#### 群组 频道 收藏夹 邀请链接填写方式
`client.send_message(entity='ok', message="ok")` # 注意`entity='ok'`内可以是邀请链接 `t.me/jahaahh` ;可以是频道公开名称链接 比如 t.me/TelethonChat，此时可以直接填写 `TelethonChat` ； 可以是 `me`，代表收藏夹； 可以是频道 / 群组的id 比如`-10051810060`

```
from telethon import TelegramClient
from telethon.sessions import StringSession

string = ''
import nest_asyncio
nest_asyncio.apply()
TELEGRAM_API_ID= ""
TELEGRAM_API_HASH = ""

# 替换以上占位符为您的Telegram API ID和API HASH

session = StringSession(string)

# 创建TelegramClient实例
client = TelegramClient(session, TELEGRAM_API_ID, TELEGRAM_API_HASH)

from telethon import TelegramClient

async def main():
  await client.start()
  await client.send_message(entity='ok', message="ok") # 注意entity='ok'内可以是邀请链接 t.me/jahaahh ;可以是频道公开名称链接 比如 t.me/TelethonChat，此时可以直接填写 TelethonChat ； 可以是 me，代表收藏夹； 可以是频道/组的id 比如-10051810060
"""
  async for dialog in client.iter_dialogs():
        print(dialog.name, 'has ID', dialog.id)
"""
 
async with client:
client.loop.run_until_complete(main())
```

### 下载解压文件

```
import json
from telethon import TelegramClient
#import socks
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
import json
from telethon import TelegramClient
from telethon.tl.types import PeerUser
from telethon.tl.types import MessageEntityTextUrl
# 设置 TelegramClient，连接到 Telegram API
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
#import qrcode
#from PIL import Image
import telethon
from telethon import TelegramClient
#from qrcode import QRCode, constants
#from qrcode.image.pil import PilImage
import io
import os
from datetime import datetime
import time
import urllib.parse
import os
import asyncio
from datetime import datetime, timedelta, timezone
import nest_asyncio
nest_asyncio.apply()
user_name = "me"
string = ''
TELEGRAM_API_ID= ""
TELEGRAM_API_HASH = ""
session = StringSession(string)
output = "/content"
# 创建TelegramClient实例
client = TelegramClient(session, TELEGRAM_API_ID, TELEGRAM_API_HASH)
async def main():
  await client.start()
  print("start")
  async for message in client.iter_messages(user_name,offset_date=datetime.now(tz=timezone.utc) - timedelta(hours=1),reverse=True):
    print(message.sender_id, ':', message.text)
    path = await client.download_media(message.document, output) # 下载文件
    print(path)
asyncio.run(main())
```

```
import os
import asyncio
from datetime import datetime, timedelta
import pytz

async def main():
    await client.start()
    print("start")
    for file_path in get_files_in_content():
       # async for message in client.iter_messages(user_name, offset_date=datetime.now(tz=pytz.utc) - timedelta(hours=1), reverse=True):
            await client.send_file("me", file_path, force_documents=True)  # 发送文件
            print(file_path)

def get_files_in_content():
    content_path = '/content/'
    for root, dirs, files in os.walk(content_path):
        for file in files:
            yield os.path.join(root, file) 

asyncio.run(main()) # 包括子文件夹
```


草稿、未发送的输入内容，参考https://docs.telethon.dev/en/stable/modules/client.html#telethon.client.dialogs.DialogMethods.iter_drafts ：
```
async for draft in client.iter_drafts(['bot1', 'bot2']): #频道id, "me", 频道名字都可以 
    print(draft.text)

```

获取机器人左侧按钮网页链接，menu button，创建可以使用@botfather进行创建

```
from telethon.tl.functions.users import GetFullUserRequest

url = (await client(GetFullUserRequest(bot))).full_user.bot_info.menu_button.url # "bot"为bot用户名
```

