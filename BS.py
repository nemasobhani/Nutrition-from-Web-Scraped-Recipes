from recipe_scrapers import scrape_me
from bs4 import BeautifulSoup
import sys
import csv
import re
import requests
import datetime

tic = datetime.datetime.now()
# s = [i for i in range(58)]

# for j in s:
for i in range(438,692):
    print(i)
    # payload = {'content': 'recipe','page': i}
    r = requests.get(f'https://www.bonappetit.com/search?content=recipe&page={i}')#, params=payload)
    # r  = requests.get('http://' + f'www.bonappetit.com/search/dinner?content=recipe&page=2')
    # print(r)
    data = r.text
    # print(data)
    soup = BeautifulSoup(data, 'html.parser')
    with open("bonappetitextra.csv", "a") as f:
        for link in soup.find_all('a', href=True):
            f.write(f'{link.get("href")}\n')
toc = datetime.datetime.now()
print(toc-tic)


#payload = {'page': i}
#r = requests.get('https://www.allrecipes.com/search/results/', params=payload)

# for i in range(1,438):
#     payload = {'content': 'recipe', 'page': i}
#     r = requests.get('https://www.bonappetit.com/search/', params=payload)
