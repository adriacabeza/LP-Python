# -*- coding: utf-8 -*-
import sys 
import urllib
import xml.sax 
import re 
import html

stations = {}
tag = ''

class Chghandler(xml.sax.ContentHandler): 
 
        def __init__(self):
            self.num = 5
            self.tag = ''
            self.slots  = 0
            self.b = 0
           
            
            
        def startElement(self, name, attrs):
            if(name == 'street'):
                self.b = 1
            elif name == 'slots':
                 self.b = 2
            else: 
                self.b = 0
               
        def characters(self, data):
            if self.b == 1:
                self.tag = data
            elif self.b == 2:
                self.slots = data
                
            
        def endElement(self, name):
            global tag
            if self.b == 1:
                tag = self.tag
            elif self.b == 2 :
                global stations
                stations[tag] = self.slots
          
         

url = 'https://wservice.viabicing.cat/v1/getstations.php?v=1'
parser = xml.sax.make_parser()
parser.setContentHandler(Chghandler())
parser.parse(url)
y = input("Vols fer-ho amb sax(0) o amb regex(1)?")
x = input('Quantes bicis necessites? ')

if int(y) == 0:
    for i in stations:
        if(int(stations[i]) >= int(x)):
            print("A la parada", html.unescape(i), " hi ha ", stations[i], " bicis disponibles.")
elif int(y)==1 :
    data = urllib.request.urlopen('http://wservice.viabicing.cat/getstations.php?v=1')
    xml = data.read()
    xml = xml.decode("utf-8")
    streets = re.findall(r'<street><!\[CDATA\[(.*)\]\]></street>',xml)
    numslots = re.findall(r'<slots>(.*)</slots>',xml)
    stations = {}
    for i in range(len(streets)):
        stations[streets[i]] = numslots[i]
    for i in stations:
        if(int(stations[i]) >= int(x)): 
            print("A la parada", html.unescape(i), "hi ha ", stations[i]," bicis disponibles." )
