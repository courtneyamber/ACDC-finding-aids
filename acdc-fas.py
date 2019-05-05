import numpy as np
import pandas as pd

collections = ['Volumne One Number One','AgComm Teaching','Theses','INTERPAK','Oscars in Agriculture','Eric Abbott',
               'Robert Agunga','Kathy Alison','George Axinn','Ovid Bay','John H. Behrens','Harvey F. Beutner',
               'George Biggar','Kristina M. Boone','John Brien','Claron Burnett','Francis C. Byrnes',
               'Warwick Easdown','James F. Evans','Eldon Fredericks','Claude W. Gifford','James E. Gruning',
               'Harold D. Guither','Dixon Harper','John A. Harvey','Delmar Hatesohl','Paul C. Hixson',
               'Theodore Hutchcroft','Robert Jarnagin','K. Robert Kern','Eugene A. Kroupa','Richard Lee',
               'Mason E. Miller','Geoffrey Moss','Fred Myers','Hadley Read','Bonnie Riechert','Stephen G-M Shenton',
               'Burton Swanson','Harold Swanson','Hal R. Taylor','Phillip J. Tichenor','Mark A. Tucker',
               'William B. Ward','Donald Watson','Larry R. Whiting','John L. Woods']


def process_collection(collection,filename,filename_struc):
    df = pd.read_csv('acdc-records.csv')
    df = df.applymap(str)
    df = df[df['500'].str.contains(collection)]

    #Add box and folder cleaning thing

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
    df['Subfield'] = df['852'].str.\
                            extract(r'.*\$(?P<Subfield>[a-z])\+*.*Box:.*').astype(str).Subfield
    df['RemainingData'] = df['852'].str.replace('Box:.*', '', regex=True).astype(str).str.rstrip()
    df.sort_values(['Box','Folder','RemainingData','Title'], ascending=[True,True,True,True],inplace=True)
    df.reset_index(drop=True,inplace=True)

## DataFrame now contains the fields Box, Folder, Subfield, PlusIndictor, RemainingData
##     Subfield -- subfield letter that contained the box data
##     PlusIndictor -- plus sign in found proceeding subfield letter
##     RemainingData  -- remaining data found in box subfield
##  only data from the box subfield is used to populate these extra field

    citations = []
    for index,row in df.iterrows():
        box = row['Box']
        folder = row['Folder']
        record_id = row["1"]
        record_id = record_id.replace('ACDC_','')
        author = ""
        for subfield in row['100']:
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
        box = citation.split(".")[0]
        if lastbox != box:
            print(box, file = outfile2)
        print(citation[citation.find(".")+1:], file = outfile2)
        lastbox = box

    outfile.close()
    outfile2.close()


def inventories():
    for collection in collections:
        process_collection(collection,"'"+ collection.replace(" ","-") + "-inventory.txt","'" + collection.replace(" ","-")+ "-structured-inventory.txt")


inventories()










