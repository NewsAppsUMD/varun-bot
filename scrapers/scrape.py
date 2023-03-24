import os
from datetime import datetime, timedelta
from dateutil.parser import parse
from dateutil.tz import gettz
import requests
from bs4 import BeautifulSoup

from slack import WebClient
from slack.errors import SlackApiError

slack_token = os.environ.get('SLACK_API_TOKEN')
client = WebClient(token=slack_token)

def last_updated(soup):
    return soup.find('meta', {'property': 'article:modified_time'}).get('content')

def soupify(url):
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    if response.status_code == 429:
      time.sleep(int(response.headers["Retry-After"]))
      r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    return BeautifulSoup(r.text, "html.parser") 

def coaching_changes():
    url = "https://varunshankar1.github.io/"
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    json = r.json()
    if parse(json['modified']) > datetime.now() - timedelta(hours=1):
        msg = "Churchill has potentially changed coaches, see https://churchillathletics.com/coaches-directory/"
        try:
            response = client.chat_postMessage(
                channel="slack-bots",
                text=msg,
                unfurl_links=True, 
                unfurl_media=True
            )
            print("success!")
        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"]
            print(f"Got an error: {e.response['error']}")

if __name__ == "__main__":
    coaching_changes()
