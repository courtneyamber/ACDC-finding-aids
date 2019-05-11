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

    for index,row in df.iterrows():                           # iterating through each cell in the dataframe
        if row["SortKey"].isdigit():                           # checking to see if the information in the sort key row is a                                                                  digit   
            row["SortKey"] = row["SortKey"].zfill(25)           # if so, ?????????????????
        elif row["SortKey"] == "nan":                           # checking to see if the information in the sort key row is                                                                   nothing
            row["SortKey"] = "".rjust(25, 'Z')                  # if so, ??????????????????????????
        else:                                                   # checking for anything else
            row["SortKey"] = row["SortKey"].upper()             # ??????????????????????????

    df.sort_values(["SortKey","Folder"], ascending=[True,True],inplace=True)
    df.reset_index(drop=True,inplace=True)
    df.drop('SortKey', axis=1,inplace=True)

## DataFrame now contains the fields Box, Folder, Subfield, PlusIndictor, RemainingData
##     Subfield -- subfield letter that contained the box data
##     PlusIndictor -- plus sign in found proceeding subfield letter
##     RemainingData  -- remaining data found in box subfield
##  only data from the box subfield is used to populate these extra field

    citations = []                             # Initializing the list for all of the citations the collection to go in
    for index,row in df.iterrows():             # looping over every cell in the dataframe 
        box = row['Box']                        # assigning box as what is contained in row "Box"
        folder = row['Folder']                   # assigning folder as what is contained in row "Folder"
        record_id = row["1"]                       # assigning the record_id to what is contained in row "1"
        record_id = record_id.replace('ACDC_','')      #replacing the beginning of the record_id so it only contains the                                                              actual number
        author = ""                              # initializing the author variable as an empty string
        for subfield in row['100']:             # looping over each subfield in row 100 (aka the author information)
            if subfield != "nan":                 # checking to see if the subfield doesn't equal nothing
                if subfield[0] =="a":             # if the first index position of that 
                    author = subfield[1:]
        addauthor = ""                            # initializing the additional author variable (addauthor) as an empty                                                          string  
        if row["700"] != "nan":                         # checking to see if row 700 does not equal nothing 
            for subfield in row["700"].split("$"):      # splitting row 700 on the delimeter and looping through each                                                                 subfield
                if subfield != "":                         # checking to see if the subfield does not equal an empty string
                    if subfield[0] == "a":                  # checking to see if the index position of 0 equals an a
                        addauthor += subfield[1:] + ", "      # if so, adding the rest of that subfield information after                                                                  the a to the addauthor variable along with a comma and space
            if addauthor != "":                               # checking to see if the addauthor field variable doesn't                                                                       equal nothing
                addauthor = addauthor[0:len(addauthor)-2]       # ???????????????????????
        title = row["245"]                                  # assigning the contents of row 245 to the title variable
        title = title.replace('$a','')                      # replacing the delimeter and subfield a with nothing
        year = "undated"                                #initalizing the year variable as undated (used for things with no                                                            date information 
        for subfield in row["260"].split("$"):          # splitting row 260 on the delimeter and looping over each subfield
            if subfield != "":                           # checking to see if the subfield doesn't equal nothing
                if subfield[0] == "c":                   # checking to see if the first index position in subfield equals c
                    if subfield[1:] != "":                  # if the remaining content of subfield c doen't equal nothing...
                        year = subfield[1:]                 # ... assigning this information to variable year 

        citation = ""                   # Initialized each citation to be created as an empty string

        if box != "nan":                # checking to see if the box variable doesn't equal nothing
            citation += box + '. '      # if box doesn't equal nothing, adding the contents of box to citation along with a                                           period and space
        if folder != "nan":             # checking to see if the folder variable doesn't equal nothing
            citation += folder + '. '   # if folder doesn't equal nothing, adding the contents of folder to citation along                                             with a period and space
        citation += record_id           # adding the record_id to the ciation 
        if author != "nan":             # checking to see if author doesn't equal nothing
            citation += author + ", "   # if author doesn't equal nothing, adding the contents of author to citation, along                                           with a comma
        if addauthor != "nan":          # checking to see if addauthor doesn't equal nothing
            citation += addauthor       # if addauthor doesn't equal nothing, adding the contents of addauthor (that is any                                            additional author) to the citation
        citation += title +". "         # adding the contents of title to the citation along with a period and space
        citation += "(" + year +")."    # adding the contents of year to the citation, along with encompassing parathesis                                             and a period at the end

        citations.append(citation)          # adding each citation to the citations list
    outfile = open(filename,"w",encoding="utf-8")         # opening outfile (aka the raw inventory)
    outfile2 = open(filename_struc,'w',encoding='utf-8')    # opening outfile2 (aka the structured inventory) 

    lastbox = ""                  # initializing the lastbox variable as an empty string 
    for citation in citations:        #looping over each citation in the list of citations
        print(citation, file = outfile)     # printing the citation to the outfile (aka the raw inventory)
        box = citation.split(". ")[0]       # splitting each citation on a period-space, taking the first index position of                                               that new string, and assigning it to the variable "box"
        if lastbox != box:                  # looking to see if the lastbox does not equal box
            print(box, file = outfile2)     # printing out box to outfile2 (aka the structured inventory)
        print(citation[citation.find(". ")+1:], file = outfile2)    #finding the portion of ciation that follows the box                                                                          information and printing that out to outfile2 (aka the                                                                        structured inventory) beneath the box information 
        lastbox = box                      # assigning lastbox as box to keep track of the last box number in the list that                                               way each citation with the same box is grouped together beneath that box                                                      statement

    outfile.close()       #closing both files
    outfile2.close()
    
def inventories():      #defining a function that will run each collection to the process collection function 
    for collection in collections:    #iterating through each collection in the collections list
        process_collection(collection, collection.replace(" ","-") + "-inventory.txt", collection.replace(" ","-")+ "-structured-inventory.txt")            # adding parameters into the process collection function

def process_findingaid(collection):       # defining a function that processes each of the 
    infile = open('fa_template.txt','r',encoding='utf-8')     # opening the finding aid template
    template = infile.read()                # reading in the finding aid template     
    infile.close()                          # closing the finding aid template file 

    infile2 = open(collection.replace(" ","-")+ "-structured-inventory.txt",'r',encoding='utf-8')   #reading in the                                                                                                             structured inventory to                                                                                                       be added to the                                                                                                             finding aid
    inventory = infile2.read()    
    infile2.close()

    findingaid = template
    findingaid = findingaid.replace("[@[*? title ?*]@]",collection + " Collection")     # replacing the title element in the                                                                                          template with the title for each                                                                                              collection
    findingaid = findingaid.replace("[@[*? creator ?*]@]","Creator: " + collection)     # replacing the creator element in                                                                                              the template with the creator for                                                                                             each collection
    findingaid = findingaid.replace("[@[*? structured inventory ?*]@]",inventory)        # replacing the structured                                                                                                   inventory element in the                                                                                                      template with the inventory for                                                                                               each collection

    outfile = open(collection.replace(" ","-") + "-findingaid.md",'w',encoding='utf-8')   # writing out each finding aid as                                                                                             a .md file
    print(findingaid, file = outfile)
    outfile.close()

def findingaids():                        #defining a function to generate finding aids for each collection
    for collection in collections:              # looping through each collection in the list of collections 
        process_findingaid(collection)           # calling on the process finding aids function and using each collection as                                                     a parameter
    
inventories()           # calling the inventories function
findingaids()           # calling the finding aids function





