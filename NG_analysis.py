# Naomi Goodnight
# Nutrition from Web Scraped Recipes - ANALYSIS
# https://github.com/nemasobhani/Nutrition-from-Web-Scraped-Recipes

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from get_nutrition_vars import column_names
sns.set(style="ticks", color_codes=True)

from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
#https://github.com/amueller/word_cloud

import nltk
import regex as re
from collections import Counter

# #So I can see multiple outputs
# from IPython.core.interactiveshell import InteractiveShell
# InteractiveShell.ast_node_interactivity = "all"

#Load the extra clean data
df = pd.read_csv('recipe_overclean.csv', sep = ",", quotechar = '"', dtype=object, index_col=0)
df["TotalIng"] = pd.to_numeric(df["TotalIng"])#This actually is num of nan

# Copy dataframe and group by recipe
NumRecipes = len(df)
NumIngr = sum(76 - df.TotalIng)
df_high_level = pd.Series([NumRecipes,NumIngr], ['NumRecipes','NumIngr'])

#View some summary data by website
agg1 = df.groupby("Website").size()
agg2 = 76 - df.groupby('Website')[["TotalIng"]].mean() #To convert to not nan
website = pd.concat([agg1, agg2], axis=1, sort=False)
website.rename(columns={0: 'NumRecipes', 'TotalIng': 'AveNumIngr'}, inplace=True)
website

#Read in
ingredients = pd.read_csv('ingredients_agg.csv', names = ['Title','AggIngredients'], sep = ",", quotechar = '"', skipinitialspace=True, error_bad_lines = False, dtype=object)

#summary statistic,  word frequency
wordfreq_Title = ingredients.Title.apply(lambda x: pd.value_counts(str(x).split(" "))).sum(axis = 0)
wordfreq_Title = wordfreq_Title[3:]
wordfreq_AggIng = ingredients.AggIngredients.apply(lambda x: pd.value_counts(str(x).split(" "))).sum(axis = 0)
wordfreq_AggIng = wordfreq_AggIng[4:]

# Create stopword list:
stopwords = set(STOPWORDS)
stop1 = ['a', 'and', 'the', 'or', 'of', 'if', 'on', 'but','with','®',
        'pinch', 'left', '&', 'small', 'medium', 'large', 'whole', 'into', 'in',
        'to','plus', 'more', 'thick', 'halved', 'quartered', 'good',
        'inch', 'inches', 'about', 'sea', 'end', 'approximate',
        'approximately', 'very', 'finely', 'for', 'nan', 'none',
         'recipe', 'freshly','ground']
measurement = ['teaspoon', 'tsp', 'tablespoon', 'tbsp','sprigs','sprig',
               'teaspoons', 'tablespoons',
                'ounce', 'oz', 'cup', 'pint', 'pt',
                'ounces', 'cups', 'pints',
                'quart', 'qt', 'gallon', 'gal',
                'quarts', 'gallons',
               'pound', 'lb', 'gram', 'kilogram',
               'pounds', 'lbs', 'grams', 'kilograms',
                'milliliter', 'liter', 'weight',
                'milliliters', 'liters']
amounts = ["1", "one", "2", "two", "3", 'three','4','four',
           '5','five','6','six','7','seven','8','eight','9',
           'nine','10','ten','½', '1/2','half', '1½','¼','1/4',
           '3/4','⅓','1/3','¾','1-½','12']
stopwords.update(stop1,measurement,amounts)

#Remove adj and verbs
stopwordsExtra = stopwords.copy()
stopwordsExtra.update(['peeled', 'cut', 'chopped', 'sliced','fresh','black',
                        'red','powder','minced','white','grated','kosher',
                        'unsalted','leaves','sauce','baking','dried','diced',
                        'thinly','extract','divided','brown','pieces','green',
                        'taste','slices','seeds','dry','room','temperature',
                        'all-purpose','shredded','crushed','drained','coarsely',
                        'heavy','frozen','granulated','melted','softened',
                        'trimmed','toasted','yellow','removed','cubes','cooked',
                        'light','seeded','powdered'])


wb_topsum = website.sort_values(by='NumRecipes',ascending=False).head(20)
wb_topave = website.sort_values(by='AveNumIngr',ascending=False).head(20)

wordfreq_Title = wordfreq_Title.sort_values(ascending=False).head(50)
wordfreq_Ing = wordfreq_AggIng.sort_values(ascending=False).head(50)

wordfreq_AggIng_wo_stop = wordfreq_AggIng[~wordfreq_AggIng.index.isin(stopwords)]
wordfreq_AggIng_wo_stop = wordfreq_AggIng_wo_stop.sort_values(ascending=False).head(50)

wordfreq_Title_wo_stop = wordfreq_Title[~wordfreq_Title.index.isin(stopwords)]
wordfreq_Title_wo_stop = wordfreq_Title_wo_stop.sort_values(ascending=False).head(50)

wordfreq_AggIng_wo_extra = wordfreq_AggIng[~wordfreq_AggIng.index.isin(stopwordsExtra)]
wordfreq_AggIng_wo_extra = wordfreq_AggIng_wo_extra.sort_values(ascending=False).head(50)

wordfreq_Ing_prop = wordfreq_AggIng_wo_extra/len(df)

# if analysis:
wb_topsum
wb_topave
wordfreq_Title_top
wordfreq_Ing_top
wordfreq_AggIng_top_wo_stop
wordfreq_Title_top_wo_stop
wordfreq_AggIng_top_wo_extra
# Visualization on each nutrient column
# if plot:
# sns.catplot(x=col_name, data=col_df, kind='boxen')
# plt.xlim(0, col_ser.max())


def wc(site,section, pic=None):
    # Generate a word cloud image
    wordcloud = WordCloud(stopwords=stopwords, background_color="white",mask=pic).generate(ingredients.loc[site,section])
    # Display the generated image:
    # the matplotlib way:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
