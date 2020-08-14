import sqlite3


class PasteArchive(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect('pastes.db')
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute('''CREATE TABLE IF NOT  EXISTS pastes ('filename' TEXT, 'paste' TEXT)''')

    def processPastes(self, item):
        self.store_db(item)
        return item

    def store_db(self, item):
        # print(item['Name / Title'][0] , item['Posted'][0], item['Syntax'][0], item['PasteID'][0] )
        for filename,paste in zip(item['filename'], item['paste']):
            self.curr.execute(''' INSERT INTO pastes(filename,paste)
                          VALUES(?,?) ''', (filename,paste))
            self.conn.commit()

    def fetchFiles(self):
        self.curr.execute('''SELECT * IF NOT  EXISTS pastes ('filename' TEXT, 'paste' TEXT)''')

