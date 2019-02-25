# Nema Sobhani
# Nutrition from Web Scraped Recipes
# https://github.com/nemasobhani/Nutrition-from-Web-Scraped-Recipes

'''
This script will return the following from a .txt file containing web scraped
recipe information as collected by Naomi Goodnight (partner on this project):


Recipe title
Link to recipe
Total time (in minutes)
All ingredients


Calories (kcal)
Calories from Fat (kcal) # OMITTED UNTIL FACTOR CAN BE DETERMINED
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

***All nutrition organized following fda.gov nutritional facts guidelines***

***This is not exact! Many false assumptions are made to keep things simple!***
Assumptions:
    1 gram = 1 ml (all density = water)
    If no quantity or weight given, 50g used by default.
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

        # I'm using this to jump around in the raw data file
        for blah in range(10000):# KILL
            next(f) # KILL

        z = 0 # KILL

        for line in f:
            # Error handling for UnicodeDecodeError and IndexError
            try:

                print(line) # KILL

                # Split on parenthesis and commas with no space after them
                recipe = re.split(',\"|\",|,(?=\S)', line) # Use (?<=\S) before comma?
                recipe = [i.strip('"') for i in recipe] # Removes redundant parenthesis
                del recipe[-1] # Deletes newline
                recipe = list(filter(None, recipe)) # Removes empty elements

                # Switching link and title position
                recipe[0], recipe[1] = recipe[1], recipe[0]

            except:
                continue

            # Parse ingredients, figuring out whether has quantity, weight, or none
            for ingredient in recipe[3:]: # Skips Title, Link, and Time

                ingredient_list = re.split(', | ', ingredient.lower())

                grams = None
                qty = None

                # Check if fractional unicode in first or second element and convert
                for i in range(2):
                    for key in fractional_keys:
                        # Handling standalone fractions
                        if key == ingredient_list[i]:
                            ingredient_list[i] = fractional[key]
                            break
                        # Handling fractions that are attached to another number
                        if key in ingredient_list[i]:
                            idx = ingredient_list[i].find(key)
                            if ingredient_list[i][idx-1].isdigit():
                                # This inserts the summed value into position
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
                        # If first index is a digit, save in variable
                        qty = float(ingredient_list[0])
                        # If first index is a number, and second is a float
                        ingredient_list[0] = (str(int(ingredient_list[0]) +
                                                float(ingredient_list[1])))
                        del ingredient_list[1]
                        qty = float(ingredient_list[0])
                    # If the above crashes, still saved first index as qty
                    # If it doesn't, first two indexes summed and qty overwritten
                    except:
                        pass
                else:
                    # In the case first index is a float
                    try:
                        qty = float(ingredient_list[0])
                    except:
                        pass

                # Check for common units of measurement (BBC format)
                if "g/" in ingredient_list[0] and 'kg/' not in ingredient_list[0]:
                    grams = float(ingredient_list[0][0:ingredient_list[0].find('g/')])

                elif "kg/" in ingredient_list[0]:
                    grams = float(ingredient_list[0][0:ingredient_list[0].find('kg/')])/1000

                elif "l/" in ingredient_list[0] and 'ml/' not in ingredient_list[0]:
                    grams = float(ingredient_list[0][0:ingredient_list[0].find('l/')])/1000

                elif "ml/" in ingredient_list[0]:
                    grams = float(ingredient_list[0][0:ingredient_list[0].find('ml/')])

                # If quantity exists, convert to grams using measurement dict
                if qty != None:
                    # Check for common units of measurement (UNIVERSAL)
                    for i in range(1,3): # Checking second and third indices
                        for key in measurement_keys:
                            if key in ingredient_list[i]:
                                grams = qty * measurement[key]
                                break

                # Get nutrition from USDA database
                '''
                ### TRUNCATE ###
                1. Numeric
                2. Measurements
                3. Stop words

                ### HOW TO MATCH INGREDIENTS TO USDA DATABASE ###

                1. Highest number of matches in ingredient_list line
                2. Shortest length USDA food reference

                My logic here is that the highest matches with the most concise
                ingredient line should be the most accurate. For example, 'bacon'
                may show up in a line of baby food. Naturally there will be many
                other ingredients in that food, while the simplest, shortest
                USDA food that contains bacon, is bacon itself.

                Therefore, we initialize a list that tracks:
                -Counter indicating how many words in the ingredient line match
                -USDA food length
                -USDA food id

                BestMatch = [0, float('inf'), None]

                If our count is higher AND our length is lower, we replace
                BestMatch with that information.

                ex.
                    if count > BestMatch[0] and length < BestMatch[1]:
                        BestMatch = [highercount, shorter food description, food ID]

                FOOD_DESC

                '''


                print(ingredient_list, grams, qty)

            print(recipe)



            # Make dataframe consisting of all ingredients and nutrition data
            column_names = ["Ingredients",
                            "Calories (kcal)",
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

            # ingredients_df = pd.DataFrame(data=recipe), columns=column_names)



            z += 1 # KILL
            if z == 1: # KILL
                break # KILL

print(GetNutrition("recipe_output_new.csv"))



### NOTES ###
'''Will create a dataframe from lists containing all information defined in top
docstring. The lists themselves may be used to create a text file that is easily
converted back to a dataframe, giving broader, more specific uses.

In the case a text file is created from the cleaned scraped data, will follow:

-Title, Link, Time, and Ingredients separated by: ' ~~~ '
-Separator to indicate ingredients are finished: ' ~^~ '
-All nutritional data separated by: ' ~~~ '
'''

### CITATIONS ###
# https://www.ars.usda.gov/northeast-area/beltsville-md-bhnrc/beltsville-human-nutrition-research-center/nutrient-data-laboratory/docs/sr28-download-files/
# https://www.fda.gov/food/labelingnutrition/ucm274593.htm
# https://www.exploratorium.edu/cooking/convert/measurements.html
