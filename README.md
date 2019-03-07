# Nutrition-from-Web-Scraped-Recipes

We are using the web scraper, [beautiful soup](https://www.crummy.com/software/BeautifulSoup/), to pull all recipes from a multitude of food websites, followed by the scraping of those individual sites using an established package from [github](https://github.com/hhursev/recipe-scrapers). We will analyze the nutritional content (from the USDA) of recipes found on a large dataset of online recipes and give comparisons accordingly.

##### Contribution from Nema Sobhani:


## 1. Team Members and Project Objective

**Team Members**
- Nema Sobhani
- Naomi Goodnight

**Objective**
We are using the web scraper, [beautiful soup](https://www.crummy.com/software/BeautifulSoup/), to pull all recipes from a multitude of food websites, followed by the scraping of those individual sites using an established package from [github](https://github.com/hhursev/recipe-scrapers). We will analyze the nutritional content (from the USDA) of recipes found on a large dataset of online recipes and give comparisons accordingly.


## 2. Data Set Attributes (Nema Sobhani)

**Attributes**  
Typical USDA food descriptions look like this:  

\~10123\~^\~1000\~^\~Pork,cured,bacon,unprepared\~^\~PORK,CURED,BACON,UNPREP\~^\~\~^\~\~^\~Y\~^\~\~^0^\~\~^6.25^4.27^9.02^3.87

The description will inform the data of the food and allows to locate information in the USDA nutrition data file (each three digit number indicates what type of nutritional data, such as Calories, Protein, Carbs, Fats, etc):  

\~10123\~^\~203\~^12.62^18^0.247^\~1\~^\~A\~^\~\~^\~\~^1^10.50^14.70^14^12.093^13.150^\~2, 3\~^05/2012^  
\~10123\~^\~204\~^39.69^18^1.165^\~1\~^\~A\~^\~\~^\~\~^1^32.60^49.20^13^37.172^42.206^\~2, 3\~^05/2012^  
\~10123\~^\~205\~^1.28^0^^\~4\~^\~NC\~^\~\~^\~\~^^^^^^^\~\~^05/2012^ ...and so on...  

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
- Analysis approach  
- Visualization  
- Write-up  
- Jupyter Notebook  

- Generate Questions  
    - Naomi  
        - Word Cloud and Frequencies  
    - Nema  
        - Drop outliers (start high)  
        - Standard Numeric Analysis (Max/Min/Mean/Median/Mode)  
    - Fun  
        - TBD  
    
- Paper  
        - Methods  
            - Code efficiency  
        - Numeric Summaries  
        - Visualization Summaries  
        - Troubleshooting / Optimization / Assumptions  
        - Discussion  
            - Accuracy  
            - What we learned  
            - Moving forward  

Timeline (do by):  
Monday, 3/11 - Raw Data Analysis Finished and meet up at 1:30pm (DISTILLATION SESSION) Assign Paper  
Tuesday, 3/12 - <After class> Presentation Outline!  


