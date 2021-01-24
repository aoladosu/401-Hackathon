
def loginFailMSG(errorString):
    
    string = '''
                        <div>
                            <p style="color:red;text-align:center;">{}</p>
                        </div>
                        
                    </body>
                </html>
                '''.format(errorString)
    return string


def listEvents(events):
    # event = (id, title, date, location, items)
    
    html = open('pages/eventsList.html','r').read()
    
    if (len(events) == 0):
        # no events
        html += '''</div>\n
                <h2><center>There are currently no events</center></h2>
                </body>
             </html>
            '''
        return html
        
    odd = True
    for event in events:
        # get info needed
        eid = event[0]
        title = event[1]
        date = event[2]
        location = event[3]
        items = event[4]
        
        # determine color
        if (odd):
            color = "gray"
        else:
            color = "white"
        
        # replace text
        html += '''<div class="row">
             <div class="col-lg-3" style="text-align:center;background-color:{};">
               <a href="/event/{}">{}</a>
             </div>
             <div class="col-lg-3" style="text-align:center;background-color:{};">
               {}
             </div>
             <div class="col-lg-3" style="text-align:center;background-color:{};">
               {}
             </div>
             <div class="col-lg-3" style="text-align:center;background-color:{};">
               {}
             </div>
           </div>
           \n\n
           '''.format(color, eid, title, color, date, color, location, color, items)
        
        odd = not odd
    
    # close html
    html +=''' </div>     
               </body>
             </html>
            '''
    
    return html

def showEvent(event, username, resultString):
    # display one event
    
    html = open("pages/header.html",'r').read()
    
    if (resultString != ""):
        html += '<p style="color:red">{}</p>\n'.format(resultString)
    
    html += '''
                    <div>
                        <h2>{}</h2>
                        <br>
                        <p>By: <a href="/profile/{}">{}</a></p>
                        <p>Date: {}</p>
                        <p>Location: {}</p>
                        <p>Items: {}</p>
                        <br>
                        <p><strong>Summary: </strong>{}</p>            
                    </div>   
                    
                    <div class="d-flex justify-content-start">
                        <form action="/pledge/{}" method="post">
                            <button type="submit" class="btn btn-outline-success">Pledge</button>
                        </form>
                    </div>
                    
                </body>       
            </html>
            '''.format(event[2], event[1], username, event[4], event[5], event[6], event[3], event[0])
    
    return html


def showProfile(username, events, pledges, isUser):
    # show user profile
    # event = (id, userID, title, date, location, items)
    # pledges = (id, title)
    
    html = open("pages/header.html",'r').read()
    
    html += "<h1>{}'s Profile</h1><br>".format(username)
    
    if (isUser):
        html += '''
                    <form action="/newEvent" method="get">
                        <button type="submit" class="btn btn-outline-success">Create New Event</button>
                    </form>
                    <br>
                '''
    
    # show current events
    html +='''
        <div>
            <h2>Events</h2>
        </div>
    
        <div class="container">
        
          <h3> 
          <div class="row">
            <div class="col-lg-3" style="text-align:center">
              <strong>Title</strong>
            </div>
            <div class="col-lg-3" style="text-align:center">
              <strong>Date</strong>
            </div>
            <div class="col-lg-3" style="text-align:center">
              <strong>Location</strong>
            </div>
            <div class="col-lg-3" style="text-align:center">
              <strong>Items</strong>
            </div>
          </div>
          </h3>
          '''        
    
    odd = True
    for event in events:
        # get info needed
        eid = event[0]
        title = event[2]
        date = event[4]
        location = event[5]
        items = event[6]
        
        # determine color
        if (odd):
            color = "gray"
        else:
            color = "white"
        
        # replace text
        html += '''<div class="row">
             <div class="col-lg-3" style="text-align:center;background-color:{};">
               <a href="/event/{}">{}</a>
             </div>
             <div class="col-lg-3" style="text-align:center;background-color:{};">
               {}
             </div>
             <div class="col-lg-3" style="text-align:center;background-color:{};">
               {}
             </div>
             <div class="col-lg-3" style="text-align:center;background-color:{};">
               {}
             </div>
           </div>
           \n\n
           '''.format(color, eid, title, color, date, color, location, color, items)
        odd = not odd
    
    html += "</div>\n" 
    if (len(events) == 0):
        html += '<h2><center>This user has no events</center></h2>'
    
    
    # pledges
    html +='''
        <br>
        <br>
        <div>
            <h2>Pledges</h2>
        </div>
    
        <div class="container">
        

          '''
    odd = True
    i = 0
    while (i < len(pledges)):
        # get info needed
        eid = pledges[i][0]
        title = pledges[i][1]
        
        try:
            eid2 = pledges[i+1][0]
            title2 = pledges[i+1][1]
        except:
            eid2 = None
            title2 = None
        
        # determine color
        if (odd):
            color = "gray"
        else:
            color = "white"
        
        # replace text
        if (eid2 != None):
            html += '''<div class="row">
                 <div class="col-lg-6" style="text-align:center;background-color:{};">
                   <a href="/event/{}">{}</a>
                 </div>
                 <div class="col-lg-6" style="text-align:center;background-color:{};">
                   <a href="/event/{}">{}</a>
                 </div>
               </div>
               \n\n
               '''.format(color, eid, title, color, eid2, title2)
           
        else:
            html += '''<div class="row">
                 <div class="col-lg-6" style="text-align:center;background-color:{};">
                   <a href="/event/{}">{}</a>
                 </div>
                 <div class="col-lg-6" style="text-align:center;background-color:{};">
                 </div>
               </div>
               \n\n
               '''.format(color, eid, title, color)
               
        odd = not odd
        i += 2
    
    html += "</div>\n" 
    if (len(pledges) == 0):
        html += '<h2><center>This user has made no pledges</center></h2>'
    
    html += "\n</body></html>\n"
    return html

def createEvent(resultString):
    # create new event for database
    html = open("pages/header.html",'r').read() + '<br><br>'
    
    if (resultString != ''):
        html += '<div style="color:red;"><center>{}</center></div><br>'.format(resultString)
    
    html += open("pages/newEventPartial.html",'r').read()
    return html













