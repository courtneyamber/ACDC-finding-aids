# Project Narrative 
----------------------------------

The goal of this project is to create collection inventories for a series of finding aids for collections in the the Agricultural Communications Documentation Center (ACDC) in the Funk ACES Library.  Currently, we have nearly 50 collections without a finding aids.  Each of these finding aids will contain several elements including a title, creator, extent, access statement, biographical note, arrangement note, and collection inventory.  The bulk of the work needing to be done on these finding aids is creating inventories, and the rest of the elements will be brought in after those are complete in order to create the completed finding aids.  

The ACDC stores its records in our online citation database, BibLeaves.  BibLeaves is a homegrown tool that was developed by the University of Illinois Library IT, and it was designed to specifically meet the needs of the ACDC.  However, it's capabiities are limited.  In order to begin this project I needed to be able to extract the citation information from each record that was part of a collection.  To achieve this, I downloaded a .mrc file containing MARC records for all records in the database.  

After downloading this file, I needed to convert it to a format I could easily read into Python (either a .csv or a .xml file), and I needed to determine the best tool to convert the file.  First, I decided that I would convert the .mrc file into a .csv file.  After doing some research, I determined that I wanted to use pandas in order to itterate through each record, given that it has the capacity to work with larger datasets.  I decided then that converting the .mrc file to a .csv would be easiest to read into a dataframe using pandas.  Next, I was deciding whether to use C# Marc Editor or Marc Edit in order to conver .mrc file.  At first I used C# Marc Editor because I did not need admin permissions to download this tool onto my work computer.  This tool seemed to work okay, though I was getting a lot of validation errors in many records, and I was getting many extra columns in my csv that I did not need.  I decided that Marc Edit would be the better route, so I decided to work off of my personal laptop to convert the data since I was coding in PyCharm there anyway. 

After doing some research into working with pandas, I began to write my code.  To start I had to install the pandas and numpy collections through Anaconda, and then import the two in my code.  Next, I gathered a list of collection I knew we held, but did not have finding aids for.  I assigned this list to the variable "collections" becuase I knew it would be much easy to iterate through this list then to would be to enter each of these collections into the rest of my program individually.  

Next, I worked on creating the first function: One that would process each of these collections and return to me an inventory.  I began first with just returning a raw inventory to make it easy to look for patterns in each citation, and enable me to have a better idea of patterns to look for when I was cleaning the data.  I found that the easiest way to be able to extract the box and folder information from 852 field would be to go back and use regex to find each of those instances and add as a new row in the dataframe.  Adding each of the citations I created to a list 

After I had the raw inventories all set, I went about adding in another outfile that would group each citation by box in order to create structured inventories.  This is the inventory that I would need add to each of the finding aids.  I created this by looking for.... First I needed to make sure that the citation were sorted numerically by box number, and that anything without a box number would be together at the end (these ones I need to find in our collection and add in box numbers for). 

After I had my structured inventories complete, I created a finding aid in a text file.  In this template I included both field content that would remain constant across all collection finding aids, and for content that would differ, I added an element that I would replace with content created by the program, e.g. inventories and collection titles. 





...


I decided to write out the finding aids in .md files.  I did this so that I would be able to easily convert those .md files to .doc files and then to .pdf files without fussing over formatting.  

Moving forward, I will need to read in the biographical notes the Center has been working on created.  



-------------------

STILL IN PROGRESS 

-------------------

### 750 words
