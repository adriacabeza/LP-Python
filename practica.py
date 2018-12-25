import sys
import urllib.request
import html 
import string
import datetime
import xml.etree.ElementTree as ET
from math import sin,cos,sqrt,atan2,radians

URL1= 'http://wservice.viabicing.cat/getstations.php?v=1'
URL2= 'http://w10.bcn.es/APPS/asiasiacache/peticioXmlAsia?id=103'

def load(key):
    value = None 
    if key in sys.argv:
        value = eval(sys.argv[sys.argv.index(key)+1])
    return value 

def distance(elem, station):
    #using haversine formula assuming that the Earth is a sphere
    longitud1, latitud1 = map(radians, [station['long'], station['lat']])
    longitud2, latitud2 = map(radians, [elem['long'], elem['lat']])
    dlon = longitud2 - longitud1
    dlat = latitud2 - latitud1
    a = sin(dlat / 2)**2 + cos(latitud1) * cos(latitud2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6373.0 * c
    return distance 


def parse_stations(xml):
    root = ET.fromstring(xml)
    stations = list()
    for station in root.iter('station'):
        information = {
            'id': station.find('id').text,
            'lat': station.find('lat').text,
            'long': station.find('long').text,
            'street': html.unescape(station.find('street').text),
            'bikes': station.find('bikes').text,
            'slots': station.find('slots').text
        }
        stations.append(information)

    return stations



def parse_parkings(xml):
    root = ET.fromstring(xml)
    llistaParkings = list()
    for parking in root.iter('acte'):
        information = {
            'id': parking.find('nom').text,
            # 'long': parking.find('geocodificacio')['y'].text,
            # 'address': html.unescape(parking.find('address').text)
        }
        # print(information)
        llistaParkings.append(information)

    return llistaParkings


# def crearmapa(stations):




def main():
    key = load('--key')
    date = load('--date')
    BICING = urllib.request.urlopen(URL1).read()
    PARKING = urllib.request.urlopen(URL2).read()
    stations = parse_stations(BICING)
    parkings = parse_parkings(PARKING)
    # print("STATIONS")
    print(stations)
    # print(PARKING)
    print("PARKINGS")
    # print(parkings)


    # acts = crearmapa(stations)

#per fer la pàgina 
    # body = ET.Element("body")
    # estil = open("style.txt", "r")
    # style = ET.SubElement(body, "style").text, = estil.read()

    # table = ET.SubElement(body,"table", width="100%")
   

    # tree = ET.ElementTree(body)
    # tree.write("output.html")
    

if __name__ == '__main__':
    main()

#  for act in acts:
#         create_title("Activitat",table)
#         add_act_data(act,table)
#         if act['bicing_slots']:
#             create_title("Aparcament bicicletes disponibles",table)
#             add_bicings(act['bicing_slots'],table,"Llocs disponibles",'slots')
#         if act['bicing_bikes']:
#             create_title("Bicicletes disponibles",table)
#             add_bicings(act['bicing_bikes'],table,"Bicis disponibles",'bikes')
#         if act['parkings']:
#             create_title("Aparcaments propers",table)
#             add_parkings(act['parkings'],table)
#         create_title("\n\n",table)
