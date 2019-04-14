import numpy as np
import pandas as pd
import csv as csv

df = pd.read_csv('acdc-records.csv')

excol = ['RecordID', 'DateAdded', 'DateChanged', 'Author', 'Title',
       'CopyrightDate', 'Barcode', 'Classification', 'MainEntry', 'Custom1',
       'Custom2', 'Custom3', 'Custom4', 'Custom5', 'ImportErrors',
       'ValidationErrors', 'TagNumber', 'Ind1', 'Ind2']


for column in df.columns:
    if column in excol:
        df.drop(column, axis=1, inplace = True) #change the dataframe directly

# print(df.columns)

#### Pulling out notes for clean records only ######

df = df.applymap(str) #https://stackoverflow.com/questions/42676982/python-turn-all-items-in-a-dataframe-to-strings
#this turns everything in the dataframe into a string so that you can iterate over it


# http://jose-coto.com/query-method-pandas

# example = pd.DataFrame(df,columns = (["1","100","245","260","700"]))
# print(example)
#
# example = example.applymap(str)


### add code comments \/
df = df[df['500'].str.contains("Hal R. Taylor")]

citations = []
for index,row in df.iterrows():
    box = row["852"]
    record_id = row["1"]
    author = row["100"]
    addauthor = ""
    if row["700"] != "nan":
        for subfield in row["700"].split("$"):
            if subfield != "":
                if subfield[0] == "a":
                    addauthor += subfield[1:] + ", "
        if addauthor != "":
            addauthor = addauthor[0:len(addauthor)-2]
    title = row["245"]
    year = ""
    for subfield in row["260"].split("$"):
        if subfield != "":
            if subfield[0] == "c":
                year = subfield[1:]
    citation = box + record_id + "." + author + "," + addauthor + "." + title + "." + year + "."
    citations.append(citation)


filename = "inventory.txt"
outfile = open(filename,"w",encoding="utf-8")
for citation in citations:
    print(citation, file = outfile)
outfile.close



#CITATION
# Box No.
#   Record ID No. Author(s). "Title". (Year)

# [852]
#   [1]. [100$a],[700$a].[245$a].[260$c]

# ------------
#| To Dos    |
# ------------

    #put my inventory code into a function that can read in ALL of the collections
    # finish cleaning all of the stuff in each field going into the inventory
    # make a list of collections
    # figure out how to deal with the messy data, aka the records with collection notes OUTSIDE of the 500 bc of import errors
    # sort by box numbers, then by record id











