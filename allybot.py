import requests
import threading
from itertools import cycle
import json
import time

scraped = []
currenttoken = []

with open('config.json', 'r+', encoding='utf-8') as f:
    config = json.load(f)

with open('proxies.txt','r+', encoding='utf-8') as f:
	ProxyPool = cycle(f.read().splitlines())

cookie = config['cookie']
selfgroupid = config['selfgroupid']

keywords = ['Military', 'Roleplay', 'Fan', 'Fun', 'Youtube', 'Games', 'Roblox']
req = requests.Session()

def tokenUpdater(cookie):
    cookies = {
        ".ROBLOSECURITY": cookie
    }
    r = req.post("https://auth.roblox.com/v1/logout", cookies=cookies)
    if r.status_code == 200 or r.status_code == 403:
        currenttoken.append(r.headers['x-csrf-token'])
        print('Successfully updated token')
    else:
        print('Error when updating token')
def sendRequest(selfgroup, cookie, proxy, groupid, cursor=None):
    cookies = {
        ".ROBLOSECURITY": cookie
    }
    headers = {
        "x-csrf-token": currenttoken[0]
    }
    r = req.post(f'https://groups.roblox.com/v1/groups/{selfgroup}/relationships/allies/{groupid}', cookies=cookies, proxies=proxy, headers=headers)
    if r.status_code == 200:
        print(f'Successfully sent ally request to {groupid}!')
                
def scrapeGroups(cookie, proxy, keyword, cursor=None):
    cookies = {
        ".ROBLOSECURITY": cookie
    }
    if cursor == None:
        r = req.get(
            f'https://groups.roblox.com/v1/groups/search?keyword={keyword}&limit=100', cookies=cookies, proxies=proxy).json()
        for breadchill in r['data']:
            squeakalusnoob = breadchill['id']
            print(f'Successfully scraped {squeakalusnoob}')
            sendRequest(selfgroupid, cookie, proxy, squeakalusnoob)
            try:
                cursor = r['nextPageCursor']
                return scrapeGroups(cookie, proxy, keyword, cursor)
            except KeyError:
                print('Finished checking all pages on a single thread.')
    else:
        r = req.get(f'https://groups.roblox.com/v1/groups/search?keyword={keyword}&limit=100&cursor={cursor}', cookies=cookies, proxies=proxy).json()
        for breadchill in r['data']:
            squeakalusnoob = breadchill['id']
            print(f'Successfully scraped {squeakalusnoob}')
            sendRequest(selfgroupid, cookie, proxy, squeakalusnoob)
            try:
                cursor = r['nextPageCursor']
                return scrapeGroups(cookie, proxy, keyword, cursor)
            except KeyError:
                print('Finished checking all pages on a single thread.')

tokenUpdater(cookie)
for key in keywords:
    proxy = {
        "https": "https://" + next(ProxyPool)
    }
    threading.Thread(target=scrapeGroups, args=[cookie, proxy, key]).start()
