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
        for i in range(41002):# KILL
            next(f) # KILL

        z = 0 # KILL

        for line in f:
            # Error handling for UnicodeDecodeError and IndexError
            try:

                print(line) # KILL
                recipe = re.split(',\"|\",|[?<=\w],[?=\w]', line)
                recipe = [j.strip('"') for j in recipe] # Removes redundant parenthesis
                del recipe[-1] # Deletes newline
                recipe = list(filter(None, recipe))

                print(recipe) # KILL
                # Switching link and title position
                recipe_link = recipe[0]
                recipe_title = recipe[1]
                recipe[0] = recipe_title
                recipe[1] = recipe_link

            except:
                continue

            # Parse ingredients, figuring out whether has quantity, weight, or none
            for ingredient in recipe[3:]:

                ingredient_list = re.split(', | ', ingredient.lower())

                if "g/" in ingredient_list[0] and 'kg/' not in ingredient_list[0]:
                    grams = int(ingredient_list[0][0:ingredient_list[0].find('g/')])

                if "kg/" in ingredient_list[0]:
                    grams = int(ingredient_list[0][0:ingredient_list[0].find('kg/')])/1000

                if "l/" in ingredient_list[0] and 'ml/' not in ingredient_list[0]:
                    grams = int(ingredient_list[0][0:ingredient_list[0].find('l/')])/1000

                if "ml/" in ingredient_list[0]:
                    grams = int(ingredient_list[0][0:ingredient_list[0].find('ml/')])

            #     if ('g/' in ingredient_list[0]
            #         or "kg/" in ingredient_list[0]
            #         or "l/" in ingredient_list[0]
            #         or "ml/" in ingredient_list[0]):
            #         print(ingredient_list)
            #         print(grams)
            #
            #     print(ingredient)
            # print(recipe)







            # ingredients_df = pd.DataFrame(data=recipe)#, columns=column_names)


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




            z += 1 # KILL
            if z == 1: # KILL
                break # KILL



    # return ' ~~~ '.join(recipe) # KILL???




print(GetNutrition("recipe_output_new.csv"))


### CITATIONS ###
# USDA
# https://www.fda.gov/food/labelingnutrition/ucm274593.htm
