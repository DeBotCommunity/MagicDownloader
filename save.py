# Module by DeCoded
# EW: https://endway.su/@decoded
# TG: https://t.me/whynothacked
# Канал с модулями: https://t.me/DeBot_userbot

import json

import aiohttp
from telethon import events
from pytube import YouTube

from userbot import client

info = {'category': 'tools', 'pattern': ".save", 'description': 'Скачать видео из TikTok'}

class CobaltModule:
    def __init__(self) -> None:
        self.url = 'https://co.wuk.sh/api/json'
    async def get_download_link(self, data):
        headers = {
            'Content-Type':'application/json',
            'Accept':'application/json',
            'host':'co.wuk.sh',
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, json=data, headers=headers) as response:
                return json.loads(await response.text()).get('url')
            
    async def check_bytes_count(self, size_b):
        return size_b / (1024 * 1024) < 50

    async def download(self, link):
        if not 'youtube.com' in link:
            data = {"url": link, "aFormat": "mp3", "dubLang": False, "vQuality": "1080", "isNoTTWatermark": True}
            url = await self.get_download_link(data)
            return await self.download_media_file(str(url))
        else:
            yt = YouTube(link)
            stream = yt.streams.first()
            content = stream.download()
            if await self.check_bytes_count(len(content)):
                return content
    

    async def download_media_file(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    
                    content = await response.read()
                    
                    if await self.check_bytes_count(len(content)):
                        return content


cobalt = CobaltModule()


@client.on(events.NewMessage(outgoing=True, pattern=".save ?(.*)"))
async def save(event: events.NewMessage.Event):
    link = event.pattern_match.group(1).replace('http://', 'https://')
    await event.delete()
    if link == '':    
        return
    print("-> [.save]")
    try:
        content = await cobalt.download(link)
    except aiohttp.client_exceptions.InvalidURL:
        await client.send_message(f'🔴 Не удалось скачать файл по ссылке: <code>{link}</code>')
    if content != False:
        try:
            await client.send_file(entity=event.chat_id, file=await client.upload_file(file=content, file_name='video.mp4'), video_note=True)
        except:
            pass
