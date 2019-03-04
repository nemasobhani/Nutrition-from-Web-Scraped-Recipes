# Nema Sobhani
# Nutrition from Web Scraped Recipes
# https://github.com/nemasobhani/Nutrition-from-Web-Scraped-Recipes

'''
This script will return the following from a .csv file containing web scraped
recipe information as collected by Naomi Goodnight (partner on this project):

From raw scraped data:
    Recipe title
    Link to recipe
    Total time (in minutes)
    All ingredients

Desired information:
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
    If no quantity or weight given, default grams given based on food group.
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
                            'cilantro', 'jalapeno', 'jalapeño', 'scallion',
                            'scallions'},

                    '1200': {'seeds', 'nuts', 'almonds', 'brazilnuts', 'cashews',
                            'chestnuts', 'coconut', 'macadamia', 'pecans', 'pine',
                            'pistachios', 'walnuts'},

                    '1300': {'beef', 'brisket'},

                    '1400': {'water', 'alcoholic', 'liquor', 'liqueur', 'beer',
                            'daiquiri', 'tea', 'coffee', 'lemonade', 'wine'},

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
                            'doughnuts', 'muffins', 'toast', 'pancakes', 'pie',
                            'baking', 'tortillas'},

                    '1900': {'pudding', 'gelatin', 'flan', 'candy', 'frosting',
                            'molasses', 'sugar', 'syrup', 'jam', 'preserve',
                            'popcorn'},

                    '2000': {'barley', 'buckwheat', 'grain', 'cornmeal',
                            'couscous', 'hominy', 'millet', 'rice', 'semolina',
                            'pasta', 'noodles', 'quinoa', 'sorghum'}
                    })

    # Factor to determine grams for 1 serving of item from food group compared to 100g default
    FoodGroupFactor = ({'0100':1, '0200':1, '0300':1, '0400':1, '0500':1,
                        '0600':1, '0700':1, '0800':1, '0900':1, '1000':1,
                        '1100':1, '1200':1, '1300':1, '1400':1, '1500':1,
                        '1600':1, '1700':1, '1800':1, '1900':1, '2000':1,
                        '2100':1, '2200':1, '2500':1, None:1})

    # Stop words to ignore when parsing individual ingredients
    stop = (['a', 'and', 'the', 'or', 'of', 'if', 'on', 'but',
            'pinch', 'left', 'peeled', 'cut', 'chopped', 'sliced',
            'small', 'medium', 'large', 'whole', 'into', 'in', 'to',
            'plus', 'more', 'thick', 'halved', 'quartered', 'good',
            'inch', 'inches', 'about', 'sea', 'end', 'approximate',
            'approximately', 'very', 'finely', 'for'])

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

    # Initialize dataframe consisting of all ingredients and nutrition data
    column_names = ["Recipe",
                    "Link",
                    "Time (min)",
                    "Ingredient",
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

    ingredients_df = pd.DataFrame(columns=column_names)



    # Access scraped data
    with open(file, encoding='utf-8') as f:

        # I'm using this to jump around in the raw data file
        for blah in range(10013):# KILL
            next(f) # KILL

        z = 0 # KILL

        for line in f:
            # Error handling for UnicodeDecodeError and IndexError
            try:

                # print(line) # KILL

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
                try:
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
                except:
                    pass



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
                    -food group
                Best match will be highest count in shortest description
                '''

                BestMatch = [0, float('inf'), None, FoodGroup]

                with open('USDA_Nutrition_DataSet/FOOD_DES.txt') as g:
                    for line in g:
                        USDA_desc = line.lower().split('~^~')

                        # If food group identified, only search there
                        if FoodGroup != None and USDA_desc[1] == FoodGroup:

                            CurrentMatch = [0, float('inf'), None, FoodGroup]

                            # Check if words in ingredient are in USDA database
                            for i in truncated:

                                # Remove last letter to deal with plurality
                                i = i[:-1]

                                # Hard coded exceptions. Pretty annoying...
                                if 'canadian' in USDA_desc[2] and 'canadian' not in truncated:
                                    continue
                                if 'soy' in USDA_desc[2] and 'soy' not in truncated:
                                    continue
                                if 'tofu' in USDA_desc[2] and 'tofu' not in truncated:
                                    continue
                                if 'nog' in USDA_desc[2] and 'nog' not in truncated:
                                    continue
                                if 'yolk' in USDA_desc[2] and 'yolk' not in truncated:
                                    continue
                                if 'white' in USDA_desc[2] and 'white' not in truncated:
                                    continue
                                if 'dried' in USDA_desc[2] and 'dried' not in truncated:
                                    continue
                                if 'powder' in USDA_desc[2] and 'powder' not in truncated:
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
                                # BestDesc = USDA_desc[2].split(', ')
                                # print("\ntruncated: ", truncated,
                                #         "\nUSDA_Desc: ", BestDesc,
                                #         '\nbest match:', BestMatch, "\n###############")

                        # Otherwise, check every USDA food description
                        elif FoodGroup == None:

                            CurrentMatch = [0, float('inf'), None, FoodGroup]

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
                                CurrentMatch[3] = USDA_desc[1]

                            # If count higher, take that one
                            if CurrentMatch[0] > BestMatch[0]:
                                BestMatch = CurrentMatch

                            # If count is higher and ref length is shorter, update best
                            if (CurrentMatch[0] >= 1 and
                                CurrentMatch[0] >= BestMatch[0] and
                                CurrentMatch[1] <= BestMatch[1]):

                                BestMatch = CurrentMatch

                                # Print statement to see match
                                # BestDesc = USDA_desc[2].split(', ')
                                # print("\ntruncated: ", truncated,
                                #         "\nUSDA_Desc: ", BestDesc,
                                #         '\nbest match:', BestMatch, "\n###############")

                        else:
                            continue

                    # Print statement to see result of ingredient search
                    # print('\n','~^~^~^~^~^~^~^~^~^~  RESULT  ~^~^~^~^~^~^~^~^~^~^~',
                    #         '\nscraped:   ', INGREDIENT,
                    #         '\ntruncated: ', truncated,
                    #         '\nUSDA_Desc: ', BestDesc,
                    #         '\nbest match:', BestMatch,
                    #         '\n\nqty:  ',qty,
                    #         '\ngrams:',grams,
                    #         '\n','~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~')


                    # Define multiplication factor based on qty, grams, and food group
                    if grams == None and qty == None:
                        factor = FoodGroupFactor[BestMatch[3]]
                    if grams == None and qty != None:
                        factor = FoodGroupFactor[BestMatch[3]]*qty
                    if grams != None:
                        factor = grams / 100

                    # Using food_ID get nutrition data from USDA file (NUT_DATA)
                    with open('USDA_Nutrition_DataSet/NUT_DATA.txt') as g:

                        # Initialize dictionary to track nutrients
                        NutrDict = ({'protein':None, 'fat':None, 'carb':None,
                                    'cal':None, 'sugar':None, 'fiber':None,
                                    'calcium':None, 'iron':None, 'sodium':None,
                                    'vitA':None, 'vitC':None, 'cholest':None,
                                    'transfat':None, 'satfat':None})

                        for line in g:
                            if BestMatch[2] == line[1:6]: # Specific to avoid references
                                USDA_nutr = line.split('^')[:3]

                                # Pull each nutrient amount into variable
                                if USDA_nutr[1] == '~203~':
                                    NutrDict['protein'] = float(USDA_nutr[2])*factor
                                if USDA_nutr[1] == '~204~':
                                    NutrDict['fat'] = float(USDA_nutr[2])*factor
                                if USDA_nutr[1] == '~205~':
                                    NutrDict['carb'] = float(USDA_nutr[2])*factor
                                if USDA_nutr[1] == '~208~':
                                    NutrDict['cal'] = float(USDA_nutr[2])*factor
                                if USDA_nutr[1] == '~269~':
                                    NutrDict['sugar'] = float(USDA_nutr[2])*factor
                                if USDA_nutr[1] == '~291~':
                                    NutrDict['fiber'] = float(USDA_nutr[2])*factor
                                if USDA_nutr[1] == '~301~':
                                    NutrDict['calcium'] = float(USDA_nutr[2])*factor
                                if USDA_nutr[1] == '~303~':
                                    NutrDict['iron'] = float(USDA_nutr[2])*factor
                                if USDA_nutr[1] == '~307~':
                                    NutrDict['sodium'] = float(USDA_nutr[2])*factor
                                if USDA_nutr[1] == '~318~':
                                    NutrDict['vitA'] = float(USDA_nutr[2])*factor
                                if USDA_nutr[1] == '~401~':
                                    NutrDict['vitC'] = float(USDA_nutr[2])*factor
                                if USDA_nutr[1] == '~601~':
                                    NutrDict['cholest'] = float(USDA_nutr[2])*factor
                                if USDA_nutr[1] == '~605~':
                                    NutrDict['transfat'] = float(USDA_nutr[2])*factor
                                if USDA_nutr[1] == '~606~':
                                    NutrDict['satfat'] = float(USDA_nutr[2])*factor

                        nutr_data = (recipe[:3] + [ingredient] +
                                    [NutrDict['cal']] + [NutrDict['fat']] +
                                    [NutrDict['satfat']] + [NutrDict['transfat']] +
                                    [NutrDict['cholest']] + [NutrDict['sodium']] +
                                    [NutrDict['carb']] + [NutrDict['fiber']] +
                                    [NutrDict['sugar']] + [NutrDict['protein']] +
                                    [NutrDict['vitA']] + [NutrDict['vitC']] +
                                    [NutrDict['calcium']] + [NutrDict['iron']])

                        ingredients_df.loc[len(ingredients_df)] = nutr_data


            z += 1 # KILL
            print('Getting nutrition for recipe: ', z)
            if z == 20: # KILL
                break # KILL

    return ingredients_df

# print(GetNutrition("recipe_output_new.csv"))
GetNutrition("recipe_output_new.csv").to_csv('get_nutrition_01.csv', index=False)


### NOTES ###
# See GitHub repository (linked in line 3) for all discussion, analysis, and visualization.

### CITATIONS ###
# https://www.ars.usda.gov/northeast-area/beltsville-md-bhnrc/beltsville-human-nutrition-research-center/nutrient-data-laboratory/docs/sr28-download-files/
# https://www.fda.gov/food/labelingnutrition/ucm274593.htm
# https://www.exploratorium.edu/cooking/convert/measurements.html


### Scribble ###
'''
Goals:
    -Assign default food group factors
    -Break up code
        ~All predefined variables
        ~Independent functions

    -Analysis approach
    -Visualization
    -Write-up
    -Jupyter Notebook
'''
