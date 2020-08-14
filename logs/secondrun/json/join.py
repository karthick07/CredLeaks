import glob
import json

import pandas as pd
from database import PasteArchive

conn = PasteArchive()
result = []
for f in glob.glob("*.json"):
    with open(f, "rb") as infile:
        result.append(json.load(infile))

with open("../merged_file.json", "w") as outfile:
     json.dump(result,  outfile)
df = pd.read_json("../merged_file.json")
df1 = df[['filename','raw_paste']]
df1 = df1.rename(columns = {'raw_paste':'paste'})
df1 = df1.reset_index(drop=True)
df1.to_json("../final.json")
# os.remove("merged_file.json")
df2 = pd.read_json("../final.json")

conn.processPastes(df2)