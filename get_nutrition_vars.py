# Nema Sobhani
# Nutrition from Web Scraped Recipes
# https://github.com/nemasobhani/Nutrition-from-Web-Scraped-Recipes

'''This script stores all lengthy preset variables to use with get_nutrition.py'''


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
FoodGroupFactor = ({'0100':340/100, '0200':15/100, '0300':15/100, '0400':15/100,
                    '0500':1, '0600':224/100, '0700':84/100, '0800':250/100,
                    '0900':250/100, '1000':1, '1100':250/100, '1200':28/100,
                    '1300':1, '1400':360/100, '1500':224/100, '1600':125/100,
                    '1700':1, '1800':132/100, '1900':50/100, '2000':1,
                    '2100':350/100, '2200':350/100, '2500':28/100, '3500':1,
                    '3600':1, None:1})


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


# Column names for data frame
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


### NOTES ###
'''
Food Group Factor Determination:
    0100: Dairy is ~340g per serving, since eggs always have quantity, dairy used
    0200: 1 tablespoon of herbs = 1 serving (2 grams)
    0300: Baby food serving size ~1 tablespoon
    0400: Fats and oils serving size of 1 tablespoon
    0500: For poultry, 100 grams used as default
    0600: 8 ounces of soup = 224 grams
    0700: Deli meat serving is 3 ounces = 84 grams
    0800: Breakfast cereal serving is 1 cup = 250 grams
    0900: Fruit serving size is 1 cup = 250 grams
    1000: For pork, 100 grams used as default
    1100: Vegetable serving size is 1 cup = 250 grams
    1200: Nuts and seeds serving size is 1 ounce = 28 grams
    1300: For beef, 100 grams used as default
    1400: Beverage serving size is 360 ml or 360 grams
    1500: Fish serving size is 8 ounces = 224 grams
    1600: Legume serving size is 0.5 cups = 125 grams
    1700: For lamb/veal/game, 100 grams used as default
    1800: For baked goods, 132 grams used
    1900: For sweets (candy), serving size is 50 grams
    2000: For cereal grains and pasta, 100 grams is used as default
    2100: For fast food, total meal weight is ~ 350 grams
    2200: For meals, same deafult as fast food used (350 grams) [unlikely to find ingredient that is a meal]
    2500: For snacks (chips, etc.), serving size is 1 ounce = 28 grams
    3500: 100 grams default
    3600: 100 grams default
'''
