# Python 3 server example
'''
Dynamic ports, also known as private or ephemeral ports, are 
temporary communication endpoints (ports) used by client 
applications to initiate network connections with servers, 
allocated by the operating system from a predefined range 
(49152 to 65535) and released after the connection is closed. 
'''

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
from urllib.parse import urlparse
import sqlite3
from individualStats import individualStatsFig

conn = sqlite3.connect('../data/fighters.sqlite')
cur = conn.cursor()

summaryStats = open('summaryStats.json','r')
summaryStats = json.load(summaryStats)

# summaryStatsImage = open('summaryStats.png')

hostName = "localhost"
serverPort = 50000

class MyServer(BaseHTTPRequestHandler):

    # def __new__(cls, *args, **kwargs):
    #     return super().__new__(cls)
    # def __init__(self, cur):
    #     self.cur=cur
    
    def do_GET(self):
        self.send_response(200)
        
        #self.wfile.write(bytes(json.dumps([{"firstName":"Khabib","lastName":"Nurmagomedov","matches":29,"wins":29,"losses":0,"knockoutWins":8,"knockoutLosses":0,"submissionWins":11,"submissionLosses":0,"decisionWins":10,"decisionLosses":0},{"firstName":"Justin","lastName":"Gaethje","matches":30,"wins":25,"losses":5,"knockoutWins":20,"knockoutLosses":3,"submissionWins":1,"submissionLosses":2,"decisionWins":4,"decisionLosses":0},{"firstName":"Dustin","lastName":"Poirier","matches":40,"wins":30,"losses":9,"knockoutWins":15,"knockoutLosses":3,"submissionWins":8,"submissionLosses":4,"decisionWins":7,"decisionLosses":2},{"firstName":"Conor","lastName":"McGregor","matches":28,"wins":22,"losses":6,"knockoutWins":19,"knockoutLosses":2,"submissionWins":1,"submissionLosses":4,"decisionWins":2,"decisionLosses":0},{"firstName":"Al","lastName":"Iaquinta","matches":22,"wins":14,"losses":7,"knockoutWins":7,"knockoutLosses":1,"submissionWins":1,"submissionLosses":3,"decisionWins":6,"decisionLosses":3},{"firstName":"Edson","lastName":"Barboza","matches":36,"wins":24,"losses":12,"knockoutWins":14,"knockoutLosses":4,"submissionWins":1,"submissionLosses":2,"decisionWins":9,"decisionLosses":6},{"firstName":"Michael","lastName":"Johnson","matches":42,"wins":23,"losses":19,"knockoutWins":10,"knockoutLosses":3,"submissionWins":2,"submissionLosses":9,"decisionWins":11,"decisionLosses":7},{"firstName":"Darrell","lastName":"Horcher","matches":21,"wins":14,"losses":7,"knockoutWins":7,"knockoutLosses":3,"submissionWins":1,"submissionLosses":1,"decisionWins":6,"decisionLosses":3},{"firstName":"Rafael","lastName":"dos","matches":49,"wins":32,"losses":17,"knockoutWins":5,"knockoutLosses":5,"submissionWins":11,"submissionLosses":0,"decisionWins":16,"decisionLosses":12},{"firstName":"Pat","lastName":"Healy","matches":59,"wins":34,"losses":24,"knockoutWins":7,"knockoutLosses":7,"submissionWins":15,"submissionLosses":6,"decisionWins":12,"decisionLosses":11},{"firstName":"Abel","lastName":"Trujillo","matches":24,"wins":15,"losses":8,"knockoutWins":5,"knockoutLosses":1,"submissionWins":4,"submissionLosses":4,"decisionWins":5,"decisionLosses":3},{"firstName":"Thiago","lastName":"Tavares","matches":36,"wins":24,"losses":11,"knockoutWins":4,"knockoutLosses":8,"submissionWins":15,"submissionLosses":0,"decisionWins":5,"decisionLosses":3},{"firstName":"Gleison","lastName":"Tibau","matches":58,"wins":39,"losses":19,"knockoutWins":4,"knockoutLosses":5,"submissionWins":15,"submissionLosses":2,"decisionWins":20,"decisionLosses":11},{"firstName":"Kamal","lastName":"Shalorus","matches":16,"wins":9,"losses":5,"knockoutWins":4,"knockoutLosses":1,"submissionWins":1,"submissionLosses":3,"decisionWins":4,"decisionLosses":1},{"firstName":"Ali","lastName":"Bagov","matches":46,"wins":34,"losses":11,"knockoutWins":3,"knockoutLosses":7,"submissionWins":24,"submissionLosses":1,"decisionWins":7,"decisionLosses":3},{"firstName":"Shahbulat","lastName":"Shamhalaev","matches":16,"wins":12,"losses":3,"knockoutWins":8,"knockoutLosses":0,"submissionWins":1,"submissionLosses":3,"decisionWins":3,"decisionLosses":0},{"firstName":"Max","lastName":"Holloway","matches":34,"wins":26,"losses":8,"knockoutWins":12,"knockoutLosses":1,"submissionWins":2,"submissionLosses":1,"decisionWins":12,"decisionLosses":6},{"firstName":"Rafael","lastName":"Fiziev","matches":15,"wins":12,"losses":3,"knockoutWins":8,"knockoutLosses":2,"submissionWins":1,"submissionLosses":0,"decisionWins":3,"decisionLosses":1},{"firstName":"Charles","lastName":"Oliveira","matches":46,"wins":35,"losses":10,"knockoutWins":10,"knockoutLosses":4,"submissionWins":21,"submissionLosses":4,"decisionWins":4,"decisionLosses":2},{"firstName":"Michael","lastName":"Chandler","matches":32,"wins":23,"losses":9,"knockoutWins":11,"knockoutLosses":4,"submissionWins":7,"submissionLosses":1,"decisionWins":5,"decisionLosses":4},{"firstName":"Tony","lastName":"Ferguson","matches":36,"wins":25,"losses":11,"knockoutWins":12,"knockoutLosses":2,"submissionWins":8,"submissionLosses":4,"decisionWins":5,"decisionLosses":5},{"firstName":"Donald","lastName":"Cerrone","matches":55,"wins":36,"losses":17,"knockoutWins":10,"knockoutLosses":8,"submissionWins":17,"submissionLosses":2,"decisionWins":9,"decisionLosses":7},{"firstName":"James","lastName":"Vick","matches":19,"wins":13,"losses":6,"knockoutWins":3,"knockoutLosses":5,"submissionWins":5,"submissionLosses":0,"decisionWins":5,"decisionLosses":1},{"firstName":"Eddie","lastName":"Alvarez","matches":40,"wins":30,"losses":8,"knockoutWins":17,"knockoutLosses":4,"submissionWins":7,"submissionLosses":2,"decisionWins":6,"decisionLosses":2},{"firstName":"Luiz","lastName":"Firmino","matches":30,"wins":20,"losses":10,"knockoutWins":2,"knockoutLosses":1,"submissionWins":7,"submissionLosses":2,"decisionWins":11,"decisionLosses":7},{"firstName":"Brian","lastName":"Foster","matches":43,"wins":30,"losses":13,"knockoutWins":15,"knockoutLosses":3,"submissionWins":14,"submissionLosses":9,"decisionWins":1,"decisionLosses":0},{"firstName":"Luis","lastName":"Palomino","matches":43,"wins":26,"losses":17,"knockoutWins":15,"knockoutLosses":5,"submissionWins":2,"submissionLosses":3,"decisionWins":9,"decisionLosses":9},{"firstName":"Melvin","lastName":"Guillard","matches":59,"wins":32,"losses":22,"knockoutWins":21,"knockoutLosses":6,"submissionWins":2,"submissionLosses":9,"decisionWins":9,"decisionLosses":7},{"firstName":"Nick","lastName":"Newell","matches":20,"wins":16,"losses":4,"knockoutWins":2,"knockoutLosses":1,"submissionWins":11,"submissionLosses":0,"decisionWins":3,"decisionLosses":3},{"firstName":"Dan","lastName":"Lauzon","matches":23,"wins":17,"losses":6,"knockoutWins":9,"knockoutLosses":3,"submissionWins":7,"submissionLosses":2,"decisionWins":1,"decisionLosses":1},{"firstName":"Gesias","lastName":"Cavalcante","matches":37,"wins":22,"losses":12,"knockoutWins":7,"knockoutLosses":6,"submissionWins":10,"submissionLosses":1,"decisionWins":5,"decisionLosses":5},{"firstName":"Drew","lastName":"Fickett","matches":65,"wins":43,"losses":22,"knockoutWins":3,"knockoutLosses":12,"submissionWins":32,"submissionLosses":5,"decisionWins":8,"decisionLosses":5},{"firstName":"Kevin","lastName":"Croom","matches":38,"wins":22,"losses":15,"knockoutWins":6,"knockoutLosses":5,"submissionWins":10,"submissionLosses":4,"decisionWins":6,"decisionLosses":6},{"firstName":"Islam","lastName":"Makhachev","matches":28,"wins":27,"losses":1,"knockoutWins":5,"knockoutLosses":1,"submissionWins":13,"submissionLosses":0,"decisionWins":9,"decisionLosses":0},{"firstName":"Benoît","lastName":"Saint","matches":17,"wins":13,"losses":3,"knockoutWins":4,"knockoutLosses":2,"submissionWins":9,"submissionLosses":0,"decisionWins":0,"decisionLosses":1},{"firstName":"Dan","lastName":"Hooker","matches":36,"wins":24,"losses":12,"knockoutWins":11,"knockoutLosses":3,"submissionWins":7,"submissionLosses":3,"decisionWins":6,"decisionLosses":6},{"firstName":"Anthony","lastName":"Pettis","matches":39,"wins":25,"losses":14,"knockoutWins":11,"knockoutLosses":2,"submissionWins":8,"submissionLosses":3,"decisionWins":6,"decisionLosses":9},{"firstName":"Jim","lastName":"Miller","matches":57,"wins":38,"losses":18,"knockoutWins":7,"knockoutLosses":2,"submissionWins":21,"submissionLosses":3,"decisionWins":10,"decisionLosses":13},{"firstName":"Joseph","lastName":"Duffy","matches":21,"wins":16,"losses":5,"knockoutWins":4,"knockoutLosses":1,"submissionWins":10,"submissionLosses":2,"decisionWins":2,"decisionLosses":2},{"firstName":"Yancy","lastName":"Medeiros","matches":27,"wins":16,"losses":9,"knockoutWins":8,"knockoutLosses":4,"submissionWins":4,"submissionLosses":1,"decisionWins":4,"decisionLosses":4}]),'utf-8'))
        cli_query = urlparse(self.path)
        print(f'\n url query: {cli_query.query}')

        if cli_query.query=='summaryStats':
            self.send_header("Content-type", "text/plain")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            print('summaryStats request recived from front')
            numFights = str(summaryStats['numFights'])
            numFighters = str(summaryStats['numFighters'])
            
            self.wfile.write(bytes(numFights, 'utf-8'))
            self.wfile.write(bytes('/','utf-8'))
            self.wfile.write(bytes(numFighters, 'utf-8'))
            # get length of visitied_links from sqlite

        elif cli_query.query=='summaryStatsImage':
            self.send_header("Content-type", "image/jpeg")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            with open ('summaryStats.png','rb') as I:
                imageData=I.read()
            self.wfile.write(imageData)
            
        elif 'fiftyFighters' in cli_query.query:
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            # for single requests
            print('query is fiftyFighters')
            # large json file:
            allFighters = self.get_fighter_data()
            self.wfile.write(bytes(json.dumps(allFighters),'utf-8'))

            print(allFighters[0])




class dataHandler(MyServer):
    
    def get_length(self):
        cur.execute('SELECT COUNT(*) FROM visited_links')
        lngth = str(cur.fetchone()[0])
        return lngth

    # is it better to do many requests? or just one request with a huge json file?

    # one large json:
    def get_fighter_data(self):
        cur.execute('SELECT * FROM profesional_record_data LIMIT 50')
        all = cur.fetchall()
        return all

    


if __name__ == "__main__":  
    
    
    webServer = HTTPServer((hostName, serverPort), dataHandler)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    
    cur.close()

    webServer.server_close()
    print("Server stopped.")