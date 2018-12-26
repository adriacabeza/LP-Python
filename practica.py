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
    longitud1, latitud1 = map(radians, [station['log'], station['lat']])
    longitud2, latitud2 = map(radians, [elem['log'], elem['lat']])
    dlon = longitud2 - longitud1
    dlat = latitud2 - latitud1
    a = sin(dlat / 2)**2 + cos(latitud1) * cos(latitud2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6373.0 * c
    return distance 

#parseja totes les estacions de bicing 
#PENSAR SI NECESSITO EL ID 
def parse_stations(xml):
    root = ET.fromstring(xml)
    stations = list()
    for station in root.iter('station'):
        id = station.find('id')
        lat = station.find('lat')
        log = station.find('log')
        street = station.find('street')
        bikes= station.find('bikes')
        slots = station.find('slots')
        if any(map(lambda x: x is None, (id,lat,log,street,bikes,slots))):
            continue
        information = {
            'id': id.text,
            'lat':lat.text,
            'log':log.text,
            'street':html.unescape(street.text),
            'bikes': bikes.text,
            'slots': slots.text
        }
        stations.append(information)

    return stations


#parseja tots els actes 
def parse_actes(xml):
    root = ET.fromstring(xml)
    llistaActes = list()
    for acte in root.iter('acte'):
        nom = acte.find('nom')
       
        dates = acte.find('data')
        data_init = dates.find('data_inici')
        data_fi = dates.find('data_fi')
        hora = dates.find('hora_inici') 

        lloc = acte.find('lloc_simple').find('adreca_simple')
        districte = lloc.find('districte')
        carrer = lloc.find('carrer')
        numero = lloc.find('numero')
        coordenades = lloc.find('coordenades').find('geocodificacio')
        lat = coordenades.get('x')
        log = coordenades.get('y')

        if any(map(lambda x: x is None, (nom,districte,carrer, numero, data_init, data_fi))):
            continue
        information = {
            'nom': nom,
            'districte':districte.text,
            'log':log,
            'lat':lat,
            # 'hora':hora, 
            'data_init':data_init.text,
            'data_fi':data_fi.text,
            'address': carrer.text # + numero.text
        }
        llistaActes.append(information)
    
    return llistaActes


#retorna els parkings de bicing que estan a una distancia menor del parametre
def getParkings(stations,elem, distance=300):
    llistaParking = list()
    for i in stations:
        if distance(elem,i) <= distance :
                llistaParking.append(i)
    return llistaParking



def main():
    key = load('--key')
    date = load('--date')
    distance = load('--distance')
    #TEMA ACTES
    ACTES = urllib.request.urlopen(URL2).read()
    actes = parse_actes(ACTES)
    print(actes)

    #TEMA BICING 
    BICING = urllib.request.urlopen(URL1).read()
    stations = parse_stations(BICING)


    
    # getParkings(stations, elem, distance)
    # print("STATIONS")
    # print(stations)
    
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
