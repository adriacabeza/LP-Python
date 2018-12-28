import sys
import urllib.request
import html 
import string
import unicodedata
import argparse 
from datetime import datetime
import xml.etree.ElementTree as ET
from ast import literal_eval
from math import sin,cos,sqrt,asin,radians

URL1= 'http://wservice.viabicing.cat/getstations.php?v=1'
URL2= 'http://w10.bcn.es/APPS/asiasiacache/peticioXmlAsia?id=103'
DATE_FORMAT = "%d/%m/%Y"

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
        if any(map(lambda x: x.text is None, (nom,districte,carrer, numero, data_init, data_fi))):
            continue
        information = {
            'nom': nom.text,
            'districte':districte.text,
            'log':log,
            'lat':lat,
            'hora':"XX.XX" if hora.text is None else hora.text,
            'data_init':data_init.text,
            'data_fi':data_fi.text,
            'address': html.unescape(str(carrer.text)) + " "+ html.unescape(str(numero.text))
        }
        llistaActes.append(information)
    return llistaActes


#per a cada element de la llista he de ficar-li els seus slots i bikes
def afegir_parkings(llista, stations, dist):
    for l in llista: 
        for x in stations: 
            x['distance'] = distance(l,x)  
        #ara cada estació té a dintre la distancia
        st = list(filter(lambda x: x['distance'] <= dist, stations)) 
        st = sorted(st, key= lambda x: x['distance'])
        print(l['nom'])
        print(st)
        slots = list(filter(lambda x: int(x['slots']) > 0, st))
        bikes = list(filter(lambda x: int(x['bikes']) > 0, st))
        l['slots']=[item['street'] for item in slots[:5]]
        l['bikes']= [item['street'] for item in bikes[:5]] 

    return llista

#retorna true si està entre les dues dates d'elem
def filterDate(elem, date):
    current = datetime.strptime(date, DATE_FORMAT)
    ini = datetime.strptime(elem['data_init'],DATE_FORMAT)
    fin = datetime.strptime(elem['data_fi'],DATE_FORMAT)
    return (ini < current and current < fin)

#afegeix headers de la taula 
def afegeix_headers(table):
    tr = ET.SubElement(table, "tr")
    th = ET.SubElement(tr, "th",align="left").text = "Nom"    
    th = ET.SubElement(tr, "th",align="left").text = "Adreça" 
    th = ET.SubElement(tr, "th",align="left").text = "Districte"        
    th = ET.SubElement(tr, "th",align="left").text = "Dia"    
    th = ET.SubElement(tr, "th",align="left").text = "Hora"    
    th = ET.SubElement(tr, "th", align="left").text = "Estacions amb Slots"
    th = ET.SubElement(tr, "th", align="left").text = "Estacions amb Bicis"

 
#afegeix una activitat a la taula 
def afegeix_activitat(act,table):
    tr = ET.SubElement(table, "tr")
    th = ET.SubElement(tr, "td").text = act['nom']    
    th = ET.SubElement(tr, "td").text = act['address']   
    th = ET.SubElement(tr, "td").text = act['districte']  
    th = ET.SubElement(tr, "td").text = act['data_init']+'-'+act['data_fi']    
    th = ET.SubElement(tr, "td").text = act['hora']  
    text = str()
    first = True
    if(len(act['slots']) == 0): th = ET.SubElement(tr, "td").text = "No hi ha slots disponibles"
    else:
        for i in act['slots']:
            if first:  
                text = i
                first = False
            else : text = text + ", " + i
        th = ET.SubElement(tr, "td").text = text
        first = True
    text = str()
    if(len(act['bikes']) == 0): th = ET.SubElement(tr, "td").text = "No hi ha bicis disponibles"
    else:
        for i in act['bikes']:
            if first:  
                text = i
                first = False
            else: text = text + ", " + i
        th = ET.SubElement(tr, "td").text = text

#normalitza un text
def normalize(value):
    return unicodedata.normalize('NFC', value.casefold())

#filtra segons les paraules clau
def filterEvent(key, elem):
    if isinstance(key, str):
        return normalize(key) in normalize(elem['districte']) or normalize(key) in normalize(elem['nom']) or normalize(key) in normalize(elem['address'])
    elif isinstance(key, list):
        return all(map(lambda x: filterEvent(x,elem), key))
    elif isinstance(key, tuple):
        return any(map(lambda x: filterEvent(x,elem), key))
    return False

#TODO: mirar si fer-ho amb l'interval de dates o amb data inici ja està bé
def dif_dates(elem, date):
    return abs((datetime.strptime(elem['data_init'],DATE_FORMAT)- datetime.strptime(date, DATE_FORMAT)).days)

#crea la taula html amb els actes
def make_html(llista):
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
th,td{
    text-align:center;
}

table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
}
    """
    title = ET.SubElement(head,'title')
    title.text = 'Taula amb els actes buscats i les estacions de bicing'
    body = ET.SubElement(html, 'body')
    titol = ET.SubElement(body,"h1", align= "center")
    titol.text = 'Taula amb els actes buscats i les estacions de bicing'
    table = ET.SubElement(body,"table", width="100%")
    afegeix_headers(table)
    for act in llista:
        afegeix_activitat(act,table)
        
    tree = ET.ElementTree(html)
    tree.write("output.html")

    
#modifica una data"%d/%m/%Y" per a avaluar-la
def eval_date(date):
    
    
    return 



#carrega un xml d'un url
def carregarXML(url):
    return urllib.request.urlopen(url).read()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--distance", required= False, help = "afegir la distancia")
    ap.add_argument("--key", required= True, help="afegir les paraules clau")
    ap.add_argument("--date", required= False, help = "afegir el dia amb el format DIA/MES/ANY")
    args = vars(ap.parse_args())
    key = None if args['key'] == None else literal_eval(args['key'])
    date = datetime.today().strftime(DATE_FORMAT) if args['date'] == None  else literal_eval(eval_date(args['date']))
    dist = 300 if args['distance'] == None else literal_eval(args['distance'])
    
    #TEMA ACTES
    ACTES = carregarXML(URL2)
    actes = parse_actes(ACTES)

    #TEMA BICING 
    BICING = carregarXML(URL1)
    stations = parse_stations(BICING)
    
    #FILTRO LES ESTACIONS I EVENTS  
    if key:
        llista = list(filter(lambda x: filterEvent(key,x), actes))
    if date:
        llista = list(filter(lambda x: filterDate(x,date),llista))

    #ordenar segons la proximitat de data inici
    llista = sorted(llista, key = lambda x: dif_dates(x,date))

    #filtrar per cada activitat les estacions a menys distance
    llista = afegir_parkings(llista,stations,dist)
  
    make_html(llista)



if __name__ == '__main__':
    main()


#COSES A ARREGLAR:
""" els parkings no els tinc ben organitzats, he de trobar una manera guay de printarho tot. A més he de canviar la manera amb la que faig argparse"""