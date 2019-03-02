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

    # Using USDA FD_GROUP IDs, create dict of common items to shorten search later
    FoodGroupID = ({'0100': {'butter', 'cheese', 'cream', 'milk', 'yogurt',
                    'egg', 'eggs'},

                    '0200': {'vinegar', 'allspice', 'anise', 'bay', 'caraway',
                            'cardamom', 'cinnamon', 'cloves',
                            'corriander', 'cumin', 'curry', 'fenugreek',
                            'marjoram', 'nutmeg', 'oregano', 'rosemary',
                            'tarragon', 'tumeric', 'dill', 'salt'},

                    '0400': {'oil', 'margarine', 'shortening', 'mayonnaise'},

                    '0500': {'chicken', 'duck', 'gooose', 'pheasant', 'quail',
                            'squab', 'turkey', 'emu', 'ostrich'},

                    '0600': {'soup', 'sauce', 'gravy', 'broth', 'stock'},

                    '0700': {'sausage', 'bologna', 'bratwurst', 'chorizo',
                            'frankfurter', 'mortadella', 'pastrami', 'pate',
                            'pepperoni', 'salami', 'kielbasa', 'beerwurst',
                            'pancetta'},

                    '0800': {'cereal'},

                    '0900': {'apples', 'apricots', 'avocado', 'avocados',
                            'bananas', 'blackberries', 'cherries', 'blueberries',
                            'boysenberries', 'cranberries', 'currants', 'dates',
                            'elderberries', 'figs', 'gooseberries', 'goji',
                            'grapefruit', 'grapes', 'guavas', 'jackfruit',
                            'kiwis', 'kumquats', 'lemon', 'lime', 'limes',
                            'mangos', 'cantaloupe', 'honeydew', 'mulberries',
                            'nectarines', 'olives', 'oranges', 'tangerines',
                            'papaya', 'papayas', 'passion-fruit', 'peaches',
                            'pears', 'persimmons', 'pineapple', 'plantains',
                            'plums', 'pomegranates', 'prunes', 'quince',
                            'quinces', 'raisins', 'raspberries', 'rhubarb',
                            'strawberries', 'durian', 'clementines', 'nectar'},

                    '1000': {'bacon'},

                    '1100': {'artichoke', 'artichokes', 'bamboo', 'beets', 'bell',
                            'broccoli', 'brussel', 'brussels', 'cabbage',
                            'carrot', 'carrots', 'celeriac', 'celery', 'chard',
                            'chicory', 'chives', 'collard', 'corn', 'cucumber',
                            'cucumbers', 'eggplant', 'eggplants', 'edamame',
                            'garlic', 'kale', 'mushroom', 'mushrooms', 'leek',
                            'leeks', 'lettuce', 'spinach', 'okra', 'onions',
                            'parsnips', 'peas', 'peppers', 'potatoes', 'pumpkin',
                            'radishes', 'rutabagas', 'sauerkraut', 'seaweed',
                            'shallot', 'shallots', 'soybeans', 'squash',
                            'succotash', 'taro', 'tomato', 'tomatoes', 'turnip',
                            'turnips', 'watercress', 'yams','pickles', 'arugula',
                            'cauliflower', 'asparagus', 'zucchini', 'zucchinis',
                            'cilantro', 'jalapeno', 'jalapeño'},

                    '1200': {'seeds', 'nuts', 'almonds', 'brazilnuts', 'cashews',
                            'chestnuts', 'coconut', 'macadamia', 'pecans', 'pine',
                            'pistachios', 'walnuts'},

                    '1300': {'beef', 'brisket'},

                    '1400': {'alcoholic', 'liquor', 'liqueur', 'beer', 'daiquiri',
                            'tea', 'coffee', 'lemonade', 'wine'},

                    '1500': {'anchovy', 'anchovies', 'bass', 'carp', 'caviar',
                            'cod', 'catfish', 'mahimahi', 'eel', 'grouper',
                            'haddock', 'halibut', 'herring', 'mackerel',
                            'monkfish', 'mullet', 'perch', 'pike', 'pollock',
                            'rockfish', 'roe', 'roughy', 'salmon', 'sardine',
                            'sardines', 'trout', 'smelt', 'snapper', 'sturgeon',
                            'swordfish', 'tuna', 'whitefish', 'crab', 'crabs',
                            'crayfish', 'lobster', 'lobsters', 'shrimp',
                            'abalone', 'clam', 'clams', 'mussels', 'octopus',
                            'osyters', 'scallops', 'squid', 'tilapia'},

                    '1600': {'fava', 'chickpeas', 'lima', 'mung', 'peanut',
                            'peanuts', 'miso', 'natto', 'tempeh', 'soy', 'tofu',
                            'hummus', 'soymilk', 'navy', 'pinto'},

                    '1700': {'lamb', 'veal', 'bison', 'boar', 'deer', 'elk',
                            'moose', 'rabbit'},

                    '1800': {'bread', 'cornbread', 'pumperknickle', 'bagels',
                            'cookies', 'crackers', 'croissants', 'croutons',
                            'pastry', 'doughnuts', 'muffins', 'toast', 'pancakes',
                            'pie', 'baking', 'tortillas'},

                    '1900': {'pudding', 'gelatin', 'flan', 'candy', 'frosting',
                            'molasses', 'sugar', 'syrup', 'jam', 'preserve',
                            'popcorn'},

                    '2000': {'barley', 'buckwheat', 'grain', 'cornmeal',
                            'couscous', 'hominy', 'millet', 'rice', 'semolina',
                            'pasta', 'noodles', 'quinoa', 'sorghum'}
                    })


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
        for blah in range(15000):# KILL
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

                INGREDIENT = re.split(', | ', ingredient.lower())

                # Handling random standalone numbers from poor website formatting
                if len(INGREDIENT) == 1 and INGREDIENT[0].isdigit():
                    continue

                grams = None
                qty = None

                # Check if fractional unicode in first or second element and convert
                for i in range(2):
                    for key in fractional_keys:
                        # Handling standalone fractions
                        if key == INGREDIENT[i]:
                            INGREDIENT[i] = fractional[key]
                            break
                        # Handling fractions that are attached to another number
                        if key in INGREDIENT[i]:
                            idx = INGREDIENT[i].find(key)
                            if INGREDIENT[i][idx-1].isdigit():
                                # This inserts the summed value into position
                                INGREDIENT[i] = (INGREDIENT[i][:idx-1] +
                                                    str(int(INGREDIENT[i][idx-1]) +
                                                    float(fractional[key])) +
                                                    INGREDIENT[i][idx+1:])
                            else:
                                INGREDIENT[i] = (INGREDIENT[i][:idx] +
                                                    fractional[key] +
                                                    INGREDIENT[i][idx+1:])
                            break


                # Establish quantity
                if INGREDIENT[0].isdigit():
                    try:
                        # If first index is a digit, save in variable
                        qty = float(INGREDIENT[0])
                        # If first index is a number, and second is a float
                        INGREDIENT[0] = (str(int(INGREDIENT[0]) +
                                                float(INGREDIENT[1])))
                        del INGREDIENT[1]
                        qty = float(INGREDIENT[0])
                    # If the above crashes, still saved first index as qty
                    # If it doesn't, first two indexes summed and qty overwritten
                    except:
                        pass
                else:
                    # In the case first index is a float
                    try:
                        qty = float(INGREDIENT[0])
                    except:
                        pass


                # Check for common units of measurement (BBC format)
                if "g/" in INGREDIENT[0] and 'kg/' not in INGREDIENT[0]:
                    grams = float(INGREDIENT[0][0:INGREDIENT[0].find('g/')])

                elif "kg/" in INGREDIENT[0]:
                    grams = float(INGREDIENT[0][0:INGREDIENT[0].find('kg/')])/1000

                elif "l/" in INGREDIENT[0] and 'ml/' not in INGREDIENT[0]:
                    grams = float(INGREDIENT[0][0:INGREDIENT[0].find('l/')])/1000

                elif "ml/" in INGREDIENT[0]:
                    grams = float(INGREDIENT[0][0:INGREDIENT[0].find('ml/')])


                # If quantity exists, convert to grams using measurement dict
                if qty != None and grams == None:
                    # Check for common units of measurement (UNIVERSAL)
                    try:
                        for i in range(1,3): # Checking second and third indices
                            for key in measurement_keys:
                                if key in INGREDIENT[i]:
                                    grams = qty * measurement[key]
                                    break
                    except:
                        pass


                # Truncate to remove numerics, measurements, and stop words
                truncated = []
                stop = (['a', 'and', 'the', 'or', 'of', 'if', 'on', 'but',
                        'pinch', 'left', 'peeled', 'cut', 'chopped', 'sliced',
                        'small', 'medium', 'large', 'whole', 'into', 'in', 'to',
                        'plus', 'more', 'thick', 'halved', 'quartered', 'good',
                        'inch', 'inches', 'about', 'sea', 'end', 'approximate',
                        'approximately'])

                for i in INGREDIENT:
                    skip = False
                    for j in i:
                        if j.isdigit():
                            skip = True
                    for k in measurement_keys:
                        if k in i:
                            skip = True
                    for l in fractional_keys:
                        if l in i:
                            skip = True
                    if i in stop:
                        continue
                    if skip == False:
                        truncated.append(i)

                # Find food group if applicable
                FoodGroup = None

                exit = False
                check = False

                for i in truncated:
                    for fdgrp, vals in FoodGroupID.items():
                        # Check one more ingredient to make sure
                        # (ex. red wine vinegar - wine is a keyword, but want vinegar)
                        if check:
                            check = False
                            if i in vals:
                                FoodGroup = fdgrp
                                exit = True
                                break

                        elif i in vals:
                            FoodGroup = fdgrp
                            exit = True
                            check = True
                            break
                    if check:
                        continue
                    if exit == True:
                        break



                # Get nutrition from USDA database
                '''
                Initialize list to keep track of:
                    -counter
                    -description length
                    -food ID
                Best match will be highest count in shortest description
                '''

                BestMatch = [0, float('inf'), None]

                with open('USDA_Nutrition_DataSet/FOOD_DES.txt') as g:
                    for line in g:
                        USDA_desc = line.lower().split('~^~')

                        # If food group identified, only search there
                        if FoodGroup != None and USDA_desc[1] == FoodGroup:

                            CurrentMatch = [0, float('inf'), None]

                            # Check if words in ingredient are in USDA database
                            for i in truncated:

                                # Remove last letter to deal with plurality
                                i = i[:-1]

                                # Hard coded exceptions. Pretty annoying...
                                if 'canadian' in USDA_desc[2] and 'canadian' not in truncated:
                                    continue
                                if 'tofu' in USDA_desc[2] and 'tofu' not in truncated:
                                    continue
                                if i == 'cilantr' and 'coriander' in USDA_desc[2]:
                                    CurrentMatch[0] += 2 # Cheating
                                if 'tortilla' in i:
                                    FoodGroup = '1800'
                                if i in USDA_desc[2]:
                                    CurrentMatch[0] += 1

                            # If count is >= best, add rest of information
                            if CurrentMatch[0] >= BestMatch[0]:
                                CurrentMatch[1] = len(USDA_desc[2])
                                CurrentMatch[2] = USDA_desc[0][1:]

                            # If count higher, take that one
                            if CurrentMatch[0] > BestMatch[0]:
                                BestMatch = CurrentMatch

                            # If count is higher and ref length is shorter, update best
                            if (CurrentMatch[0] >= 1 and
                                CurrentMatch[0] >= BestMatch[0] and
                                CurrentMatch[1] <= BestMatch[1]):

                                BestMatch = CurrentMatch

                                # Print statement to see match
                                BestDesc = USDA_desc[2].split(', ')
                                print("\ntruncated: ", truncated,
                                        "\nUSDA_Desc: ", BestDesc,
                                        '\nbest match:', BestMatch, "\n###############")

                        # Otherwise, check every USDA food description
                        elif FoodGroup == None:

                            CurrentMatch = [0, float('inf'), None]

                            # Check if words in ingredient are in USDA database
                            for i in truncated:

                                # Remove last letter to deal with plurality
                                i = i[:-1]

                                if i in USDA_desc[2]:
                                    CurrentMatch[0] += 1

                            # If count is >= best, add rest of information
                            if CurrentMatch[0] >= BestMatch[0]:
                                CurrentMatch[1] = len(USDA_desc[2])
                                CurrentMatch[2] = USDA_desc[0][1:]

                            # If count higher, take that one
                            if CurrentMatch[0] > BestMatch[0]:
                                BestMatch = CurrentMatch

                            # If count is higher and ref length is shorter, update best
                            if (CurrentMatch[0] >= 1 and
                                CurrentMatch[0] >= BestMatch[0] and
                                CurrentMatch[1] <= BestMatch[1]):

                                BestMatch = CurrentMatch

                                # Print statement to see match
                                BestDesc = USDA_desc[2].split(', ')
                                print("\ntruncated: ", truncated,
                                        "\nUSDA_Desc: ", BestDesc,
                                        '\nbest match:', BestMatch, "\n###############")

                        else:
                            continue

                    # Print statement to see result of ingredient search
                    print('\n','~^~^~^~^~^~^~^~^~^~  RESULT  ~^~^~^~^~^~^~^~^~^~^~',
                            '\nscraped:   ', INGREDIENT,
                            '\ntruncated: ', truncated,
                            '\nUSDA_Desc: ', BestDesc,
                            '\nbest match:', BestMatch,
                            '\n\nqty:  ',qty,
                            '\ngrams:',grams,
                            '\n','~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~')

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



### SCRIBBLE ###
'''
### TRUNCATE ###
1. Numeric
2. Measurements
3. Stop words

### HOW TO MATCH INGREDIENTS TO USDA DATABASE ###

1. Highest number of matches in INGREDIENT line
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

FOOD_DES


---2019.02.27---
We need a new heuristic in managing the USDA food id lookup.
    -Perhaps incorporating some nlp techniques?
    -Pulling in synonyms of key words?
    -Finding words by lowest frequency?
'''
