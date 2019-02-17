# Nutrition-from-Web-Scraped-Recipes

We are using the web scraper, "beautiful soup" (https://www.crummy.com/software/BeautifulSoup/), to pull all recipes from a multitude of food websites, followed by the scraping of those individual sites using an established package from github (https://github.com/hhursev/recipe-scrapers). We will analyze the nutritional content (from the USDA) of recipes found on a large dataset of online recipes and give comparisons accordingly.

##### Contribution from Nema Sobhani:


## 1. Team Members and Project Objective

**Team Members**
- Nema Sobhani
- Naomi Goodnight

**Objective**
We are using the web scraper, "beautiful soup" (https://www.crummy.com/software/BeautifulSoup/), to pull all recipes from a multitude of food websites, followed by the scraping of those individual sites using an established package from github (https://github.com/hhursev/recipe-scrapers). We will analyze the nutritional content (from the USDA) of recipes found on a large dataset of online recipes and give comparisons accordingly.


## 2. Data Set Attributes

Attributes
- Item
  - Corn, Milk, Chicken
- Calories
  - 250, 1000
- Protein
  - 10, 20

*Noise*: Each item has multiple different versions. For example, corn may be raw, on the cob, canned. These will have to be parsed carefully to yield the correct item. Another form of noise is that weights may vary, as well as percentage of daily value, all of which will have to be normalized.
