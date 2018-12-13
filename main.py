from bs4 import BeautifulSoup
from save_to_file import save_to_file
from save_to_file import delete_contents
from save_to_file import read_file
from check_latest_link import check_latest_link
from gitcommit import git_commit
import os
import discord
import asyncio
import threading
import requests

news_links = []
url = 'http://maplestory2.nexon.net/en/news/'
r  = requests.get(url)
data = r.text
soup = BeautifulSoup(data, features="html.parser")
client = discord.Client()
token = os.environ.get("DISCORD_BOT_SECRET")
channel_id = os.environ.get("CHANNEL_ID") 

def parse_links():
    for link in soup.find_all('a', {"class": "news-item-link"}):
      news_links.append('http://maplestory2.nexon.net' + link.get('href'))
      return(news_links)

@client.event
async def task():
    await client.wait_until_ready()
    print('Running')
    while True:
      channel = discord.Object(id=channel_id)
      news_links = parse_links()
      last_saved_link = check_latest_link()
      #print(last_saved_link)
      #print(news_links[0])
      print('Running')
      await asyncio.sleep(500)
      if last_saved_link != news_links[0]:
        read_file()
        delete_contents()
        save_to_file(news_links[0])
        git_commit()
        await client.send_message(channel, news_links[0])
        #await asyncio.sleep(500)

def handle_exit():
    print("Handling")
    client.loop.run_until_complete(client.logout())
    for t in asyncio.Task.all_tasks(loop=client.loop):
        if t.done():
            t.exception()
            continue
        t.cancel()
        try:
            client.loop.run_until_complete(asyncio.wait_for(t, 5, loop=client.loop))
            t.exception()
        except asyncio.InvalidStateError:
            pass
        except asyncio.TimeoutError:
            pass
        except asyncio.CancelledError:
            pass

while True:
    @client.event
    async def on_message(m):
        if m.content == 'die':
            print("Terminating")
            raise SystemExit

    @client.event
    async def on_message(message):
      if message.content.startswith('!latest'):
        await client.send_message(message.channel, news_links[0])

    client.loop.create_task(task())
    try:
        client.loop.run_until_complete(client.start(token))
    except SystemExit:
        handle_exit()
    except KeyboardInterrupt:
        handle_exit()
        client.loop.close()
        print("Program ended")
        break

    print("Bot restarting")
    client = discord.Client(loop=client.loop)
	
client.run(token)
