# Project Narrative 
----------------------------------

The goal of this project is to create collection inventories for a series of finding aids for collections in the the Agricultural Communications Documentation Center (ACDC) in the Funk ACES Library.  Currently, we have nearly 50 collections without a finding aids.  Each of these finding aids will contain several elements including a title, creator, extent, access statement, biographical note, arrangement note, and collection inventory.  The bulk of the work needing to be done on these finding aids is creating inventories, and the rest of the elements will be brought in after those are complete in order to create the completed finding aids.  

The ACDC stores its records in our online citation database, BibLeaves.  BibLeaves is a homegrown tool that was developed by the University of Illinois Library IT, and it was designed to specifically meet the needs of the ACDC.  However, it's capabiities are limited.  In order to begin this project I needed to be able to extract the citation information from each record that was part of a collection.  To achieve this, I downloaded a .mrc file containing MARC records for all records in the database.  

After downloading this file, I needed to convert it to a format I could easily read into Python (either a .csv or a .xml file), and I needed to determine the best tool to convert the file.  First, I decided that I would convert the .mrc file into a .csv file.  After doing some research, I determined that I wanted to use pandas in order to itterate through each record, given that it has the capacity to work with larger datasets.  I decided then that converting the .mrc file to a .csv would be easiest to read into a dataframe using pandas.  Next, I was deciding whether to use C# Marc Editor or Marc Edit in order to conver .mrc file.  At first I used C# Marc Editor because I did not need admin permissions to download this tool onto my work computer.  This tool seemed to work okay, though I was getting a lot of validation errors in many records, and I was getting many extra columns in my csv that I did not need.  I decided that Marc Edit would be the better route, so I decided to work off of my personal laptop to convert the data since I was coding in PyCharm there anyway.  



-------------------

STILL IN PROGRESS 

-------------------

### 395 words
