import sys
import urllib.request
import html 
import string
from datetime import datetime
import xml.etree.ElementTree as ET
from math import sin,cos,sqrt,asin,radians

URL1= 'http://wservice.viabicing.cat/getstations.php?v=1'
URL2= 'http://w10.bcn.es/APPS/asiasiacache/peticioXmlAsia?id=103'
DATE_FORMAT = "%d/%m/%Y"

#CANVIARHO
def load(key):
    value = None 
    if key in sys.argv:
        value = eval(sys.argv[sys.argv.index(key)+1])
    return value 

#retorna la distancia entre elem i station
def distance(elem, station):
    longitud1, latitud1 = map(radians, [float(station['log']), float(station['lat'])])
    longitud2, latitud2 = map(radians, [float(elem['log']), float(elem['lat'])])
    dlon = longitud2 - longitud1
    dlat = latitud2 - latitud1
    a = sin(dlat / 2)**2 + cos(latitud1) * cos(latitud2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a)) 
    distance = 6373000.0 * c
    return distance 

#parseja totes les estacions de bicing 
def parse_stations(xml):
    root = ET.fromstring(xml)
    stations = list()
    for station in root.iter('station'):
        lat = station.find('lat')
        log = station.find('long')
        street = station.find('street')
        bikes= station.find('bikes')
        slots = station.find('slots')
        if any(map(lambda x: x is None, (lat,log,street,bikes,slots))):
            continue
        information = {
            'lat':lat.text,
            'log':log.text,
            'street': html.unescape(str(street.text)),
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
        # print(list(map(lambda x: x is None, (nom,districte,carrer, numero, data_init, data_fi))))
        if any(map(lambda x: x.text is None, (nom,districte,carrer, numero, data_init, data_fi))):
            continue
        information = {
            'nom': nom.text,
            'districte':districte.text,
            'log':log,
            'lat':lat,
            #'hora':hora,  PREGUNTAR AL PROFE PQ QUASI SEMPRE ES NULL
            'data_init':data_init.text,
            'data_fi':data_fi.text,
            'address': html.unescape(str(carrer.text)) + " "+ html.unescape(str(numero.text))
        }
        llistaActes.append(information)
    return llistaActes


#retorna els parkings de bicing que estan a una distancia menor del parametre
def getParkings(stations,elem, dist=300):
    llistaParking = list()
    for i in stations:
        distancia = distance(elem,i)
        if distancia <= dist :
                i['distance']= distancia
                llistaParking.append(i)
    return llistaParking

#retorna true si està entre les dues dates d'elem
def filterDate(date,elem):
    current = datetime.strptime(date, format)
    ini = datetime.strptime(elem['data_init'])
    fin = datetime.strptime(elem['data_fi'])
    return (ini < current and current < fin)

#retorna true si té alguns dels temes de key CANVIAR_HO
def filterEvent(key, elem):
    if isinstance(key, str):
        return key in elem['districte'] or key in elem['nom'] or key in elem['address']
    elif isinstance(key, list):
        filters = map(filterEvent(key,elem), key)
        return all(map(lambda f: f(elem), filters))
    elif isinstance(key, tuple):
        return any(map(lambda f: f(elem), map(filterEvent(key,elem), key)))
    return False

def afegeix_activitat(act,table):
    tr = ET.SubElement(table, "tr")
    th = ET.SubElement(tr, "th",align="left").text = "Nom"    
    th = ET.SubElement(tr, "th",align="left").text = "Adreça" 
    th = ET.SubElement(tr, "th",align="left").text = "Districte"        
    th = ET.SubElement(tr, "th",align="left").text = "Dia"    
    
    tr = ET.SubElement(table, "tr")
    th = ET.SubElement(tr, "td").text = act['nom']    
    th = ET.SubElement(tr, "td").text = act['address']   
    th = ET.SubElement(tr, "td").text = act['districte']  
    th = ET.SubElement(tr, "td").text = act['data_init']+'-'+act['data_fi']    
    # th = ET.SubElement(tr, "td").text = act['slots']   
    # th = ET.SubElement(tr, "td").text = act['bikes']

#ARREGLAR
def afegeix_bicing(llista,table):
    th = ET.SubElement(table, "th").text = "Nom"    
    for parking in parkings:
        for i in parking:
            tr = ET.SubElement(table, "tr")
            th = ET.SubElement(tr, "td").text = i['street']
    th = ET.SubElement(table, "th").text = "Nom"    
    for parking in parkings:
        for i in parking:
            tr = ET.SubElement(table, "tr")
            th = ET.SubElement(tr, "td").text = i['street']
#ARREGLAR
def afegirparkings(parkings,llista):
    for i in range(len(llista)):
        llista[i]['slots'] = sorted(parkings[i], key= lambda x: x['distance'])
        llista[i]['bikes'] = sorted(parkings[i],key=lambda x: x['distance'])


def main():
    #fer-ho amb argparse
    key = load('--key')
    date = load('--date')
    dist = load('--distance')

    #TEMA ACTES
    ACTES = urllib.request.urlopen(URL2).read()
    actes = parse_actes(ACTES)

    #TEMA BICING 
    BICING = urllib.request.urlopen(URL1).read()
    stations = parse_stations(BICING)

    
    #FILTRO LES ESTACIONS I EVENTS  
    if key:
        llista = list(filter(lambda x: filterEvent(key,x), actes))
    if date:
        llista = list(filter(lambda x: filterDate(date,x),actes))
    
    parkings = list(map(lambda x: getParkings(stations,x,dist), llista))
    #LO QUE SE TIENE QUE ARREGLAR
    afegirparkings(parkings, llista)
    print("LLISTA")
    for j in llista: print(j)
    
    #MAKING THE WEBSITE
    html = ET.Element('html')
    head = ET.SubElement(html,'head')
    style = ET.SubElement(html,"style").text = """
   @import "https://fonts.googleapis.com/css?family=Montserrat:300,400,700";

body {
  padding: 2em;
  font-family: Montserrat, sans-serif;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
  color: #444;
  background: #eee;
}

h1 {
  font-weight: normal;
  letter-spacing: -1px;
  color: #34495E;
}

.rwd-table {
  background: #34495E;
  color: #fff;
  border-radius: .4em;
}
.rwd-table tr {
  border-color: #46637f;buscats i le
}

.rwd-table th, .rwd-table td:before {
  color: #dd5;
}

    """
    title = ET.SubElement(head,'title')
    title.text = 'Taula amb els actes buscats i les estacions de bicing'
    body = ET.SubElement(html, 'body')
    titol = ET.SubElement(body,"h1", align= "center")
    titol.text = 'Taula amb els actes buscats i les estacions de bicing'
    table = ET.SubElement(body,"table", width="100%")
    for act in llista:
        afegeix_activitat(act,table)
        # afegeix_bicing(parkings,table)
    

    tree = ET.ElementTree(html)
    tree.write("output.html")

if __name__ == '__main__':
    main()


#COSES A ARREGLAR:
""" els parkings no els tinc ben organitzats, he de trobar una manera guay de printarho tot. A més he de canviar la manera amb la que faig argparse"""