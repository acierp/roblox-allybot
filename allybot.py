
import requests
import threading
from itertools import cycle
import termcolor
import json
import time
import random
import string
import os
os.system('color')

scraped = []
currenttoken = []

with open('config.json', 'r+', encoding='utf-8') as f:
    config = json.load(f)

with open('proxies.txt','r+', encoding='utf-8') as f:
    ProxyPool = cycle(f.read().splitlines())

cookie = config['cookie']
selfgroupid = config['selfgroupid']
threads = config['threads']


keywords = ['Military', 'Roleplay', 'Fan', 'Fun', 'Youtube', 'Games', 'Roblox', 'Productions', 'Hi', 'Noob', 'Raid', 'Group', 'difficult', 'easy', 'fun', 'funny', 'hard', 'friend', 'cool', 'fortnite', 'hotel', 'cafe', 'gamer', 'fall guys', 'minecraft', 'vibin', 'i love her..', 'shes my world..', '❤️', '😐', 'dm me please', 'hiiiii', "Coder", "Vegan", "Man", "Hacker", "Horse", "Bear", 'lol', 'X', 'famous', '!!!', '   ', 'isnot', 'me', 'help', 'FN', 'MINECRAFT', 'minecraft', 'fortnite', 'PUBG', 'rust', 'CSGO', 'csgo', ' hi there', ' dm me!', ''"Goat", "Goblin", "Learner", "Killer", "Woman", "Programmer", "Spy", "Stalker", "Spooderman", "Carrot", "Goat", "Quickscoper", "Quickscoper", "C#", "lol", 'funny', 'dead', 'TV', 'epic', '23', '656', '1234', '124', '1202', '🎃', '0', 'vie', 'via', 'cier', 'virtual', 'smh', 'pain', 'depress', 'sub', 'YT', 'DOE', ' Water', 'lis', 'hi', ' !', 's', 'vs', 'FUNNY', 'meme', 'guy', 'man', 'nigga', 'black', "Super", "Retarded", "Great", "Sexy", "Vegan", "Brave", 'X' "Shy", "Cool", 'YOUTUBE', 'YT', 'TTV', 'Twitch' "Poor", "Rich", "Fast", "Gummy", "Yummy", "Masked", "Unusual", "American", "Bisexual", "MLG", "Mlg", "lil", "Lil", "Bro", "Fortnite", "Red", "Ball", "Simp", ".", "$", "!", "al", "ban", "funny", 'epic', 'boi', 'bark', 'dy', 'rd', 'by', 'ac', 'icon', 'joes', 'linus', 'python', 'snake', 'liquid', 'pro', 'metro', 'nic', 'acier', 'ace', 'Nut', 'Ice', 'PS', 'pup', 'BRO', 'RAY', 'system', 'tim', 'theo', 'void', 'yellow', 'skia', 'Festive', 'Why', 'XD', 'homo', 'HA','Beauty','Twig','Cindy Lou Who','Tomcat','Stud','Loosetooth','Harry Potter','Rabbit','Gummi Bear','Tank','Fun Dip','Coke Zero','Raisin','Daria','Cowboy','Chump','Dragonfly','Headlights','Bossy','Big Nasty','Tough Guy','Duckling','Buckeye','Amour','Fatty','Smirk','Mini Me','Autumn','Cheesestick','Amigo','Salt','Diesel','Doctor','Foxy','Swiss Miss','Bumblebee','Midge','Captain','Diet Coke','Music Man','Belch','C-Dawg','Beast','Princess','Buck','Lovely','Prego','Freak','Bunny Rabbit','Carrot','Heisenberg','Cello','Homer','Coach','Cumulus','Gummy Pop','Winnie','Turkey','Bambino','Bubbles','Dorito','Captain Crunch','Pixie Stick','Filly Fally','Backbone','Silly Sally','Pinata','Buzz','Peppa Pig','Halfling','Hubby','Crumbles','Cutie Pie','Tootsie','Twiggy','Dummy','Cookie Dough','Muscles','Oompa Loompa','Chewbacca','Mini Skirt','Bumpkin','Boo Bug','Baby Maker','Cutie','Piglet','Piggy','Dragon','Bean','Beetle','Dimples','Mimi','Bug','Silly Gilly','Rapunzel','Admiral','Brown Sugar','Ringo','Amiga','Nerd','Guy','Junior','Cuddles','Twizzler','Biffle','Lefty','Ginger','Hot Sauce','Pookie','Fiesta','Fifi','Shrinkwrap','Tater','Fun Size','Baldie','Chili','Teeny','Bubba','Redbull','Chubs','Short Shorts','Mouse','Bebe','Dum Dum','Dino','Sugar','Fattykins','Bridge','Dottie','Creep','Herp Derp','Baby Bird','Cruella','Peppermint','Buttercup','Smoochie','Lover','Weirdo','Snoopy','Dulce','Con','Dirty Harry','Brutus','Weiner','Donuts','Braniac','Skinny Minny','Goose','Matey','Cottonball','Candycane','Chuckles','Grease','Barbie','Queenie','Papito','Boo Bear''Rosebud','Lil Mama','Dot','Bud','Honeybun','Figgy','Pork Chop','Angel','Skinny Jeans','Hulk','Miss Piggy','Lion','General','Frauline','Chickie','Senior','Giggles','Marge','Lil Girl','Gordo','Shorty']

def tokenUpdater(cookie):
    cookies = {
        ".ROBLOSECURITY": cookie
    }
    try:
        r = requests.post("https://auth.roblox.com/v1/logout", cookies=cookies)
    except:
        print('Proxy error')
        pass
    if r.status_code == 200 or r.status_code == 403:
        currenttoken.clear()
        currenttoken.append(r.headers['x-csrf-token'])
        print('Successfully updated token')
    else:
        print('Error when updating token')
def sendRequest(selfgroup, cookie, proxy, groupid):
    cookies = {
        ".ROBLOSECURITY": cookie
    }
    headers = {
        "x-csrf-token": currenttoken[0],
        "connection":"keep-alive"
    }
    proxy = {
        "https": "https://" + next(ProxyPool)
    }
    try:
        r = requests.post(f'https://groups.roblox.com/v1/groups/{selfgroup}/relationships/allies/{groupid}', cookies=cookies, proxies=proxy, headers=headers)
    except:
        print('Proxy error')
        pass
    if r.status_code == 200:
        print(f'Successfully sent ally request to {groupid}!')
    elif r.status_code == 400:
        print('Ally request was already sent to the scraped group.')
    elif "TooManyRequests" in r.text:
        proxy = {
        "https": "https://" + next(ProxyPool)
        }
        return sendRequest(selfgroup, cookie, proxy, groupid)
    if 'Token Validation' in r.text:  
        tokenUpdater(cookie)
                    
def scrapeGroups(cookie, proxy, keyword, cursor=None):
    proxy = {
        "https": "https://" + next(ProxyPool)
    }
    cookies = {
        ".ROBLOSECURITY": cookie
    }
    if cursor == None:
        try:
            r = requests.get(f'https://groups.roblox.com/v1/groups/search?keyword={keyword}&limit=100', headers={"connection":"keep-alive"}, cookies=cookies, proxies=proxy).json()
        except:
            print('Proxy error')
            pass
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
        try:
            r = requests.get(f'https://groups.roblox.com/v1/groups/search?keyword={keyword}&limit=100&cursor={cursor}', cookies=cookies, headers={"connection":"keep-alive"}, proxies=proxy).json()
        except:
            print('Proxy error')
            pass
        for breadchill in r['data']:
            squeakalusnoob = breadchill['id']
            print(f'Successfully scraped {squeakalusnoob}')
            sendRequest(selfgroupid, cookie, proxy, squeakalusnoob)
            try:
                cursor = r['nextPageCursor']
                return scrapeGroups(cookie, proxy, keyword, cursor)
            except KeyError:
                print('Finished checking all pages on a single thread.')

def scrapeRandom(cookie):
    while True:
        proxy = {
            "https": "https://" + next(ProxyPool)
        }
        groupid = ('').join(random.choices(string.digits, k=7))
        try:
            sendRequest(selfgroupid, cookie, proxy, groupid)
        except KeyError:
            print('Random error')
            pass
        except:
            print('Proxy error')
            sendRequest(selfgroupid, cookie, proxy, groupid)
print('''
acier ally bot

[1] Scrape by keyword
[2] Scrape by random group''')
choice = input('Choice: ')
if "1" in choice:
    tokenUpdater(cookie)
    for key in keywords:
        proxy = {
            "https": "https://" + next(ProxyPool)
        }
        threading.Thread(target=scrapeGroups, args=[cookie, proxy, key]).start()
elif "2" in choice:
    tokenUpdater(cookie)
    for _ in range(int(threads)):
        proxy = {
            "https": "https://" + next(ProxyPool)
        }
        threading.Thread(target=scrapeRandom, args=[cookie]).start()
