## Narrative (thus far) 

The goal of this project is to create a series of finding aids for collections in the the Agricultural Communications Documentation Center (ACDC) in the Funk ACES Library.  Each of these finding aids will contain several elements including a title, creator, extent, access statement, biographical note, arrangement note, and collection inventory.

To begin, I downloaded a .mrc file for all records from the ACDC's database, BibLeaves.  Documents that belong to a particular collection should include a note in the record indicating such, e.g. "James F. Evans Collection".  I then converted this .mrc file to a csv using C# Marc Editor.  I am still trying to determine whether to convert these records to either a .csv or .xml in Marc Edit. 

I've decided a dataframe is easiest to work with this large of a file (Reading in the csv in python wasn't working out so well). I've been researching out to work with dataframes in python, and have been slowing making progress. 

I've worked through a 'rough draft' of an inventory, but fields still need to be cleaned.  

(Still working on transferring notes from my work notebook to my narrative, most of the time I was getting lost down rabbit holes and forgetting to write down my progress and challenges). 



## Detailed Sketch of Project (with questions)

1. Download .mrc file of all records from BibLeaves
2. Convert the .mrc file to a .csv (or .xml) using C# Marc Editor (or Marc Edit) *** C# Marc Editor gave me a lot of import errors in the csv, so trying to figure out if I should use Marc Edit to avoid this or if its a problem with the .mrc file itself. 
3. Read in the .csv into python as a dataframe using pandas. 
4. Drop out any unnecessary columns from the dataframe- determine which columns are completely empty and drop these
5. Change all of the content in the dataframe into strings so that you can iterate over them
6. Search for each collection note in the dataframe and only work with that portion of dataframe at a time -would be within the 500 note column (this is only going to apply to clean data right now, deal with messy data after). 
7. Iterate over the dataframe containing collection notes in a for loop, pull out citation information, clean, and write out into a text file.
8. Read in text files, incorporate other elements of each finding aid. 


### Code for this project is under acdc-fas.py
