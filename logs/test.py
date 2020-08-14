#!/usr/bin/python
# -*- coding: utf-8 -*-
import glob
import json
import os
import pandas as pd
import pickle
import time
from sklearn.pipeline import Pipeline
from database import PasteArchive


def process():

    conn = PasteArchive()
    result = []
    dpath = os.path.abspath(os.path.curdir)
    os.chdir(dpath)

    # In the current setup, the json files in the output directory are merged and the merged file is stored in the database and also fed to the model

    for f in glob.glob('*.json'):
        with open(f, 'rb') as infile:
            result.append(json.load(infile))

    # Save merged file in the current directory

    with open('../merged_file.json', 'w') as outfile:
        json.dump(result, outfile)

    # Open merged file

    df = pd.read_json('../merged_file.json')

    # Since the model only requires filename and content it is extracted and saved into a new dataframe

    df1 = df[['filename', 'raw_paste']]

    # Column is renamed

    df1 = df1.rename(columns={'raw_paste': 'paste'})
    df1 = df1.reset_index(drop=True)

    # All relevant fields like URL,title,username,pasteID,hash of the pastes and content are stored in a seperate dataframe which is passed to database

    df2 = df[[
        'full_url',
        'title',
        'user',
        'filename',
        '@timestamp',
        'MD5',
        'SHA256',
        'raw_paste',
        ]]
    print(df2)

    # df2 = pd.read_json("../final.json")
    # Stores all fields from df2 into the database

    conn.processPastes(df2)

    # Loads the saved pickle file which consists of the Machine learning model

    with open('../prep.pickle', 'rb') as picklefile:
        saved_pipe = pickle.load(picklefile)

    # Read merged json file

    final_df = pd.read_json('../merged_file.json')
    final_df = final_df.rename(columns={'raw_paste': 'paste'})

    # Remove duplicate pastes from the output folder

    final_df = final_df.drop_duplicates(['paste'])
    final_df = final_df.reset_index(drop=True)

    # Invoke predict method which returns a 0 or 1 based on the content (1 depicts PII and 0 depicts notPII)

    unseenVals = saved_pipe.predict(final_df.paste)

    # Predicted labels are stored into a new dataframe

    finalLabels = pd.DataFrame(unseenVals, columns=['predictedLabels'])

    # Predicted values are then merged with the filenames so that labels with 1 can be seperated easily

    final_df = final_df.join(finalLabels)

    # Filenames that has a label 1 are seperated and saved as a new file in the current directory

    PIIfnames = final_df.loc[final_df['predictedLabels'] == 1]
    files = pd.DataFrame(PIIfnames['filename'], columns=['filename'])
    print(files)

    # files = files.reset_index(drop=True, inplace=True)

    files.to_json('../predictedIDs.json')
    time.sleep(1)

    # Invoke fetch command from the database file to fetch contents corresponding to the filenames stored.

    conn.fetchFiles()

