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
