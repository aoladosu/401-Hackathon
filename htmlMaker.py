
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



          # <div class="row">
          #   <div class="col-lg-3" style="text-align:center;background-color:gray;">
          #     <a href="hello">Clothes Drive</a>
          #   </div>
          #   <div class="col-lg-3" style="text-align:center;background-color:gray;">
          #     11-02-16
          #   </div>
          #   <div class="col-lg-3" style="text-align:center;background-color:gray;">
          #     Edmonton
          #   </div>
          #   <div class="col-lg-3" style="text-align:center;background-color:gray;">
          #     Clothes, shirts, socks
          #   </div>
          # </div>
          
          # <div class="row">
          #   <div class="col-lg-3" style="text-align:center;background-color:white;">
          #     <a href="hello">Clothes Drive</a>
          #   </div>
          #   <div class="col-lg-2" style="text-align:center;background-color:white;">
          #     11-02-16
          #   </div>
          #   <div class="col-lg-3" style="text-align:center;background-color:white;">
          #     Edmonton
          #   </div>
          #   <div class="col-lg-3" style="text-align:center;background-color:white;">
          #     Clothes, shirts, socks
          #   </div>
          # </div>