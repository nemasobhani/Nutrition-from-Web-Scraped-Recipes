#This section is a collection of commands I used individually
#     #Initial state
#       wc -l 'recipe_output_new.csv'  #155891
#     #lines without a first ingredient
#       awk -F, '!length($4)' 'recipe_output_new.csv' > 'blank4.csv'
#       wc -l 'blank4.csv'  #17355
#     #How many 0 ingredient lines were duplicate recipes?
#     #create a new file with lines from original if url matches a url of blank4
#       awk -F, 'FNR==NR {a[$1]=$0; next}; $1 in a {print a[$1]}' 'recipe_output_new.csv' 'blank4.csv' >'noing.csv'
#       wc -l 'noing.csv' #17355, I think because only the first match printed
#     #So, how many of the new combined file have a first ingredient
#       awk -F, 'length($4)' 'noing.csv' | wc -l #12340
#     #Therefore, 12340 lines of the 17355 blank ingredient lines have duplicate lines that DO contain ingredients
#     #Let's chop out the empty ingredient lines, should reduce by 17355
#       awk -F, 'length($4)' 'recipe_output_new.csv' > 'recipe_output_alling.csv'
#       wc -l recipe_output_alling.csv
#     #Couldn't overwrite inline, so clear out old _new and rename this recipe_output_new
#Only rows from file2 that are NOT in file1
#awk 'FNR==NR{a[$0]++}FNR!=NR && !a[$0]{print}' 'long29.csv' 'recipe_output_new.csv'
#Check
#awk -F',' '$1~/joyofkosher/' recipe_output_wo_longjoy.csv> didiwork.csv
#awk -F"," '$1 != "http://www.joyofkosher.com/recipes/fresh-tuna-nicoise-salad/" {print $0 }' 'recipe_temp.csv' > 'recipe_output_new.csv'
#awk -F"," '$1 == "http://foodnetwork.com/recipes/rebuilt-louisiana-seafood-platter-recipe3-1965535" {print $0 }' 'recipe_output_new.csv' > 'recipe_temp.csv'
#Print lines with only two fields and the line immediately following
#awk -F, 'NF==2 {print; nr[NR+1];next}; NR in nr' recipe_output.csv > test.csv

import pandas as pd
import re

df = pd.read_csv('recipe_output_new.csv', names = range(80), sep = ",", quotechar = '"', skipinitialspace=True, error_bad_lines = False, dtype=object)
# df.to_csv(path_or_buf = f'recipe_temp.csv', header = False)#, index = False)
# print(max(df.count(axis=1)))#.to_csv(path_or_buf = f'recipe_ing_count.csv', header = True)

#Finds and prints recipes with ingredients containing more than 30 spaces
# for i in range(80):
#     mask = (df[i].str.count(" ") > 30)
#     df.loc[mask].to_csv(path_or_buf = f'long{i}.csv')
# for i in range(2,80):
#     mask = (df[i].str.contains(r"\(([^\)]+)\),")==True)#then change , to "
#     df.loc[mask,i].to_csv(path_or_buf = f'parenthesis{i}.csv')
    #cat parenthesis3.csv parenthesis4.csv parenthesis5.csv parenthesis6.csv parenthesis7.csv parenthesis8.csv parenthesis9.csv parenthesis10.csv parenthesis11.csv parenthesis12.csv parenthesis13.csv parenthesis14.csv parenthesis15.csv parenthesis16.csv parenthesis17.csv parenthesis18.csv parenthesis19.csv parenthesis20.csv parenthesis21.csv parenthesis22.csv parenthesis23.csv parenthesis24.csv parenthesis25.csv parenthesis26.csv parenthesis27.csv parenthesis28.csv parenthesis29.csv parenthesis30.csv parenthesis31.csv parenthesis32.csv parenthesis33.csv parenthesis34.csv parenthesis35.csv parenthesis36.csv parenthesis37.csv parenthesis38.csv parenthesis39.csv parenthesis40.csv parenthesis41.csv parenthesis42.csv parenthesis43.csv parenthesis44.csv parenthesis45.csv parenthesis46.csv parenthesis47.csv > parenthesis.csv
# for i in range(2,80):
#     df.loc[:,i] = df.loc[:,i].str.replace(pat=r"\([^\)]+\)", repl=',', n=-1, case=None, flags=re.IGNORECASE, regex=True)
#     # print(df.loc[i])
# df.to_csv(path_or_buf = f'recipe_noparens.csv', header = False, index = False)
# for i in range(2,80):
#     df[df[i].str.contains("Instructions")==True].to_csv(path_or_buf = f'instruct{i}.csv')


def dupes():
    '''Remove duplicate rows'''
    dupes = df[df.duplicated()]
    print(len(dupes))#4866
    dupes.to_csv(path_or_buf = f'recipe_dupes2.csv')#, header = False
    dupes = df.drop_duplicates(keep='last')
    dupes.to_csv(path_or_buf = f'recipe_temp.csv', header = False)#, index = False)
    #Remove the first row(weird column names), Put our header back on top, Remove the first column
    # awk 'NR>1 {print$0}' recipe_temp.csv>recipe_output_new.csv
    # cat header.csv recipe_temp.csv >recipe_output_new.csv
    # awk -F',' '{print substr($0, index($0, $2))}' recipe_temp_temp.csv > recipe_output_new.csv



def repeat_ingredients():
    '''For recipes with more than 50 ingredients, finds recipes with repeat ingredients'''
    mask = (df.count(axis=1) > 50)
    mass = df.loc[mask]
    print(f'The number of recipes to investigate are {len(mass)}')#53

    for i in range(len(mass)):
        ingset = set()
        rec_list = list(mass.iloc[i,0:3])
        # print(f'The head is {rec_list}')
        ing_count = mass.iloc[i].count()
        # print(f'Starting with {ing_count} ingredients')
        for j in range(3,155):
            ing = mass.iloc[i,j]
            # print(ing)
            ingset.add(ing)
        uniq_ing_count = len(ingset)
        # print(f'My set has {uniq_ing_count} ingredients')
        rec_list = rec_list + list(ingset) + ["" for i in range (len(ingset)+3,155)]
        #print(f'My list has {len(rec_list)} elements')
        #print(f'My collected list is {rec_list}')
        #print(f'I will remove {len(df[df[0] == rec_list[0]])} rows from the master df')
        mask2 = (df[0] == rec_list[0])
        #print(f'The length of the master df is {len(df)}')
        if (ing_count/uniq_ing_count) > 1.5:
            df.drop(df[mask2].index, inplace = True)
            df.loc[len(df)] = rec_list
            print(f'The length of the master df is {len(df)}')
            print(f'I reduced ingredients from {ing_count} to {uniq_ing_count} in {mass.iloc[i,0:1]}')

    mask = (df.count(axis=1) > 50)
    mass = df.loc[mask]
    print(f'The number of remaining recipes to investigate are {len(mass)}') #32
    df.to_csv(path_or_buf = f'recipe_temp.csv', header = False, index = False)
    #Remove excess commas
    # awk '{print substr($0, 1, length($0)-75)}' recipe_temp.csv > recipe_output_new.csv
def freq():
    '''create a word frequency dictionary'''
    word_count = {}
    with open('recipe_output_new.csv') as f:
        for line in f:
            line = line.lower()
            for w in re.findall(r"[\w']+", line, re.IGNORECASE):
                if w in word_count:
                    word_count[w] += 1
                else:
                    word_count[w] = 1
    # print(word_count)
    wc_sorted = sorted(word_count.items(), key=lambda kv: kv[1])
    wc_sorted2 = []
    for i in range(len(wc_sorted)):
        if int(wc_sorted[i][1]) > 1000:
            wc_sorted2.append(wc_sorted[i])
    print(wc_sorted2)
dupes() #resmove duplicate rows
# repeat_ingredients() #remove repeated ingredients
