import flask
from flask import Flask, request, redirect, url_for
import dbManager
import htmlMaker
from datetime import *
app = Flask(__name__)
app.debug = True
db = dbManager.dbManager()
    
def checkCookie():    
    try:
        cookie = request.headers["Cookie"].split("=")[1]
        userID = db.checkCookie(cookie)
        return userID
    except:
        return None
        
def isNotLoggedIn():
    # not logged in return error page
    errorString = "You must be logged in"
    html += htmlMaker.loginFailMSG(errorString)
    return html, 200
    
    
# url routes from here on    
@app.route("/", methods=["GET"])
def loginPage():

    if (checkCookie()):
        # already logged in
        return redirect(url_for('listEvents'))
        
    try:
        # return log in page
        html = htmlMaker.loginPage()
    except:
        return '', 404
    return html, 200


@app.route("/login", methods=["POST"])
def login():
        
    error = False
    
    # get login info
    username = request.form["username"]
    password = request.form["pass"]
    loginType = request.form["loginType"]

    # check for enough information
    if (not username or not password):
        error = True
        errorString = "Not enough information provided"
    else:
        # check db for valid user
        if (loginType == "create"):
            error = db.createUser(username, password)
            errorString = "A user with that username already exists"
        if (not error):
            userID = db.loginUser(username, password)
            error = (userID == None)
            errorString = "The username and password do not match"

    
    if (error):
        # return error page
        html = htmlMaker.loginFailMSG(errorString)
        return html, 200
    else:
        # create a cookie
        cookie = db.createCookie(userID[0])
        response = redirect(url_for('listEvents'), 302)
        response.set_cookie("session", cookie)
        return response
    
    
@app.route("/logout", methods=["POST"])
def logout():
    # logout the user
    
    try:
        cookie = request.headers["Cookie"].split("=")[1]
        db.deleteCookie(cookie)
    except:
        pass  
    return redirect(url_for('loginPage'))
    

@app.route("/events", methods=["GET", "POST"])
def listEvents():
    # list all events
    
    # must be logged in
    if (not checkCookie()):
        return isNotLoggedIn()
    
    if ((request.method == "GET") or (not request.form["keywords"])):
        try:
            events = db.getAllEvents()
            html = htmlMaker.listEvents(events, False)
        except:
            return '', 404
        
    else:
        # a search
        keywords = request.form["keywords"].split()
        events = db.searchEvents(keywords)
        html = htmlMaker.listEvents(events, True)
        
    return html, 200

@app.route("/event/<ID>", methods=["GET"])
def showEvent(ID):
    
    # must be logged in
    userID = checkCookie()
    if (not userID):
        return isNotLoggedIn()
    
    username = db.getUsername(userID)
    event = db.getEvent(ID)
    if (event == None):
        return redirect(url_for('listEvents'))
    html = htmlMaker.showEvent(event, username, '')
    return html, 200
  
@app.route("/pledge/<ID>", methods=["POST"])
def pledge(ID):
    # pledge to donate an item
    
    # must be logged in
    userID = checkCookie()
    if (not userID):
        return isNotLoggedIn()
    
    if (db.createPledge(userID, ID)):
        resultString = "You've already pledged to this event!"
    else:
        resultString = "Thank you for pledging to donate to this event!"
        
    username = db.getUsername(userID)    
    event = db.getEvent(ID)
    if (event == None):
        return redirect(url_for('listEvents'))    
    html = htmlMaker.showEvent(event, username, resultString)
    return html, 200
    
@app.route("/profile/<ID>", methods=["GET"])
def profile(ID):
    # show users profile
    
    # must be logged in
    userID = checkCookie()
    if (not userID):
        return isNotLoggedIn()
    if ((ID == '0') or (ID == '0?')):
        ID = userID
    
    username = db.getUsername(ID)
    if (username == None):
        return redirect(url_for('listEvents'))
    pledges = db.getpledges(ID)
    events = db.getEventsForUser(ID)
    html = htmlMaker.showProfile(username, events, pledges)
    return html, 200
    
@app.route("/newEvent", methods=["GET"])
def newEvent():    
    # create a new event
    
    # must be logged in
    userID = checkCookie()
    if (not userID):
        return isNotLoggedIn()
    
    html = htmlMaker.createEvent('')
    return html, 200
    
@app.route("/createEvent", methods=["POST"])
def createEvent():    
    # create a new event
    
    # must be logged in
    userID = checkCookie()
    if (not userID):
        return isNotLoggedIn()
    
    # get data
    title = request.form["title"]
    summary = request.form["summary"]
    eventDate = request.form["date"]
    location = request.form["location"]
    items = request.form["items"]

    # check for all info
    if (not title or not summary or not eventDate or not location or not items):
        html = htmlMaker.createEvent('Not enough information provided')
        return html, 200
    
    # check for date
    dateSplit = eventDate.split("-")
    d1 = date(int(dateSplit[0]),int(dateSplit[1]),int(dateSplit[2]))
    d2 = date.today()
    if (d2>d1):
        html = htmlMaker.createEvent('Cannot create an event in the past')
        return html, 200
    
    if (db.createEvent(userID, title, summary, eventDate, location, items)):
        html = htmlMaker.createEvent('A similar event has already been created')
    else:
        html = htmlMaker.createEvent('Event created!')
    return html, 200
    
    
if __name__ == "__main__":
    app.run()    
    
    
    
    
    
    
    
    
    
    
    
    