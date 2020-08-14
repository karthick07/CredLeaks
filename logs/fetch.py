import sqlite3
import pandas as pd
import json


class PasteArchive(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect('pastes.db')
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute('''CREATE TABLE IF NOT  EXISTS pastes ('Full_URL' TEXT, 'Title' TEXT, 'UserName' TEXT, 'Filename' TEXT UNIQUE , 'Timestamp' TEXT, 'MD5_Hash' TEXT, 'SHA256_Hash' TEXT, 'Content' TEXT)''')

    def processPastes(self, item):
        self.store_db(item)
        return item

    def store_db(self, item):
        try:
            for url,title,name,fname,time,md,sha2,data in zip(item['full_url'], item['title'], item['user'],item['filename'],item['@timestamp'],item['MD5'],item['SHA256'],item['raw_paste']):
                self.curr.execute(''' INSERT INTO pastes(Full_URL,Title,UserName,Filename,Timestamp,MD5_Hash,SHA256_Hash,Content)
                              VALUES(?,?,?,?,?,?,?,?) ''', (url,title,name,fname,time,md,sha2,data))
                self.conn.commit()
        except:
            pass

    def fetchFiles(self):
        result = ""
        fname = open('fnames.json')
        load_json = json.load(fname)
        print(load_json)
        for val in load_json['filename']:
            result = result + '\'' + load_json['filename'][val] + '\','
        result = result[:-1]
        query = "SELECT * FROM pastes WHERE Filename IN (" + result + ")"
        print(query)
        data = self.curr.execute(query)
        df = data.fetchall()
        df1 = pd.DataFrame(df)
        print(df1)
