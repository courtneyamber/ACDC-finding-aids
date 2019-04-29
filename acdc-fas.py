
##########################################
#  IMPORT COLLECTIONS TO MAKE THIS WORK  #
##########################################
                                         #
import numpy as np                       #
import pandas as pd                      #
                                         #
##########################################

########################################################################################################################
#                                    CREATE A LIST OF COLLECTION NAMES                                                 #
########################################################################################################################
                                                                                                                       #
collections = ['Volumne One Number One','AgComm Teaching','Theses','INTERPAK','Oscars in Agriculture','Eric Abbott',   #
               'Robert Agunga','Kathy Alison','George Axinn','Ovid Bay','John H. Behrens','Harvey F. Beutner',         #
               'George Biggar','Kristina M. Boone','John Brien','Claron Burnett','Francis C. Byrnes',                  #
               'Warwick Easdown','James F. Evans','Eldon Fredericks','Claude W. Gifford','James E. Grunig',            #
               'Harold D. Guither','Dixon Harper','John A. Harvey','Delmar Hatesohl','Paul C. Hixson',                 #
               'Theodore Hutchcroft','Robert Jarnagin','K. Robert Kern','Eugene A. Kroupa','Richard Lee',              #
               'Mason E. Miller','Geoffrey Moss','Fred Myers','Hadley Read','Bonnie Riechert','Stephen G-M Shenton',   #
               'Burton Swanson','Harold Swanson','Hal R. Taylor','Phillip J. Tichenor','Mark A. Tucker',               #
               'William B. Ward','Donald Watson','Larry R. Whiting','John L. Woods']                                   #
                                                                                                                       #
########################################################################################################################


########################################################################################################################
#                            DEFINE THE FUNCTION TO CREATE THE RAW INVENTORIES                                         #
########################################################################################################################
                                                                                                                       #
def raw_inventory(collection,filename):                                                                                #
                                                                                                                       #
    #READ THE CSV INTO A DATAFRAME USING PANDAS                                                                        #
    ###########################################                                                                        #
    df = pd.read_csv('acdc-records.csv')                                                                               #
                                                                                                                       #
    #CHANGE EVERYTHING IN THE DATAFRAME INTO A STRING                                                                  #
    #################################################                                                                  #
    df = df.applymap(str)                                                                                              #
                                                                                                                       #
    #DETERMINE WHICH COLUMNS UNNEEDED AND ASSIGN THOSE TO A VARIABLE                                                   #
    ################################################################                                                   #
    excol = ['RecordID', 'DateAdded', 'DateChanged', 'Author', 'Title','CopyrightDate', 'Barcode', 'Classification',   #
             'MainEntry', 'Custom1','Custom2', 'Custom3', 'Custom4', 'Custom5', 'ImportErrors','ValidationErrors',     #
             'TagNumber', 'Ind1', 'Ind2']                                                                              #
                                                                                                                       #
    #LOOP OVER DATAFRAME TO DROP UNEEDED COLUMNS                                                                       #
    ############################################                                                                       #
    for column in df.columns:                                                                                          #
        if column in excol:                                                                                            #
            df.drop(column, axis=1, inplace = True) #change the dataframe directly with inplace                        #
                                                                                                                       #
    #MAKE THE DATEFRAME ONLY INCLUDE ROWS IN WHICH THE 500 COLUMN CONTAINS A CERTAIN COLLECTION NOTE                   #
    ################################################################################################                   #
    df = df[df['500'].str.contains(collection)]                                                                        #


    df['sort'] = df['852'].str.extract('(\d+)', expand=False).astype(str)
    df.sort_values('sort',inplace=True, ascending=False)
    df = df.drop('sort', axis=1)
                                                                                                                       #
    #INITIALIZE THE CITATION LIST                                                                                      #
    #############################                                                                                      #
    citations = []                                                                                                     #
                                                                                                                       #
    #LOOP OVER EACH CELL IN THE DATAFRAME                                                                              #
    #####################################                                                                              #
    for index,row in df.iterrows():                                                                                    #
                                                                                                                       #
        #BOX NUMBER                                                                                                    #
                                                                                                                       #
        box = row["852"]                                                                                               #
        box = box.replace(                                                                                             #
            "$aAgricultural Communications Documentation Center, Funk Library, University of Illinois$j","")           #
        box = box.replace(                                                                                             #
            "$aAgricultural Communications Documentation Center, Funk Library, University of Illinois$c+. ","")        #
        box = box.replace(                                                                                             #
            "$aAgricultural Communications Documentation Center, Funk Library, University of Illinois$c+ ","")         #
        box = box.replace(                                                                                             #
            "OAK ST 338.9105 CE ","")                                                                                  #
        box = box.replace(                                                                                             #
            "$aAgricultural Communications Documentation Center, Funk Library, University of Illinois$c+","")          #
        box = box.replace(                                                                                             #
            "Oak Street 338.9105 CE. ","")                                                                             #
                                                                                                                       #
        #RECORD ID                                                                                                     #
                                                                                                                       #
        record_id = row["1"]                                                                                           #
        record_id = record_id.replace('ACDC_','')                                                                      #
        record_id = record_id.replace(                                                                                 #
            '$aAgricultural Communications Documentation Center, Funk Library, University of Illinois$c+. ',"")        #

        #AUTHOR

        author = row["100"]
        author = author.replace("$a","")
        author = author.replace("$eauthor$4aut","")
        author = author.replace("nan,","")

        #ADDITIONAL AUTHORS

        addauthor = ""
        if row["700"] != "nan":
            for subfield in row["700"].split("$"):
                if subfield != "":
                    if subfield[0] == "a":
                        addauthor += subfield[1:] + ", "
            if addauthor != "":
                addauthor = addauthor[0:len(addauthor)-2]

        #TITLE

        title = row["245"]
        title = title.replace("$a","")
        title = title.replace("$u","")

        #YEAR

        year = "undated"
        for subfield in row["260"].split("$"):
            if subfield != "":
                if subfield[0] == "c":
                    if subfield[1:] != "":
                        year = subfield[1:]

        #CREATING THE CITATION
        ######################
        if "Box" not in box:
            citation = record_id + ". " + author + ", " + addauthor + ". " + title + ". " + "(" + year + ")."
            citations.append(citation)
        else:
            citation = box + ". " + record_id + ". " + author + ", " + addauthor + ". " + title + ". " \
                       + "(" + year + ")."
            citations.append(citation)

        #CITATION
        # Box No.
        #   Record ID No. Author(s). "Title". (Year)                                                                   #
        # [852]                                                                                                        #
        #   [1]. [100$a],[700$a].[245$a].[260$c]                                                                       #
                                                                                                                       #
                                                                                                                       #
    #WRITING OUT THE FILE                                                                                              #
    #####################                                                                                              #
    outfile = open(filename,"w",encoding="utf-8")                                                                      #
    for citation in citations:                                                                                         #
        print(citation, file = outfile)                                                                                #
    outfile.close                                                                                                      #
                                                                                                                       #
########################################################################################################################



#####################################################################################################
#                      APPLYING THE RAW INVENTORIES FUNCTION TO EACH COLLECTION                     #
#####################################################################################################
                                                                                                    #
def inventories():                                                                                  #
    inventorynames = []                                                                             #
    for collection in collections:                                                                  #
        filenames = raw_inventory(collection,"'"+ collection.replace(" ","-") + "-inventory.txt")   #
        inventorynames.append(filenames)                                                            #
    return filenames                                                                                #
inventories()                                                                                       #
                                                                                                    #
#####################################################################################################


#DEFINE A FUNCTION TO CLEAN THE RAW INVENTORIES ??????????????????????????
#CLEAN WHEN CREATING THE RAW INVENTORIES ?????????????????????????????????

#####################################################################################
#               DEFINE A FUNCTION TO WRITE OUT STRUCTURED INVENTORIES               #
#####################################################################################
def structured_inventory(test):                                                     #
                                                                                    #
    infile = open(test,"rt",encoding="utf-8")                                       #
    inventory = infile.readlines()                                                  #
    infile.close()                                                                  #
    outfile = open("Harold-Swanson-clean-inventory.txt","w",encoding="utf-8")       #
    if "Box" in inventory:                                                          #
        for item in inventory:                                                      #
            print(item[0:7] + "/n" + item[9:], file = outfile)                      #
    elif "Box" not in inventory:                                                    #
        for item in inventory:                                                      #
            print("Items Without Box Number" + '/n' + item, file = outfile)         #
    outfile.close                                                                   #
                                                                                    #
structured_inventory("'Harold-Swanson-inventory.txt")                               #
                                                                                    #
#####################################################################################











