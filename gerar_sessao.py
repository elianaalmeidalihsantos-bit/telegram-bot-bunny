from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import os

api_id = int(input("Digite API_ID: "))
api_hash = input("Digite API_HASH: ")
phone = input("Digite telefone com 55: ")

with TelegramClient(StringSession(), api_id, api_hash) as client:
    client.start(phone=phone)
    print("SESSION_STRING:")
    print(client.session.save())
