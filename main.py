from telethon import TelegramClient, events
import os
import requests

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
phone = os.getenv("TELEGRAM_PHONE")

bunny_api_key = os.getenv("CHAVE_API_BUNNY")
library_id = os.getenv("ID_DA_BIBLIOTECA_DO_COELHO")

client = TelegramClient("session", api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    if event.video or event.document:
        try:
            await event.reply("Recebi o vídeo 👀")

            file_path = await event.download_media()

            video_name = os.path.basename(file_path)

            headers = {
                "AccessKey": bunny_api_key,
                "Content-Type": "application/octet-stream"
            }

            create_video = requests.post(
                f"https://video.bunnycdn.com/library/{library_id}/videos",
                headers={"AccessKey": bunny_api_key},
                json={"title": video_name}
            )

            video_id = create_video.json()["guid"]

            with open(file_path, "rb") as video_file:
                upload = requests.put(
                    f"https://video.bunnycdn.com/library/{library_id}/videos/{video_id}",
                    headers=headers,
                    data=video_file
                )

            if upload.status_code == 200:
                await event.reply("Enviado para o Bunny ✅")
            else:
                await event.reply("Erro ao enviar para o Bunny.")

        except Exception as e:
            print(e)
            await event.reply(f"Erro: {str(e)}")

client.start(phone)
print("Bot online 🚀")
client.run_until_disconnected()
