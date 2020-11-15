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

keywords = ['Military', 'Roleplay', 'Fan']
req = requests.Session()

def tokenUpdater(cookie, proxy):
    cookies = {
        ".ROBLOSECURITY": cookie
    }
    r = req.post("https://auth.roblox.com/v1/logout", cookies=cookies, proxies=proxy)
    if r.status_code == 200 or r.status_code == 403:
        currenttoken.clear()
        currenttoken.append(r.headers['x-csrf-token'])
        print('Successfully updated token')
    else:
        print('Error when updating token')
def sendRequest(selfgroup, cookie, proxy, cursor=None):
    cookies = {
        ".ROBLOSECURITY": cookie
    }
    while True:
        for scrape in scraped:
            headers = {
                "x-csrf-token": currenttoken[0]
            }
            r = req.post(f'https://groups.roblox.com/v1/groups/{selfgroup}/relationships/allies/{scrape}', cookies=cookies, proxies=proxy)
            if r.status_code == 200:
                print(f'Successfully sent ally request to {scrape}!')
                
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
            scraped.append(breadchill['id'])
            try:
                cursor = r['nextPageCursor']
                return scrapeGroups(cookie, proxy, keyword, cursor)
            except KeyError:
                print('Finished checking all pages on a single thread.')
    else:
        r = req.get(f'https://groups.roblox.com/v1/groups/search?keyword={keyword}&limit=100&cursor={cursor}', cookies=cookies, proxies=proxy).json()
        for breadchill in r['data']:
            scraped.append(breadchill['id'])
            try:
                cursor = r['nextPageCursor']
                return scrapeGroups(cookie, proxy, keyword, cursor)
            except KeyError:
                print('Finished checking all pages on a single thread.')

def worker(cookie, proxy):
    for key in keywords:
        scrapeGroups(cookie, proxy, key)

proxy = {
    "https": "https://" + next(ProxyPool)
}
threading.Thread(target=tokenUpdater, args=[cookie, proxy]).start()
for keywordpar in keywords:
    proxy = {
        "https": "https://" + next(ProxyPool)
    }
    threading.Thread(target=worker, args=[cookie, proxy]).start()
for _ in range(50):
    proxy = {
        "https": "https://" + next(ProxyPool)
    }
    threading.Thread(target=sendRequest, args=[selfgroupid, cookie, proxy]).start()
