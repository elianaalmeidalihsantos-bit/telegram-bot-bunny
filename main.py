from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os
import requests

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
session_string = os.getenv("SESSION_STRING")

bunny_api_key = os.getenv("CHAVE_API_BUNNY")
library_id = os.getenv("ID_DA_BIBLIOTECA_DO_COELHO")

client = TelegramClient(StringSession(session_string), api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    # Só funciona no privado. Ignora canal/grupo.
    if not event.is_private:
        return

    if not event.video and not event.document:
        return

    try:
        await event.reply("Baixando vídeo...")

        file_path = await event.download_media()
        title = os.path.basename(file_path)

        create_video = requests.post(
            f"https://video.bunnycdn.com/library/{library_id}/videos",
            headers={"AccessKey": bunny_api_key},
            json={"title": title}
        )

        video_id = create_video.json()["guid"]

        await event.reply("Enviando para o Bunny...")

        with open(file_path, "rb") as video_file:
            upload = requests.put(
                f"https://video.bunnycdn.com/library/{library_id}/videos/{video_id}",
                headers={
                    "AccessKey": bunny_api_key,
                    "Content-Type": "application/octet-stream"
                },
                data=video_file
            )

        os.remove(file_path)

        if upload.status_code == 200:
            await event.reply(f"Enviado para o Bunny. ID: {video_id}")
        else:
            await event.reply("Erro no upload para o Bunny.")

    except Exception as e:
        await event.reply(f"Erro: {e}")

print("Telethon online")
client.start()
client.run_until_disconnected()
