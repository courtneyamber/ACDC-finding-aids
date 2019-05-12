import numpy as np
import pandas as pd

collections = ['Volume One Number One','AgComm Teaching','Thesis','INTERPAK','Eric Abbott',
                'Robert Agunga','Kathleen I. Alison','George H. Axinn','Ovid Bay','John Behrens','Harvey F. Beutner',
                'Kristina M. Boone','John Brien','Claron Burnett','Francis C. Byrnes','Warwick Easdown',
               'James F. Evans','Eldon Fredericks','James E. Grunig','Dix Harper','John Harvey','Delmar Hatesohl',
               'Paul C. Hixson','Theodore Hutchcroft','K. Robert Kern','Eugene A. Kroupa','Mason E. Miller',
               'Geoffrey Moss','Fred Myers','Bonnie Riechert','Burton Swanson','Harold Swanson','Hal R. Taylor',
               'William B. Ward','Larry R. Whiting','John L. Woods']

def process_collection(collection,filename,filename_struc):
    df = pd.read_csv('acdc-records.csv')
    df = df.applymap(str)
    df = df[df['500'].str.contains(collection)]

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

    citations = []
    for index,row in df.iterrows():
        box = row['Box']
        folder = row['Folder']
        record_id = row['001']
        record_id = record_id.replace('ACDC_','')
        author = ""
        if row["100"] != "nan":
            for subfield in row['100'].split("$"):
                if subfield[0] == "a":
                    author = subfield[1:]
        addauthor = ""
        if row["700"] != "nan":
            for subfield in row['700'].split("$"):
                if subfield[0] == "a":
                    addauthor += subfield[1:] + ", "
            if addauthor != "":
                addauthor = addauthor[0:len(addauthor)-2]
        title = ""
        if row["245"] != "nan":
          for subfield in row['245'].split("$"):
            if subfield[0] == "a":
                title = subfield[1:]
        year = "undated"
        if row["260"] != "nan":
            for subfield in row['260'].split("$"):
                if subfield[0] == "c":
                    year = subfield[1:]

        citation = ""
        if box != "nan":
            citation += box + '. '
        if folder != "nan":
            citation += folder + '. '
        citation += record_id + ". "
        if author != "":
            citation += author + ", "
        if addauthor != "":
            citation += addauthor + ", "
        citation += '"' + title + '". '
        citation += "(" + year + ")."
        citations.append(citation)

    outfile = open(filename,"w",encoding="utf-8")
    outfile2 = open(filename_struc,'w',encoding='utf-8')

    lastbox = ""
    for citation in citations:
        print(citation, file = outfile)
        box = citation.split(". ")[0]
        if lastbox != box:
            print("__**" + box + "**__" + "\n", file = outfile2)
        print(citation[citation.find(". ")+1:] + "\n", file = outfile2)
        lastbox = box

    outfile.close()
    outfile2.close()

def inventories():
    for collection in collections:
        process_collection(collection, collection.replace(" ","-") + "-raw-inventory.txt",
                           collection.replace(" ","-")+ "-structured-inventory.txt")

def process_findingaid(collection):
    infile = open('fa_template.txt','r',encoding='utf-8')
    template = infile.read()
    infile.close()

    infile2 = open(collection.replace(" ","-")+ "-structured-inventory.txt",'r',encoding='utf-8')
    inventory = infile2.read()
    infile2.close()

    findingaid = template
    findingaid = findingaid.replace("[@[*? title ?*]@]", collection + " Collection")
    findingaid = findingaid.replace("[@[*? creator ?*]@]", collection)
    findingaid = findingaid.replace("[@[*? structured inventory ?*]@]",inventory)

    outfile = open(collection.replace(" ","-") + "-findingaid.md",'w',encoding='utf-8')
    print(findingaid, file = outfile)
    outfile.close()

def findingaids():
    for collection in collections:
        process_findingaid(collection)

inventories()
findingaids()
