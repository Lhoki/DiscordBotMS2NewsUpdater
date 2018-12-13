import requests

def check_latest_link():
  res = requests.get('https://raw.githubusercontent.com/Lhoki/DiscordBotMS2NewsUpdater/master/last_update.txt')
  content = res.text
  return(content)



