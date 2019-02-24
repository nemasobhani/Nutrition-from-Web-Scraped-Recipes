# Nema Sobhani
# Nutrition from Web Scraped Recipes
# https://github.com/nemasobhani/Nutrition-from-Web-Scraped-Recipes

'''
This script will return the following from a .txt file containing web scraped
recipe information as collected by Naomi Goodnight (partner on this project):

(all separated by " ~~~ ", and all nutritional totals adjusted by weight if given)

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

***This is not exact! Many false assumptions are made to keep things simple!***
Assumptions:
    1 gram = 1 ml
    All density = water
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

    # Create dictionary storing all possible measurements and conversion to grams
    # https://www.exploratorium.edu/cooking/convert/measurements.html
    measurement = ({'teaspoon':5, 'tsp':5, 'tablespoon':15, 'tbsp':15,
                    'ounce':28, 'oz':28, 'cup':250, 'pint':500, 'pt':500,
                    'quart':1000, 'qt':1000, 'gallon':4000, 'gal':4000,
                    'pound':453.592, 'lb':453.592, 'gram':1, 'kilogram':1000,
                    'milliliter':1, 'liter':1000})
    measurement_keys = list(measurement.keys())

    # Create dictionary to handle fractions and fractional unicode
    fractional = ({'1/2':str(1/2), '1/3':str(1/3), '2/3':str(2/3), '1/4':str(1/4),
                    '3/4':str(3/4), '1/8':str(1/8), '½':str(1/2), '⅓':str(1/3),
                    '⅔':str(2/3), '¼':str(1/4), '¾':str(3/4), '⅛':str(1/8)})
    fractional_keys = list(fractional.keys())

    # Access scraped data
    with open(file, encoding='utf-8') as f:

        for blah in range(0, 10000, 1000):# KILL
            next(f) # KILL

        z = 0 # KILL

        for line in f:
            # Error handling for UnicodeDecodeError and IndexError
            try:

                print(line) # KILL

                # Split on parenthesis and commas with no space around them
                recipe = re.split(',\"|\",|,(?=\S)', line) # Use (?<=\S) before comma?
                recipe = [i.strip('"') for i in recipe] # Removes redundant parenthesis
                del recipe[-1] # Deletes newline
                recipe = list(filter(None, recipe)) # Removes empty elements

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

                grams = None
                qty = None

                # Check if fractional unicode in first or second element and convert
                for i in range(2):
                    for key in fractional_keys:
                        if key == ingredient_list[i]:
                            ingredient_list[i] = fractional[key]
                            break
                        if key in ingredient_list[i]:
                            idx = ingredient_list[i].find(key)
                            if ingredient_list[i][idx-1].isdigit():
                                ingredient_list[i] = (ingredient_list[i][:idx-1] +
                                                    str(int(ingredient_list[i][idx-1]) +
                                                    float(fractional[key])) +
                                                    ingredient_list[i][idx+1:])
                            else:
                                ingredient_list[i] = (ingredient_list[i][:idx] +
                                                    fractional[key] +
                                                    ingredient_list[i][idx+1:])
                            break

                # Establish quantity
                if ingredient_list[0].isdigit():
                    try:
                        qty = float(ingredient_list[0])
                        ingredient_list[0] = (str(int(ingredient_list[0]) +
                                                float(ingredient_list[1])))
                        del ingredient_list[1]
                        qty = float(ingredient_list[0])
                    except:
                        pass
                else:
                    try:
                        qty = float(ingredient_list[0])
                    except:
                        pass

                # Check for common units of measurement (BBC format)
                if "g/" in ingredient_list[0] and 'kg/' not in ingredient_list[0]:
                    grams = int(ingredient_list[0][0:ingredient_list[0].find('g/')])

                elif "kg/" in ingredient_list[0]:
                    grams = int(ingredient_list[0][0:ingredient_list[0].find('kg/')])/1000

                elif "l/" in ingredient_list[0] and 'ml/' not in ingredient_list[0]:
                    grams = int(ingredient_list[0][0:ingredient_list[0].find('l/')])/1000

                elif "ml/" in ingredient_list[0]:
                    grams = int(ingredient_list[0][0:ingredient_list[0].find('ml/')])

                # If quantity exists, convert to grams using measurement dict
                if qty != None:
                    # Check for common units of measurement (UNIVERSAL)
                    for i in range(1,3):
                        for key in measurement_keys:
                            if key in ingredient_list[i]:
                                grams = qty * measurement[key]
                                break



                print(ingredient_list, grams, qty)

            print(recipe)







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




            # z += 1 # KILL
            # if z == 1: # KILL
            #     break # KILL



    # return ' ~~~ '.join(recipe) # KILL???




print(GetNutrition("recipe_output_new.csv"))


### CITATIONS ###
# USDA
# https://www.fda.gov/food/labelingnutrition/ucm274593.htm
