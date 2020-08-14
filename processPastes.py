import glob
import json
import os
import pandas as pd
import pickle
import time
from sklearn.pipeline import Pipeline
from database import PasteArchive
import preprocessing

conn = PasteArchive()
result = []
dpath = os.path.abspath(os.path.curdir)
os.chdir(dpath)

def process():

    try:
        # In the current setup, the json files in the output directory are merged and the merged file is stored in the database and also fed to the model
        for f in glob.glob("*"):
            with open(f, "rb") as infile:
                result.append(json.load(infile))

        # Save merged file in the current directory
        with open("../merged_file.json", "w") as outfile:
            json.dump(result, outfile)
        # Open merged file
        df = pd.read_json("../merged_file.json")
        # All relevant fields like URL,title,username,pasteID,hash of the pastes and content are stored in a seperate dataframe which is passed to database
        extractedfields = df[['full_url', 'title', 'user', 'filename', '@timestamp', 'MD5', 'SHA256', 'raw_paste']]
        print(extractedfields)
        # Stores all fields from df2 into the database
        conn.processPastes(extractedfields)
        totalfiles = len(extractedfields)
        print("Source code files are filtered and % d files are added to the database" %totalfiles)
    except Exception:
        print("Exception occured while merging json files and storing it in the database")



def predict_pii():
    try:
        # Loads the saved pickle file which consists of the Machine learning model
        print("Predicting PII pastes !!!! ")
        with open('../model.pickle', 'rb') as picklefile:
            saved_pipe = pickle.load(picklefile)
        # Read merged json file
        readMergedfile = pd.read_json("../merged_file.json")

        # Since the model only requires filename and content it is extracted and saved into a new dataframe
        extractPaste = readMergedfile[['filename', 'raw_paste']]
        # Column is renamed
        extractPaste = extractPaste.rename(columns={'raw_paste': 'paste'})
        extractPaste = extractPaste.reset_index(drop=True)

        # Remove duplicate pastes from the output folder
        extractPaste = extractPaste.drop_duplicates(['paste'])
        extractPaste = extractPaste.reset_index(drop=True)
        #Apply preprocessing steps
        preprocessing.preprocess(extractPaste)
        print(extractPaste)
        # Invoke predict method which returns a 0 or 1 based on the content (1 depicts PII and 0 depicts notPII)
        unseenVals = saved_pipe.predict(extractPaste.paste)
        # Predicted labels are stored into a new dataframe
        finalLabels = pd.DataFrame(unseenVals, columns=["predictedLabels"])
        # Predicted values are then merged with the filenames so that labels with 1 can be seperated easily
        extractPaste = extractPaste.join(finalLabels)
        # Filenames that has a label 1 are seperated and saved as a new file in the current directory
        PIIfnames = extractPaste.loc[extractPaste['predictedLabels'] == 1]
        files = pd.DataFrame(PIIfnames['filename'], columns=['filename'])
        #If no files are predicted as PII in the current run the process is repeated from the beginning.
        if files.empty:
            print("No PII pastes found in the current run")
            return
        # files = files.reset_index(drop=True, inplace=True)
        totalpastes = len(files)
        print("Number of pastes that are predicted as PII are % d" %totalpastes)
        #Files that are predicted as PII are saved as a new json files which only consist of the Paste IDs
        files.to_json("../predictedIDs.json")
        print("Fetching contents of PII predicted pastes")
        #Invoke fetch command from the database file to fetch contents corresponding to the predicted paste IDs.
        conn.fetchFiles()
    except Exception as e:
        print("Exception occured during prediction and fetching files from the database"+e)



