from recipe_scrapers import scrape_me
#https://github.com/hhursev/recipe-scrapers
from bs4 import BeautifulSoup
import sys
# import csv
import re
import requests
import datetime

tic = datetime.datetime.now()
in_file = 'bonappetitextra.csv'
out_file = 'bonappetit_output.csv'
#Header Row
with open(out_file, "w") as output:
    output.write(f'Link,Title,TotalTime,Ingredients\n')

i=0 #for myself
with open(in_file, "r") as source:
    for line in source:
        print(i)
        scraper = scrape_me(f'{line.strip()}')
        with open(out_file, "a") as output:
            output.write(f'{line.strip()},')
            #To handle commas within site text
            output.write(f'"{scraper.title()}",')
            output.write(f'{scraper.total_time()},')
            # ing = scraper.ingredients()
            for ing in scraper.ingredients():
                output.write(f'"{ing}",')
            output.write('\n')
        # print(scraper.instructions())
        # print(scraper.links())
        i += 1
toc = datetime.datetime.now()
print(toc-tic)


# scraper = scrape_me('https://hellofresh.com/recipes/pineapple-poblano-beef-tacos-5c1aa173e3f33930297e3fd7')
# print(scraper.title())
# print(scraper.total_time())
# print(scraper.ingredients())
# print(scraper.instructions())
# print(scraper.links())
