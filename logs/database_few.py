import sqlite3


class PasteArchive(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect('pastes.db')
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute('''CREATE TABLE IF NOT  EXISTS pastes ('Full_URL' TEXT, 'Title' TEXT, 'User' TEXT, 'Filename' TEXT, 'Timestamp' TEXT, 'MD5_Hash' TEXT)''')

    def processPastes(self, item):
        self.store_db(item)
        return item

    def store_db(self, item):
        # print(item['Name / Title'][0] , item['Posted'][0], item['Syntax'][0], item['PasteID'][0] )
        for url,title,user,filename,time,md5 in zip(item['full_url'], item['title'], item['user'], item['filename'],item['timestamp'],item['MD5_Hash']):
            self.curr.execute(''' INSERT INTO pastes(Full_URL,Title,User,Filename,'Timestamp','MD5')
                          VALUES(?,?,?,?) ''', (url,title,user,filename,time,md5))
            self.conn.commit()

    #def fetchFiles(self):
        #self.curr.execute('''SELECT * IF NOT  EXISTS pastes ('filename' TEXT, 'paste' TEXT)''')

