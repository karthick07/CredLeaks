#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3


class PasteArchive(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect('pastes.db')
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute('''CREATE TABLE IF NOT  EXISTS pastes ('Full_URL' TEXT , 'Title' TEXT , 'User' TEXT , 'Filename' TEXT UNIQUE, 'Timestamp' TEXT , 'MD5_Hash' TEXT , 'SHA256_hash' TEXT, 'Content' TEXT, 'Yara_rule' TEXT)'''
                          )

    def processPastes(self, item):
        self.store_db(item)
        return item

    def store_db(self, item):

        for (
            url,
            title,
            user,
            filename,
            time,
            md5,
	    sha2,
            data,
	    yara
            ) in zip(
            item['full_url'],
            item['title'],
            item['user'],
            item['filename'],
            item['@timestamp'],
            item['MD5'],
	    item['SHA256'],
	    item['raw_paste'],
	    item['YaraRule']
            ):
            try:
                self.curr.execute(''' INSERT INTO pastes(Full_URL,Title,User,Filename,'Timestamp','MD5_Hash', 'SHA256_Hash','Content','Yara_rule' VALUES(?,?,?,?,?,?,?,?,?) '''
                                  , (
                    url,
                    title,
                    user,
                    filename,
                    time,
                    md5,
                    sha2,
		    data,
		    yara
                    ))
                self.conn.commit()
            except:
                pass


    # def fetchFiles(self):
        # self.curr.execute('''SELECT * IF NOT  EXISTS pastes ('filename' TEXT, 'paste' TEXT)''')

