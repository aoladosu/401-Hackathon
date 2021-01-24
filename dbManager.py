import sqlite3
import string
import random


class dbManager():
    
    def __init__(self):
        # connect to database
        self.conn = sqlite3.connect("./DADB.db", check_same_thread=False)
        self.cursor = self.conn.cursor()

    def createUser(self, username, password):
        # create a new user in the database
        # return if there is an error or not
        
        values = (username, password)
        try:
            self.cursor.execute("""INSERT INTO Users (username, password) VALUES (?,?);""", values)
            self.conn.commit()
            return False
        except:
            return True
    
    def loginUser(self, username, password):
        # check that given password matches in database
        values = (username, password)
        self.cursor.execute("""SELECT id FROM Users WHERE username=? AND password=?;""", values)
        userID = self.cursor.fetchone()
        if (userID != None):        
            self.cursor.execute("""DELETE FROM Cookies WHERE userID=?;""", userID)
            self.conn.commit()
        return userID
    
    def createCookie(self, userID):
        # create a cookie for the login
        letters = string.ascii_letters
        cookie = ''.join(random.choice(letters) for i in range(5))
        values = (userID, cookie)
        try:
            self.cursor.execute("""INSERT INTO Cookies VALUES (?,?);""", values)
            self.conn.commit()
            return cookie
        except:
            raise
            
    def checkCookie(self, cookie):
        # check if a cookie is in the database
        values = (cookie,)
        self.cursor.execute("""SELECT userID FROM Cookies WHERE cookie=?;""", values)
        userID = self.cursor.fetchone()
        if (userID != None):
            userID = userID[0]
        return userID
    
    def deleteCookie(self, cookie):
        # remove cookie
        values = (cookie,)
        self.cursor.execute("""DELETE FROM Cookies WHERE cookie=?;""", values)
        self.conn.commit()
        
    def getAllEvents(self):
        # return a list of events
        self.cursor.execute("""SELECT id, title, date, location, items FROM Events;""")
        events = self.cursor.fetchall()
        return events
    
    def getEvent(self, eid):
        # return a list of events
        values = (eid,)
        self.cursor.execute("""SELECT * FROM Events WHERE id=?;""", values)
        event = self.cursor.fetchone()
        return event
    
    def createPledge(self, userID, eventID):
        # create a pledge in database, return if there is an error
        values = (userID, eventID)
        try:
            self.cursor.execute("""INSERT INTO Pledges VALUES (?,?);""", values)
            self.conn.commit()
            return False
        except:
            return True
        
    def getUsername(self, uid):
        # return user name
        values = (uid,)
        self.cursor.execute("""SELECT username FROM Users WHERE id=?;""", values)
        username = self.cursor.fetchone()
        if (username != None):
            return username[0] 
        return None
    
    def getpledges(self, ID):
        # return pledges
        values = (ID,)
        self.cursor.execute("""SELECT e.id, e.title FROM Events e, Pledges p WHERE p.userID=? AND p.eventID=e.id;""", values)
        pledges = self.cursor.fetchall()
        return pledges
    
    def getEventsForUser(self, ID):
        # return events that a user has made
        values = (ID,)
        self.cursor.execute("""SELECT * FROM Events WHERE userID=?;""", values)
        event = self.cursor.fetchall()
        return event
        
    def createEvent(self, userID, title, summary, date, location, items):
        # create event for a user, return if there is an error
        values = (userID, title, summary, date, location, items)
        try:
            self.cursor.execute("""INSERT INTO Events (userID, title, summary, date, location, items) VALUES (?,?,?,?,?,?);""", values)
            self.conn.commit()
            return False
        except:
            return True
        
    def searchEvents(self, keywords):
        # return events matching keywords
        
        
        query = '''SELECT id, title, date, location, items FROM Events WHERE
                    title LIKE '%{}%'
                    OR location LIKE '%{}%'
                    OR items LIKE '%{}%'
                '''.format(keywords[0],keywords[0],keywords[0])
        criteria = '''
                    OR title LIKE '%{}%'
                    OR location LIKE '%{}%'
                    OR items LIKE '%{}%'
                    ''' 
        keywords.pop(0)
                    
        # build query            
        for keyword in keywords:
            query += criteria.format(keyword,keyword,keyword)
        query += ';'
        
        self.cursor.execute(query)
        events = self.cursor.fetchall()
        return events

    











 
    