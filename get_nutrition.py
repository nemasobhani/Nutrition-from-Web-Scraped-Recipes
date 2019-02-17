# Nema Sobhani
# Nutrition from Web Scraped Recipes
# https://github.com/nemasobhani/Nutrition-from-Web-Scraped-Recipes

'''
This script will return the following from a .txt file containing web scraped
recipe information as collected by Naomi Goodnight (partner on this project):

(all " ~~~ ", and all nutritional totals adjusted by weight if given)

Recipe title
Link to recipe
Total time (in minutes)
All ingredients

Separator to indicate ingredients are finished (' ~^~ ')

Calories (kcal)
Calories from Fat (kcal)
Total Fat (g)
Saturated Fat (g)
Trans Fat (g)
Cholesterol (mg)
Sodium (mg)
Total Carbohydrate (g)
Dietary Fiber (g)
Sugars (g)
Protein (g)
Vitamin A (% DV)
Vitamin C (% DV)
Calcium (% DV)
Iron (% DV)

***All nutrition organized following fda.gov nutrition fac guidelines***
'''


# Import Statements
import re
import pandas as pd


def ScrapedRecipeNutrition(file):
    '''
    File should follow Naomi Goodnight's format (all comma-separated):
        Link
        Title
        TotalTime
        Ingredients
    '''

    # Access scraped data
    with open(file, encoding='cp437') as f:
        next(f)

        i = 0 # KILL

        for line in f:
            # If UnicodeDecodeError handling required, add try/raise block here
            print(line) # KILL

            recipe = re.split(',\"|\",', line)
            recipe = [j.strip('"') for j in recipe] # Removes redundant parenthesis
            del recipe[-1] # Deletes newline

            # Switching link and title position
            recipe_link = recipe[0]
            recipe_title = recipe[1]
            recipe[0] = recipe_title
            recipe[1] = recipe_link

            print(recipe) # KILL

            i += 1 # KILL
            if i == 1: # KILL
                break # KILL

            # Make dataframe consisting of all ingredients and nutrition data

    # return ' ~~~ '.join(recipe) # KILL???


# UnicodeDecodeError Handling



print(ScrapedRecipeNutrition("recipe_output_new.csv.txt"))


### CITATIONS ###
# USDA
# https://www.fda.gov/food/labelingnutrition/ucm274593.htm
