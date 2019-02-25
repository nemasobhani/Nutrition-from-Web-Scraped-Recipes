# Nutrition-from-Web-Scraped-Recipes

We are using the web scraper, "beautiful soup" (https://www.crummy.com/software/BeautifulSoup/), to pull all recipes from a multitude of food websites, followed by the scraping of those individual sites using an established package from github (https://github.com/hhursev/recipe-scrapers). We will analyze the nutritional content (from the USDA) of recipes found on a large dataset of online recipes and give comparisons accordingly.

##### Contribution from Nema Sobhani:


## 1. Team Members and Project Objective

**Team Members**
- Nema Sobhani
- Naomi Goodnight

**Objective**
We are using the web scraper, "beautiful soup" (https://www.crummy.com/software/BeautifulSoup/), to pull all recipes from a multitude of food websites, followed by the scraping of those individual sites using an established package from github (https://github.com/hhursev/recipe-scrapers). We will analyze the nutritional content (from the USDA) of recipes found on a large dataset of online recipes and give comparisons accordingly.


## 2. Data Set Attributes (Nema Sobhani)

Attributes
- Item
  - Corn, Milk, Chicken
- Calories
  - 250, 1000
- Protein
  - 10, 20

*Noise*: Each item has multiple different versions. For example, corn may be raw, on the cob, canned. These will have to be parsed carefully to yield the correct item. Another form of noise is that weights may vary, as well as percentage of daily value, all of which will have to be normalized.


## 2. Data Set Attributes (Naomi Goodnight)
The recipe scraper provides ingredients as they are written within the websites.  We will need to parse out the amounts from the ingredients themselves and occasionally additional instructions.  (1 10-oz. package frozen blackberries (about 2 cups), thawed) (2 large fresh fennel bulbs, trimmed, each cut vertically into 12 wedges with some core attached)  The amounts and the ingredients will need to be normalized to merge with the nutritional dataset.  


## 3. Tentative Timeline
Topic|Due Date
---|---
Data Collection Complete | Feb 1st   
Data Cleanup Complete | Feb 15th  
Data Transformation, Feature Engineering Complete | Feb 26th
Statistical Summary and Visualization Complete |  Mar 8th  

## 4. Current Micro Next Steps
Altering ingredient outliers
