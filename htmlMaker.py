
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
    # (id, title, date, location, items)
    
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
                        <p>By: {}</p>
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
            '''.format(event[1], username, event[3], event[4], event[5], event[2], event[0])
    
    return html


















