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


def GetNutrition(file):
    '''
    File should follow Naomi Goodnight's format (all comma-separated):
        Link
        Title
        TotalTime
        Ingredients
    '''

    # Access scraped data
    with open(file, encoding='utf-8') as f:
        next(f)

        i = 0 # KILL

        for line in f:
            # Error handling for UnicodeDecodeError and IndexError
            try:

                recipe = re.split(',\"|\",', line)
                recipe = [j.strip('"') for j in recipe] # Removes redundant parenthesis
                del recipe[-1] # Deletes newline

                # Switching link and title position
                recipe_link = recipe[0]
                recipe_title = recipe[1]
                recipe[0] = recipe_title
                recipe[1] = recipe_link

            except:
                continue

            # Make dataframe consisting of all ingredients and nutrition data
            column_names = ["Ingredients",
                            "Weight",
                            "Calories (kcal)",
                            "Calories from Fat (kcal)",
                            "Total Fat (g)",
                            "Saturated Fat (g)",
                            "Trans Fat (g)",
                            "Cholesterol (mg)",
                            "Sodium (mg)",
                            "Total Carbohydrate (g)",
                            "Dietary Fiber (g)",
                            "Sugars (g)",
                            "Protein (g)",
                            "Vitamin A (% DV)",
                            "Vitamin C (% DV)",
                            "Calcium (% DV)",
                            "Iron (% DV)"]

            # For each ingredient, figure out whether has quantity, weight, or none




            ingredients_df = pd.DataFrame(data=recipe)#, columns=column_names)
            print(ingredients_df)

            i += 1 # KILL
            if i == 1: # KILL
                break # KILL



    # return ' ~~~ '.join(recipe) # KILL???




print(GetNutrition("recipe_output_new.csv"))


### CITATIONS ###
# USDA
# https://www.fda.gov/food/labelingnutrition/ucm274593.htm
