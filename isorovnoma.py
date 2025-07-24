import asyncio
import hashlib
import traceback
import csv
import aiohttp
import re
import os
from telethon import utils, types, events
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import RequestWebViewRequest
from fake_useragent import UserAgent
import aiohttp_proxy
ovoz_berildi = []
qayta_ovoz = []
ovoz_berilmadi = []
premium_channels = []
# Proxy fayl yo‘li
file_path_1 = r"C:\join\proxyuz.csv"
file_path_2 = r"/storage/emulated/0/giv/proxyuz.csv"


PROXY = "http://u1ad3f1af533a05b5-zone-custom-region-uz:R123456789rQWQR123456789uhdlnax@43.153.237.55:2334"
headers = {
    'user-agent': UserAgent(platforms=["mobile"], os=["Android"], browsers=["Chrome Mobile"]).random
}

# CSVdan avval ovoz bergan raqamlarni yuklab olish
def load_existing_phones(filenames):
    existing = set()
    for filename in filenames:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row:
                        existing.add(row[0])
    return existing

skip_phones = load_existing_phones(["muvaffaqiyatli.csv", "muvaffaqiyatliqaytaovoz.csv"])

# Telefonlar ro'yxatini o'qish
phonecsv = "phone"
with open(f'{phonecsv}.csv', 'r') as f:
    raw_phones = [row[0] for row in csv.reader(f)]

# 998 bilan boshlanmaydigan va avval ovoz bergan raqamlarni chiqarib tashlash
phlist = [p for p in raw_phones if p.startswith("998") and p not in skip_phones]
print(f"Jami yangi raqamlar: {len(phlist)}")


async def fetch_with_retries(session, url, retries=3, delay=3):
    for attempt in range(1, retries + 1):
        try:
            async with session.get(url, timeout=10) as response:
                content = await response.text()
                print(f"✅ WebView yuklandi (urinish: {attempt})")
                return content
        except Exception as e:
            print(f"⚠️ [{attempt}/{retries}] WebView so‘rov xatoligi: {e}")
            if attempt < retries:
                await asyncio.sleep(delay)
            else:
                raise e


async def main():
    indexx = 0
    for phone in phlist:
        api_id = 22962676
        api_hash = '543e9a4d695fe8c6aa4075c9525f7c57'
        phone = utils.parse_phone(phone)
        indexx += 1
        print(f'\n📱 Raqam: {phone} | Index: {indexx}')

        tg_client = TelegramClient(f'sessions/{phone}', api_id, api_hash)
        last_bot_message = None

        try:
            await tg_client.connect()
            if not await tg_client.is_user_authorized():
                print('❌ Sessiyasi yo‘q raqam')
                continue

            async with tg_client:
                event_received = asyncio.Event()

                @tg_client.on(events.NewMessage(chats="@iSorovnomaBot"))
                async def handler(event):
                    nonlocal last_bot_message
                    if event.message.text:
                        last_bot_message = event.message
                        print("✅ Botdan javob keldi:")
                        event_received.set()

                try:
                    await tg_client(JoinChannelRequest("https://t.me/uchkoprik_axborot_xizmati"))
                    await tg_client(JoinChannelRequest("https://t.me/davlatxizmatchisi_uz"))
                    print("➕ Kanalga a'zo bo‘ldi")
                except Exception:
                    print("❌ Kanalga qo‘shilishda xatolik")

                username = await tg_client.get_entity("@iSorovnomaBot")
                await tg_client.send_message(username, f"/start 607-6035")
                print("🚀 /start 607-6035 yuborildi")

                try:
                    await asyncio.wait_for(event_received.wait(), timeout=30)
                except asyncio.TimeoutError:
                    print("❌ 30 soniyada javob kelmadi")
                    continue

                m = await tg_client.get_messages(username, limit=1)
                await m[0].click(29)
                await asyncio.sleep(3)
                if last_bot_message and "☎️ Raqamni yuborish" in last_bot_message.text:
                    me = await tg_client.get_me()
                    await tg_client.send_file(
                        username,
                        types.InputMediaContact(
                            phone_number=me.phone,
                            first_name=me.first_name,
                            last_name='',
                            vcard=''
                        ),
                        reply_to=last_bot_message.id
                    )
                    print("📇 Kontakt yuborildi")
                    await asyncio.sleep(2)
                else:
                    print("⚠️ Kontakt so‘ralmadi")

                msg = await tg_client.get_messages(username, limit=1)
                buttons = msg[0].reply_markup.rows
                web_view_url = None
                for row in buttons:
                    for button in row.buttons:
                        if isinstance(button, types.KeyboardButtonWebView):
                            web_view = await tg_client(RequestWebViewRequest(
                                peer=username,
                                bot=username,
                                platform='android',
                                from_bot_menu=False,
                                url=button.url
                            ))
                            web_view_url = web_view.url
                            print("🌐 WebView:", web_view_url)

                if not web_view_url:
                    print("❌ WebView topilmadi")
                    continue

                conn = aiohttp_proxy.ProxyConnector.from_url(PROXY)
                async with aiohttp.ClientSession(connector=conn) as http_client:
                    try:
                        ipres = await http_client.get("https://ipinfo.io/json")
                        print("🌍 IP:", (await ipres.json())['ip'])
                    except:
                        print("❌ IP olishda xatolik")

                    content = await fetch_with_retries(http_client, web_view_url)

                match = re.search(r'const url = "(https://t\.me/iSorovnomaBot\?start=[^"]+)"', content)
                if not match:
                    print(f"❌ Start param topilmadi | Content: {content[:100]}...")
                    continue

                start_param = match.group(1).split('start=')[1]
                if start_param.startswith("web_xato-uz_"):
                    raqam = start_param.split("_")[-1]
                    new_param = f"web_bor_{raqam}"
                    print("ℹ️ web_xato bo‘lgani sababli web_bor yuborilyapti")
                else:
                    new_param = start_param

                await tg_client.send_message(username, f"/start {new_param}")
                print(f"✅ /start {new_param} yuborildi")
                event_received.clear()
                try:
                    await asyncio.wait_for(event_received.wait(), timeout=30)
                    print("✅ Yangi javob botdan qabul qilindi")
                except asyncio.TimeoutError:
                    print("❌ 30 soniyada yangi javob kelmadi")
                    continue

                m2 = await tg_client.get_messages(username, limit=1)
                last_msg = m2[0]
                if "❗️Sizning ovozingiz qabul qilinmadi. Siz avval 31-DMTT ga ovoz berib bo‘lgansiz!" in last_msg.text:
                    print("Qayta ovoz")
                    qayta_ovoz.append(phone)
                    with open("muvaffaqiyatliqaytaovoz.csv", "a", newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([phone])
                elif "✅ Sizning bergan ovozingiz muvaffaqiyatli qabul qilindi!" in last_msg.text:
                    print("Ovoz qabul qilindi")
                    ovoz_berildi.append(phone)
                    with open("muvaffaqiyatli.csv", "a", newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([phone])
                else:
                    print(f"Nomalum javob:   {last_msg.text}")
                    ovoz_berilmadi.append(phone)

                s1 = len(ovoz_berildi)
                s2 = len(qayta_ovoz)
                s3 = len(ovoz_berilmadi)
                print(last_msg.text)
                print(f"\n{s1} - ovoz berildi\n{s2} - qayta ovoz\n{s3} - ovoz berilmadi")

        except Exception as e:
            traceback.print_exc()
            print(f"❌ Telefon: {phone} ishlamadi. Xato: {e}")


if __name__ == '__main__':
    asyncio.run(main())
