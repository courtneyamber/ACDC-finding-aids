infile = open('500-notes.txt','r',encoding='utf-8')
notes = infile.read()
infile.close()
notes = notes.lower()
notes = notes.split('=500  \\\$a')


def cleanlist(phrase,notes):
    newlist = []
    for note in notes:
        if phrase not in note:
            newlist.append(note)
    return newlist

def checknotes(phrase,notes):
    ournotes = []
    for note in notes:
        if phrase in note:
            ournotes.append(note)
    return ournotes

othernotes = ['index','title','description','latest','editor','"','reprint','consulted','edition',
               'map','printed','rev.','ed.','$5dlc','$5iu-r']

newlist = []
for note in notes:
    test = cleanlist(othernotes[0],newlist)
    newlist.append(test)





# noindex = cleanlist('index',notes)
# notitle = cleanlist('title',noindex)
# nodescription = cleanlist('description',notitle)
# nolatest = cleanlist('latest',nodescription)
# noeditor = cleanlist('editor',nolatest)
# noquotes = cleanlist('"',noeditor)
# noreprint = cleanlist('reprint',noquotes)
# noconsult = cleanlist('consulted',noreprint)
# noedition = cleanlist('edition',noconsult)
# nomap = cleanlist('map',noedition)
# noprinted = cleanlist('printed',nomap)
# norev = cleanlist('rev.',noprinted)
# noed = cleanlist('ed.',norev)
# nolc = cleanlist('$5dlc',noed)
# norbml = cleanlist('$5iu-r',nolc)
# print(len(norbml))
#
# acquired = checknotes('acquired',norbml)
# signed = checknotes('signed',acquired)


