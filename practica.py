import sys
import urllib
import xml.sax 
import html 
import datetime

class Chghandler(xml.sax.ContentHandler): 
        stations = {}
        tag = ''
 
        def __init__(self,distance = 500, date = datetime.datetime.now() ):
            self.date = date
            self.distance = distance            
            
        def startElement(self, name, attrs):
            if name == 'street':
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
            if self.b == 1:
                Chghandler.tag = self.tag
            elif self.b == 2 :
                Chghandler.stations[Chghandler.tag] = self.slots
          
         



def cerca(string param):


def data(string param):


def distance(int param):



def main(argv):
    url = 'http://wservice.viabicing.cat/getstations.php?v=1'
    url2 = 'http://w10.bcn.es/APPS/asiasiacache/peticioXmlAsia?id=103'
    parser = xml.sax.make_parser()
    parser.setContentHandler(Chghandler())
    parser.parse(url)
    
    if sys.argv[1] == '--key':
        cerca(arg[2])
    elif sys.argv[1] == '--date':
        data(argv[2])
    elif sys.arg[1] == '--distance':
        distance(argv[2])