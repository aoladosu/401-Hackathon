import flask
from flask import Flask, request, redirect, url_for
import json
import dbManager
import htmlMaker
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
    file = open("pages/loginFail.html", 'r')
    html = file.read()
    file.close()
    errorString = "You must be logged in"
    html += htmlMaker.loginFailMSG(errorString)
    return html, 200
    
    
# url routes from here on    
@app.route("/", methods=["GET"])
def loginPage():

    if (checkCookie()):
        # already logged in
        return redirect(url_for('events'))
        
    try:
        # return log in page
        file = open("pages/login.html", 'r')
        html = file.read()
        file.close()
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
        file = open("pages/loginFail.html", 'r')
        html = file.read()
        file.close()
        html += htmlMaker.loginFailMSG(errorString)
        return html, 200
    else:
        # create a cookie
        cookie = db.createCookie(userID[0])
        response = redirect(url_for('events'), 302)
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
    

@app.route("/events", methods=["GET"])
def listEvents():
    # list all events
    
    # must be logged in
    if (not checkCookie()):
        return isNotLoggedIn()

    try:
        events = db.getAllEvents()
        html = htmlMaker.listEvents(events)
    except:
        return '', 404
    return html, 200

@app.route("/event/<ID>", methods=["GET"])
def showEvent(eventID):
    
    # must be logged in
    if (not checkCookie()):
        return isNotLoggedIn()
    
    event = db.getEvent(eventID)
    
    
    
if __name__ == "__main__":
    app.run()    
    
    
    
    
    
    
    
    
    
    
    
    