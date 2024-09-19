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
import qrcode
#from PIL import Image
import telethon
from telethon import TelegramClient
from qrcode import QRCode, constants
from qrcode.image.pil import PilImage
import io
import os
from datetime import datetime
import time
import urllib.parse
output = ""
STRING = os.getenv('STRING')
TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')    
TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')    
CHANNEL_USERNAME = os.getenv('CHANNEL_USERNAME')
string = STRING

TELEGRAM_API_ID= TELEGRAM_API_ID
TELEGRAM_API_HASH = TELEGRAM_API_HASH


# 替换以下占位符为您的Telegram API ID和API HASH

session = StringSession(string)

# 创建TelegramClient实例
client = TelegramClient(session, TELEGRAM_API_ID, TELEGRAM_API_HASH)


import json
from telethon.tl.types import PeerUser, MessageMediaPhoto, MessageMediaDocument

def default_serializer(obj):
    """处理无法序列化的对象"""
    if isinstance(obj, PeerUser):
        return str(obj)  # 或者返回你希望存储的任何其他信息
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

 
import json
from cryptography.fernet import Fernet
import os

async def export_to_json(filename, data):
    encryption_key = os.getenv('TELEGRAM_API_HASH')
    # 如果没有提供密钥，则抛出异常
    if not encryption_key:
        raise ValueError("No encryption key provided in environment variable 'ENCRYPTION_KEY'")

    # 使用提供的密钥初始化 Fernet 对象
    fernet = Fernet(encryption_key)

    # 加密数据
    encrypted_data = []
    for item in data:
        # 将字典转换为 JSON 字符串
        json_str = json.dumps(item, ensure_ascii=False, indent=4, default=default_serializer)
        # 加密 JSON 字符串
        encrypted_str = fernet.encrypt(json_str.encode('utf-8'))
        # 将加密后的数据添加到列表中
        encrypted_data.append(encrypted_str)

    # 将加密后的数据写入文件
    with open(filename, 'wb') as f:
        for encrypted_item in encrypted_data:
            f.write(encrypted_item)
            f.write(b'\n')  # 写入一个换行符以分隔加密后的数据项

async def fetch_messages(channel_username):
    """
    获取指定频道的所有消息。

    参数:
    channel_username -- 目标频道的用户名
    """
    channel_entity = await client.get_input_entity(channel_username)
    offset_id = 0  # 初始消息 ID 偏移量
    all_messages = []  # 存储所有消息的列表
    limit = 100  # 设置获取消息的数量上限

    while len(all_messages) < limit:
        # 请求消息记录
        history = await client(GetHistoryRequest(
            peer=channel_entity,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=min(100, limit - len(all_messages)),  # 每次请求的消息数量，但不超过剩余需要获取的消息数量
            max_id=0,
            min_id=0,
            hash=0
        ))
        if not history.messages:  # 当没有更多消息时结束循环
            break
        last_group = []
        for message in history.messages:
            sender = await client.get_entity(message.chat_id)
            sender_username = sender.username if sender else 'Unknown'
            message_dict = {
                'id': message.id,
                'date': message.date.strftime('%Y-%m-%d %H:%M:%S'),
                'timestamp': int(message.date.timestamp()),
                'chat_id': message.from_id,
                'sender_username': sender_username,
                'grouped_id': message.grouped_id
            }
            urls = []
            for url_entity, inner_text in message.get_entities_text(MessageEntityTextUrl):

               url = url_entity.url
               print(url)
               print(message.message[url_entity.offset:url_entity.offset+ url_entity.length])
               
               if isinstance(url_entity, MessageEntityTextUrl):                                
                  message_dict['links'] = url
                  
               else:
                  print(f"o", inner_text)
                  urls.append(inner_text)
    #        items.append(message)
   #         last_group = message.grouped_id
            
            
            if message.message:
                message_dict['text'] = message.message
                filepath = "/storage/emulated/0/Pictures/vivo 文档/photo_2024-09-18_19-28-20.jpg"# 不能有中文，还是空格 

                
                
                
                
                
            if message.photo:
            
                # 获取照片信息
                photo = message.photo
                path = await client.download_media(message.media, output)
                time.sleep(1)                       
                message_dict['photo'] = {
                    'file_id': photo.id,
                    'file_unique_id': photo.access_hash,
                    'path': path
                }
                
                
                
            if message.media:
             message_dict['media'] = []
             if isinstance(message.media, list):
               print(f"message.media.list")
               for media in message.media:
                 media_info = {}
                 if isinstance(media, MessageMediaPhoto):
                   path = await client.download_media(media, output)
                   media_info = {
                    'type': 'photo',
                    'file_id': media.photo.id,
                    'file_unique_id': media.photo.access_hash,
                    'path': path  #
                   }
                   message_dict['media'].append(media_info)            
###以下没有也会报错 MessageMediaDocument 


                 elif isinstance(media, MessageMediaDocument):
                   document = media.document


###
             else:
              message_dict['documents'] = []
              print(f"message.media.one")
              media = message.media
              if isinstance(media, MessageMediaPhoto):
                print(f"message.media.one.photo")
                photo = media.photo
            #    path = await client.download_media(media, output)上面已经下载过)
              elif isinstance(media, MessageMediaDocument):
                print(f"message.media.one.document")                
                document = media.document
                print(document.mime_type)
                if not (document.mime_type == 'video/mp2t' or document.mime_type == 'audio/flac'):
      # 下载文件
                  path = await client.download_media(document, output) # 下载文件
                
                media_info = {
                    'type': 'document',
                    'file_id': document.id,
                    'file_unique_id': document.access_hash,
                    'path': path  #
                   }
                message_dict['documents'].append(media_info)            
            all_messages.append(message_dict)

        offset_id = history.messages[-1].id
        print(f"Fetched messages: {len(all_messages)}")
    return all_messages
    
async def main():
    """
    主程序：从指定频道获取消息并保存到 JSON 文件中。
    """
    await client.start()  # 启动 Telegram 客户端
    print("Client Created")

    channel_username = CHANNEL_USERNAME  # 你要抓取的 Telegram 频道用户名 #用户名id，比如 comeloveme # 收藏夹，也就是me #频道
    all_messages = await fetch_messages(channel_username)  # 获取消息
#    json不能导出timestamp也就是 message.date
    # 导出消息到 JSON 文件
    await export_to_json('channel_messages.json', all_messages)

# 当该脚本作为主程序运行时
if __name__ == '__main__':
    client.loop.run_until_complete(main())
