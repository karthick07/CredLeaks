# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 11:07:25 2020

@author: Karthik
"""

import pickle
from sklearn.pipeline import Pipeline
import pandas as pd
with open('PII_model_hack.pickle', 'rb') as picklefile:
    saved_pipe = pickle.load(picklefile)
final_df = pd.read_json("final.json")
final_df = final_df.reset_index(drop = True) 
unseenVals = saved_pipe.predict(final_df.paste)
finalLabels = pd.DataFrame(unseenVals,columns=["predictedLabels"])
final_df = final_df.join(finalLabels)
PIIfnames = final_df.loc[final_df['predictedLabels'] == 1]
files = PIIfnames['filename']
files = files.reset_index(drop=True, inplace=True)
print(files)
files.to_json("predictedFiles.json")
