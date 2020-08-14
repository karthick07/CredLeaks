__author__ = "Karthick Thambidurai"
__status__ = "Prototype"
import os
import subprocess
import time

#destination path is set to the output json directory where the pastes are stored.
dpath = os.getcwd() + '/logs/json'


#The below script is scheduled in such a way that it runs when it sees more than 25 pastes in the output directory.
while True:
    if dpath.find('/logs/json') > 0:
        pass
    else:
        dpath = dpath + '/logs/json'
    os.chdir(dpath)
    dir_contents = os.listdir('.')

    #To prevent running the scripts on an empty directory, the script waits until there are atleast 25 files.
    #The file size can be modified as per the requirements
    if not len(dir_contents) > 2:
        continue
    else:
        #To prevent files from being fed multiple times, the pastes that are present in the output folder is moved to a temporary folder.
        #Prefilter and prediction process are carried out from the temporary folder so that the actual output directory is not affected.
        #Only the prefiltered files are saved in the database and the temporary folder is deleted after every run.
        os.chdir('..')
        os.chdir('..')
        subprocess.call('mkdir temp',shell=True)
        subprocess.call('mv ./logs/json/* ./temp/',shell=True)
        #Invoke prefilter after files are moved into the temporary folder
        subprocess.call(['python3','prefilter.py'])
        #Remove files and temp directory after every run.
        subprocess.call('rm -rf ./temp/*',shell=True)
        subprocess.call('rmdir ./temp/',shell=True)




