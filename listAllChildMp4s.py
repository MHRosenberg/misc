import glob
import os
import platform
import csv
import datetime

### USER PARAMETERS:
CSV_NAME = 'mp4list.csv'
FILE_EXT = '.mp4'


### code from https://stackoverflow.com/questions/237079/how-to-get-file-creation-modification-date-times-in-python/39501288
### WARNING: there are known difficulties in getting a reliable unix date of creation; modification is given instead. 
def creationDate(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
#        return os.path.getctime(path_to_file)
        return os.path.getmtime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            return stat.st_mtime


cwd = os.getcwd()
pathLst = []
for path in glob.iglob(cwd + '/**/*' + FILE_EXT, recursive=True):
    pathLst.append(path)
    
#for path in glob.iglob(cwd + '/**/*.mp4', recursive=False):


#print('full paths:')
#[print(path) for path in pathLst]

#print('\n\nfile names:')

fileNameLst = []
dateLst = []
for pathInd, path in enumerate(pathLst):
    print('path #: {1}\nfound:{0}\n\n'.format(path,pathInd))
    path = path.strip() # remove new line
    tmpDate = creationDate(path)
    slashInd = path.rfind('/')
    fileName = path[slashInd+1:]
    fileDate = datetime.datetime.fromtimestamp(tmpDate)
    fileNameLst.append(fileName)
    dateLst.append(fileDate)

rows = zip(fileNameLst, dateLst, pathLst)
        
with open(CSV_NAME, 'w') as resultFile:        
    wr = csv.writer(resultFile) #, dialect='excel') # might be necessary
    for row in rows:
        print('writing row:{0}'.format(row))
        wr.writerow(row)
    
#[print(fileName) for fileName in fileLst]

print('\n\nlinux system detected.\nWARNING:No easy way to get creation dates here, using last modified instead.')



