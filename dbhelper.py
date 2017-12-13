import sqlite3
import json
import ast #abstract syntax tree

"""Query template accepts any amount of ? characters, and it accepts a third
argument, typically a tuple. The first ? in the template will be replaced
with the first element of the tuple and so on"""

class DBHelper:
    #DBHelper class can be used by our Chatbot to do everything it needs
    #Creates a database called mbdb
    def __init__(self, dbname="mbdb.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        #user table
        stmt1 = """CREATE TABLE IF NOT EXISTS
                user(chat_id int PRIMARY KEY, personality text,
                title text, link text, ei_ratio text, sn_ratio text,
                tf_ratio text, jp_ratio text)"""
        #ei_results table
        stmt2 = """CREATE TABLE IF NOT EXISTS
                ei_results(chat_id int PRIMARY KEY, extraverted_count int,
                introverted_count int, ei_contrast text)"""
        #sn_results table
        stmt3 = """CREATE TABLE IF NOT EXISTS
                sn_results(chat_id int PRIMARY KEY, sensing_count int,
                intuitive_count int, sn_contrast text)"""
        #tf_results table
        stmt4 = """CREATE TABLE IF NOT EXISTS
                tf_results(chat_id int PRIMARY KEY, thinking_count int,
                feeling_count int, tf_contrast text)"""
        #jf_results table
        stmt5 = """CREATE TABLE IF NOT EXISTS
                jf_results(chat_id int PRIMARY KEY, judging_count int,
                perceiving_count int, jp_contrast text)"""
        #question_bank table
        stmt6 = """CREATE TABLE IF NOT EXISTS
                question_bank(question_number int PRIMARY KEY, question text,
                question_type text, option_a text, option_b text)"""
        self.conn.execute(stmt1)
        self.conn.execute(stmt2)
        self.conn.execute(stmt3)
        self.conn.execute(stmt4)
        self.conn.execute(stmt5)
        self.conn.execute(stmt6)
        self.conn.commit()

    #Populate question_bank table with questions from JSON file
    def retrieve_data_from_json(self):
        dictlist = []
        with open('question_bank.json') as json_data:
            questions = json.load(json_data) #questions is a list of dictionaries
        for dictionary in questions:
            dictlist.append(list(dictionary.values()))  
        for question in dictlist:
            #Insertion of data must be converted to tuple form first
            self.conn.executemany("""INSERT INTO question_bank (question_number, question,
                                question_type, option_a, option_b) VALUES
                                (?,?,?,?,?)""", (question,))
        self.conn.commit()

    #Provide questions to user
    def getQuestions(self):
        stmt = "SELECT question FROM question_bank"
        #fetchall() is a cursor method
        question = self.conn.execute(stmt).fetchall()
        return question
        
    #Need to fix this method
    def check_for_user(self, user_id):
        for row in self.conn.execute("SELECT chat_id FROM user WHERE chat_id = wanted_id"):
            chat_id = row
            return true
            break
        return false

    #To store the results of users who attempted the test
    def add_to_ei(self, user_id, e_count, i_count, ei_contrast):
        stmt = "INSERT INTO ei_results (chat_id, extraverted_count, introverted_count, ei_contrast) VALUES (?, ?, ?, ?)"
        args = (user_id, e_count, i_count, ei_contrast)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def add_to_sn(self, user_id, s_count, n_count, sn_contrast):
        stmt = "INSERT INTO sn_results (chat_id, sensing_count, intuitive_count, sn_contrast) VALUES (?, ?, ?, ?)"
        args = (user_id, s_count, n_count, sn_contrast)
        self.conn.execute(stmt, args)
        self.conn.commit()    
    
    def add_to_tf(self, user_id, t_count, f_count, tf_contrast):
        stmt = "INSERT INTO tf_results (chat_id, thinking_count, feeling_count, tf_contrast) VALUES (?, ?, ?, ?)"
        args = (user_id, t_count, f_count, tf_contrast)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def add_to_jp(self, user_id, j_count, p_count, jp_contrast):
        stmt = "INSERT INTO jp_results (chat_id, judging_count, perceiving_count, jp_contrast) VALUES (?, ?, ?, ?)"
        args = (user_id, j_count, p_count, jp_contrast)
        self.conn.execute(stmt, args)
        self.conn.commit()

    #To reset the results of user who want to retake the test
    def reset_entry_from_ei(self, user_id):
        stmt = "UPDATE ei_results SET extraverted_count = 0, introverted_count = 0, ei_contrast = "" WHERE chat_id = user_id"
        self.conn.execute(stmt, user_id)
        self.conn.commit()
        
    def reset_entry_from_sn(self, user_id):
        stmt = "UPDATE sn_results SET sensing_count = 0, intuitive_count = 0, sn_contrast = "" WHERE chat_id = user_id"
        self.conn.execute(stmt, user_id)
        self.conn.commit()
        
    def reset_entry_from_tf(self, user_id):
        stmt = "UPDATE tf_results SET thinking_count = 0, feeling_count = 0, tf_contrast = "" WHERE chat_id = user_id"
        self.conn.execute(stmt, user_id)
        self.conn.commit()

    def reset_entry_from_jp(self, user_id):
        stmt = "UPDATE jp_results SET judging_count = 0, perceiving count = 0, jp_contrast = "" WHERE chat_id = user_id"
        self.conn.execute(stmt, user_id)
        self.conn.commit()

    #Present results of user
    def get_result(self, user_id):
        stmt = "SELECT personality, title, link FROM user WHERE chat_id = user_id)"
        self.conn.execute(stmt, user_id)
