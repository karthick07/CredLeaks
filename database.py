import sqlite3
import json
import pandas as pd


class PasteArchive(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    # creates a connection and resultant pastes are stored in a database file named pastes.db
    def create_connection(self):
        self.conn = sqlite3.connect('pastes.db')
        self.curr = self.conn.cursor()

    # create table with the all relevant fields.
    def create_table(self):
        self.curr.execute(
            '''CREATE TABLE IF NOT  EXISTS pastes ('Full_URL' TEXT, 'Title' TEXT, 'UserName' TEXT, 'Filename' TEXT UNIQUE , 'Timestamp' TEXT, 'MD5_Hash' TEXT, 'SHA256_Hash' TEXT, 'Content' TEXT)''')

    def processPastes(self, item):
        self.store_db(item)
        return item

    # storing of paste metadata and paste content
    def store_db(self, item):
        try:
            for url, title, name, fname, time, md, sha2, data in zip(item['full_url'], item['title'], item['user'],
                                                                     item['filename'], item['@timestamp'], item['MD5'],
                                                                     item['SHA256'], item['raw_paste']):
                self.curr.execute(''' INSERT INTO pastes(Full_URL,Title,UserName,Filename,Timestamp,MD5_Hash,SHA256_Hash,Content)
                              VALUES(?,?,?,?,?,?,?,?) ''', (url, title, name, fname, time, md, sha2, data))
                self.conn.commit()
        except:
            pass

    # Fetch files after prediction based on filenames(pasteIDs)
    def fetchFiles(self):
        result = ""
        # file containing predicted IDs are loaded
        fname = open('../predictedIDs.json')
        load_json = json.load(fname)
        # All corresponding values for the respective ID are retrieved from the database
        for val in load_json['filename']:
            result = result + '\'' + load_json['filename'][val] + '\','
        result = result[:-1]
        query = "SELECT * FROM pastes WHERE Filename IN (" + result + ")"
        data = self.curr.execute(query)
        df = data.fetchall()
        #For the POC, the files that are fetched from the DB are printed to show everything works.
        # However in the future enhancement the files can be stored in a common file format and can be analysed further or monitored.
        filenames = pd.DataFrame(df)
        print(filenames)

