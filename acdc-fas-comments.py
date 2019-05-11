#Importing pandas and numpy modules

import numpy as np
import pandas as pd

######################################


# Putting all of the collection names into a list and assigning them to a variable 

collections = ['Volume One Number One','AgComm Teaching','Theses','INTERPAK','Oscars in Agriculture','Eric Abbott',
               'Robert Agunga','Kathy Alison','George Axinn','Ovid Bay','John H. Behrens','Harvey F. Beutner',
               'George Biggar','Kristina M. Boone','John Brien','Claron Burnett','Francis C. Byrnes',
               'Warwick Easdown','James F. Evans','Eldon Fredericks','Claude W. Gifford','James E. Gruning',
               'Harold D. Guither','Dixon Harper','John A. Harvey','Delmar Hatesohl','Paul C. Hixson',
               'Theodore Hutchcroft','Robert Jarnagin','K. Robert Kern','Eugene A. Kroupa','Richard Lee',
               'Mason E. Miller','Geoffrey Moss','Fred Myers','Hadley Read','Bonnie Riechert','Stephen G-M Shenton',
               'Burton Swanson','Harold Swanson','Hal R. Taylor','Phillip J. Tichenor','Mark A. Tucker',
               'William B. Ward','Donald Watson','Larry R. Whiting','John L. Woods']

##################################################################

# Defining a function that processes each collection and outputs them into raw and strcutured inventories. 
def process_collection(collection,filename,filename_struc):
    df = pd.read_csv('acdc-records.csv')    #reading in the csv file into a dataframe
    df = df.applymap(str)   #making everything in the dataframe a string
    df = df[df['500'].str.contains(collection)]     #making the dataframe only contain rows where the 500 note contains a certain collection note

    df['Box'] = df['852'].str.\
                   extract(r'.*\$.*(?P<BoxFolder>Box:.*)').astype(str).BoxFolder.str.\
                   replace('\$.*', '', regex=True).str.\
                   replace('  ', ' ', regex=True).str.\
                   replace('Folder.*', '', regex=True).str.rstrip(' ;,')
    df['Folder'] = df['852'].str.\
                      extract(r'.*\$.*(?P<BoxFolder>Box:.*)').astype(str).BoxFolder.str.\
                      replace('\$.*', '', regex=True).str.\
                      replace('  ', ' ', regex=True).str.\
                      extract(r'.*(?P<Folder>Folder:.*)').astype(str).Folder.str.rstrip(' ;,')
    df['PlusIndictor'] = df['852'].str.\
                            extract(r'.*\$[a-z](?P<PlusIndictor>\+).*Box:.*').astype(str).PlusIndictor

    df['SortKey'] = df['Box'].str.\
                replace('Box:', '', regex=True).str.\
                rstrip(' ;,.').str.lstrip(' ;,.')

    for index,row in df.iterrows():
        if row["SortKey"].isdigit():
            row["SortKey"] = row["SortKey"].zfill(25)
        elif row["SortKey"] == "nan":
            row["SortKey"] = "".rjust(25, 'Z')
        else:
            row["SortKey"] = row["SortKey"].upper()

    df.sort_values(["SortKey","Folder"], ascending=[True,True],inplace=True)
    df.reset_index(drop=True,inplace=True)
    df.drop('SortKey', axis=1,inplace=True)

## DataFrame now contains the fields Box, Folder, Subfield, PlusIndictor, RemainingData
##     Subfield -- subfield letter that contained the box data
##     PlusIndictor -- plus sign in found proceeding subfield letter
##     RemainingData  -- remaining data found in box subfield
##  only data from the box subfield is used to populate these extra field

    citations = []      # Initializing the list for all of the citations the collection to go in
    for index,row in df.iterrows():     # looping over every cell in the dataframe 
        box = row['Box']                # assigning box as what is contained in row "Box"
        folder = row['Folder']          # assigning folder as what is contained in row "Folder"
        record_id = row["1"]            # assigning the record_id to what is contained in row "1"
        record_id = record_id.replace('ACDC_','')      #replacing the beginning of the record_id so it only contains the actua number
        author = ""                     # initializing the author variable as an empty string
        for subfield in row['100']:     # 
            if subfield != "nan":
                if subfield[0] =="a":
                    author = subfield[1:]
        addauthor = ""
        if row["700"] != "nan":
            for subfield in row["700"].split("$"):
                if subfield != "":
                    if subfield[0] == "a":
                        addauthor += subfield[1:] + ", "
            if addauthor != "":
                addauthor = addauthor[0:len(addauthor)-2]
        title = row["245"]
        title = title.replace('$a','')
        year = "undated"
        for subfield in row["260"].split("$"):
            if subfield != "":
                if subfield[0] == "c":
                    if subfield[1:] != "":
                        year = subfield[1:]

        citation = ""

        if box != "nan":
            citation += box + '. '
        if folder != "nan":
            citation += folder + '. '
        citation += record_id
        if author != "nan":
            citation += author + ", "
        if addauthor != "nan":
            citation += addauthor
        citation += title +". "
        citation += "(" + year +")."

        citations.append(citation)
    outfile = open(filename,"w",encoding="utf-8")
    outfile2 = open(filename_struc,'w',encoding='utf-8')

    lastbox = ""
    for citation in citations:
        print(citation, file = outfile)
        box = citation.split(". ")[0]
        if lastbox != box:
            print(box, file = outfile2)
        print(citation[citation.find(". ")+1:], file = outfile2)
        lastbox = box

    outfile.close()
    outfile2.close()
    
def inventories():
    for collection in collections:
        process_collection(collection, collection.replace(" ","-") + "-inventory.txt", collection.replace(" ","-")+ "-structured-inventory.txt")

def process_findingaid(collection):       # defining a function that processes each of the 
    infile = open('fa_template.txt','r',encoding='utf-8')     # opening the finding aid template
    template = infile.read()                # reading in the finding aid template     
    infile.close()                          # closing the finding aid template file 

    infile2 = open(collection.replace(" ","-")+ "-structured-inventory.txt",'r',encoding='utf-8')
    inventory = infile2.read()
    infile2.close()

    findingaid = template
    findingaid = findingaid.replace("[@[*? title ?*]@]",collection + " Collection")     # replacing the title element in the template with the title for each collection
    findingaid = findingaid.replace("[@[*? creator ?*]@]","Creator: " + collection)     # replacing the creator element in the template with the creator for each collection
    findingaid = findingaid.replace("[@[*? structured inventory ?*]@]",inventory)        # replacing the structured inventory element in the template with the inventory for each collection

    outfile = open(collection.replace(" ","-") + "-findingaid.md",'w',encoding='utf-8')
    print(findingaid, file = outfile)
    outfile.close()

def findingaids():                        #defining a function to generate finding aids for each collection
    for collection in collections:              # looping through each collection in the list of collections 
        process_findingaid(collection)           # calling on the process finding aids function and using each collection as a parameter
    
inventories()           # calling the inventories function
findingaids()           # calling the finding aids function





