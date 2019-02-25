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


#Find extra long ingredients
import pandas as pd


df = pd.read_csv('recipe_output_new.csv', names = range(100), sep = ",", quotechar = '"', skipinitialspace=True, error_bad_lines = False)

#Finds and prints recipes with ingredients containing more than 30 spaces
for i in range(80,100):
    mask = (df[i].str.count(" ") > 1)
    df.loc[mask].to_csv(path_or_buf = f'long{i}.csv')
