from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import re

# Get all of your session stuff set up so we can get and store info from the database. 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem
# connect to the database
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):
    def restaurantListHtml(self):
        restaurants = session.query(Restaurant).all()
        restListHtml = ""
        for restaurant in restaurants:
            restListHtml += "<h1>" + restaurant.name + "</h1>"
            restListHtml += ('''<a href="http://localhost:8080/restaurants/%s/edit">Edit </a>''' % restaurant.id)
            restListHtml += "</br>"
            restListHtml += ('''<a href="http://localhost:8080/restaurants/%s/delete">Delete </a>''' % restaurant.id)
        return restListHtml

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += '''<a href="http://localhost:8080/restaurants/new"><h2>Create a new Form</h2></a>'''
                output += self.restaurantListHtml()
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a new restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>Create a new Form</h2><input name="new_restaurant" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/edit"):
                restaurantId = self.path.split('/')[2]                
                editRest = session.query(Restaurant).filter_by(id = restaurantId).one()
                if editRest != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>Edit - "
                    output += editRest.name
                    output == "</h1>"
                    output += '''<form method='POST' enctype='multipart/form-data' action='%s'>''' % self.path
                    output += '''<input name="edit_restaurant" type="text" placeholder = '%s'><input type="submit" value="Rename"> </form>''' % editRest.name
                    output += "</body></html>"
                    self.wfile.write(output)
                    print output
                return

            if self.path.endswith("/delete"):
                restaurantId = self.path.split('/')[2]                
                delRest = session.query(Restaurant).filter_by(id = restaurantId).one()
                if delRest != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += '<h1>Are you sure you want to delete "'
                    output += delRest.name
                    output += '''" </h1>'''
                    output += '</br>'
                    output += '''<form method='POST' enctype='multipart/form-data' action='%s'>''' % self.path
                    output += '''<input type="submit" value="Delete"> </form>'''
                    output += "</body></html>"
                    self.wfile.write(output)
                    print output
                return

            # if self.path.endswith("/hello"):
            #     self.send_response(200)
            #     self.send_header('Content-type', 'text/html')
            #     self.end_headers()
            #     output = ""
            #     output += "<html><body>"
            #     output += "<h1>Hello!</h1>"
            #     output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            #     output += "</body></html>"
            #     self.wfile.write(output)
            #     print output
            #     return

            # if self.path.endswith("/hola"):
            #     self.send_response(200)
            #     self.send_header('Content-type', 'text/html')
            #     self.end_headers()
            #     output = ""
            #     output += "<html><body>"
            #     output += "<h1>&#161 Hola !</h1>"
            #     output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            #     output += "</body></html>"
            #     self.wfile.write(output)
            #     print output
            #     return


        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('new_restaurant')

                newRest = Restaurant(name = messagecontent[0])
                session.add(newRest)
                session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

            elif self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('edit_restaurant')
                restaurantId = self.path.split("/")[2]
                existingRest = session.query(Restaurant).filter_by(id = restaurantId).one()
                if existingRest != [] :
                    existingRest.name = messagecontent[0]
                    session.add(existingRest)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            elif self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                restaurantId = self.path.split("/")[2]
                print restaurantId
                deleteRest = session.query(Restaurant).filter_by(id = restaurantId).one()
                if deleteRest != [] :
                    session.delete(deleteRest)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            # else :
            #     self.send_response(301)
            #     self.send_header('Content-type', 'text/html')
            #     self.end_headers()
            #     ctype, pdict = cgi.parse_header(
            #         self.headers.getheader('content-type'))
            #     if ctype == 'multipart/form-data':
            #         fields = cgi.parse_multipart(self.rfile, pdict)
            #         messagecontent = fields.get('message')

            #     output = ""
            #     output += "<html><body>"
            #     output += " <h2> Okay, how about this: </h2>"
            #     output += "<h1> %s </h1>" % messagecontent[0]
            #     output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            #     output += "</body></html>"
            #     self.wfile.write(output)
            #     print output
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()