# Nema Sobhani
# Nutrition from Web Scraped Recipes - ANALYSIS
# https://github.com/nemasobhani/Nutrition-from-Web-Scraped-Recipes

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from get_nutrition_vars import column_names
sns.set(style="ticks", color_codes=True)

ingredients_df = pd.read_csv('get_nutrition_FULL20k.txt', low_memory=False)
ingredients_df.columns = column_names

# Copy dataframe and group by recipe
ingredients_df2 = ingredients_df.copy(deep=True)
ingredients_df2 = ingredients_df2.groupby('Recipe').sum()
ingredients_df2


def RecipeAnalyze(analysis=False, plot=False):
    # Make df to store all analytic information
    analysis_names = ['Nutrition', 'Mean', 'Median', 'Max', 'Max Recipe']
    analysis_df = pd.DataFrame(columns=analysis_names)

    # Analyze each column
    for col_name in column_names[4:]:

        # Establish IQR and outliers (0.15 and 0.85 quantiles used)
        Q1 = ingredients_df2[col_name].quantile(0.15)
        Q3 = ingredients_df2[col_name].quantile(0.85)
        IQR = Q3 - Q1
        magnitude = 1.5
        out_low = 0 # Q1-(magnitude*IQR) Can't get - value
        out_high = Q3+(magnitude*IQR)

        # New dataframe with outliers removed for current column
        col_df = ingredients_df2[ingredients_df2[col_name] < out_high]
        col_df = col_df[col_df[col_name] >= out_low]
        col_ser = col_df[col_name]

        # Update analysis dataframe with basic stats and associated recipe for max
        if analysis:
            max_name = col_df[col_df[col_name] == col_df[col_name].max()].iloc[0].name
            analysis_df.loc[len(analysis_df)] = [col_name, col_ser.mean().round(1), col_ser.median().round(1), col_ser.max().round(1), max_name]

        # Visualization on each nutrient column
        if plot:
            sns.catplot(x=col_name, data=col_df, kind='boxen')
            plt.xlim(0, col_ser.max())

    if analysis:
        return analysis_df.set_index('Nutrition')
    elif plot:
        return 'Plotting complete!'



def IngredientAnalyze(analysis=False, plot=False):
    # Make df to store all analytic information
    analysis_names = ['Nutrition', 'Mean', 'Median', 'Max', 'Max Ingredient']
    analysis_df = pd.DataFrame(columns=analysis_names)

    # Analyze each column
    for col_name in column_names[4:]:

        # Establish IQR and outliers (0.15 and 0.85 quantiles used)
        Q1 = ingredients_df[col_name].quantile(0.15)
        Q3 = ingredients_df[col_name].quantile(0.85)
        IQR = Q3 - Q1
        magnitude = 1.5
        out_low = 0 # Q1-(magnitude*IQR) Can't get - value
        out_high = Q3+(magnitude*IQR)

        # New dataframe with outliers removed for current column
        col_df = ingredients_df[ingredients_df[col_name] <= out_high]
        col_df = col_df[col_df[col_name] > out_low]
        col_ser = col_df[col_name]

        # Update analysis dataframe with basic stats and associated recipe for max
        if analysis:
            max_name = col_df[col_df[col_name] == col_df[col_name].max()].iloc[0].Ingredient
            analysis_df.loc[len(analysis_df)] = [col_name, col_ser.mean(), col_ser.median(), col_ser.max(), max_name]

        # Visualization on each nutrient column
        if plot:
            sns.catplot(x=col_name, data=col_df, kind='boxen')
            plt.xlim(0, col_ser.max())

    if analysis:
        return analysis_df.set_index('Nutrition')
    elif plot:
        return 'Plotting complete!'



def Factoids():

    print('Here are some fun facts about our processed data!\n')

    # Using 3258 Cal / 1 lb butter
    butter_lbs = int(round(ingredients_df[ingredients_df['Ingredient'].str.contains('butter') == True]['Calories (kcal)'].sum() / 3258))
    print('Pounds of butter:', "{:,}".format(butter_lbs), '\n')

    # Length of sausage (4" avg)
    sausage_length = int(round(ingredients_df[ingredients_df['Ingredient'].str.contains('sausage') == True]['Calories (kcal)'].sum() /229 * 4 / 12))
    print('Feet of sausage:', sausage_length, '\n')

    # ingredients_df[ingredients_df['Ingredient'].str.contains('water') == True]['Calories (kcal)'].sum()

    # How many people would our recipes feed for a day
    ppl_feed = int(round(ingredients_df['Calories (kcal)'].sum() / 2000))
    ppl_feed_yrs = round(ppl_feed/365)
    print('All of our scraped recicpes would feed', "{:,}".format(ppl_feed), 'people for 1 day (based on 2,000 Cal diet).')
    print('For one individual, that would take', ppl_feed_yrs, 'years to eat!\n')

    # How many days worth of protein is that for a bodybuilder? (200 g per day)
    bodybuilder = int(round(ingredients_df['Protein (g)'].sum() / 200 / 365))
    print('Our recipes contain a', "{:,}".format(bodybuilder), 'year supply of protein for a bodybuilder!\n')

    # Weaponized garlic
    vampire = len(ingredients_df[ingredients_df['Ingredient'].str.contains('garlic')])
    print('Enough garlic to kill', "{:,}".format(vampire), 'vampires.\n')
