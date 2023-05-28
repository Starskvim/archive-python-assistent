import os
import random
import string
from FastTelethonhelper import fast_upload, fast_download
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument

from config import username, api_id, api_hash

client = TelegramClient(username, api_id, api_hash)
client.start()

download_folder = 'downloads/'
os.makedirs(download_folder, exist_ok=True)

prev_messages = []


def generate_random_name(length):
    """Generate a random string of a given length."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


@client.on(events.NewMessage)
async def handle_new_message(event):
    global prev_messages
    message = event.message
    if message.media:
        if isinstance(message.media, MessageMediaPhoto):
            prev_messages.append(message)
        elif isinstance(message.media, MessageMediaDocument):
            file_name = os.path.splitext(message.media.document.attributes[0].file_name)[0]
            print("================\nСкачиваю\n" + file_name + "\n===============\n")
            for message_photo in prev_messages:
                await client.download_media(message_photo.media.photo, file=os.path.join(download_folder, file_name,
                                                                                         generate_random_name(
                                                                                             20) + ".jpg"))
            prev_messages = []
            await fast_download(client, message)

client.run_until_disconnected()
