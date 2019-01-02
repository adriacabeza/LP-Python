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
URL3 = 'http://w10.bcn.es/APPS/asiasiacache/peticioXmlAsia?id=199'
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
def parseStations(xml):
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
def parseActes(xml):
    root = ET.fromstring(xml)
    llistaActes = list()
    for acte in root.iter('acte'):
        nom = acte.find('nom')
        dates = acte.find('data')
        data_init = dates.find('data_inici')
        data_fi = dates.find('data_fi')
        hora = dates.find('hora_inici') 
        lloc = acte.find('lloc_simple')
        place = lloc.find('nom')
        lloc = lloc.find('adreca_simple')
        districte = lloc.find('districte')
        carrer = lloc.find('carrer')
        numero = lloc.find('numero')
        coordenades = lloc.find('coordenades').find('geocodificacio')
        lat = coordenades.get('x')
        log = coordenades.get('y')
        if any(map(lambda x: x.text is None, (nom,districte,carrer,place, numero, data_init, data_fi))):
            continue
        information = {
            'nom': nom.text,
            'districte':districte.text,
            'log':log,
            'lloc': place.text,
            'lat':lat,
            'hora':"XX.XX" if hora.text is None else hora.text,
            'data_init':data_init.text,
            'data_fi':data_fi.text,
            'address': html.unescape(str(carrer.text)) + " "+ html.unescape(str(numero.text))
        }
        llistaActes.append(information)
    return llistaActes

#parseja tots els actes d'un dia donat
def parseDaily(xml):
    root = ET.fromstring(xml)
    llistaActes = list()
    for acte in root.iter('acte'):
        nom = acte.find('nom')
        lloc = acte.find('lloc_simple')
        place = lloc.find('nom')
        lloc = lloc.find('adreca_simple')
        barri = lloc.find('barri')
        carrer = lloc.find('carrer')
        numero = lloc.find('numero')
        coordenades = lloc.find('coordenades').find('googleMaps')
        lat = coordenades.get('lat')
        log = coordenades.get('lon')
        if any(map(lambda x: x.text is None, (nom,barri,place,carrer, numero))):
            continue
        information = {
            'nom': nom.text,
            'barri':barri.text,
            'lloc': place.text,
            'log':log,
            'lat':lat,
            'address': carrer.text + " "+ numero.text
        }
        llistaActes.append(information)
    return llistaActes

#per a cada element de la llista he de ficar-li els seus slots i bikes
def afegirParkings(llista, stations, dist):
    for l in llista: 
        for x in stations: 
            x['distance'] = distance(l,x)  
        #ara cada estació té a dintre la distancia
        st = list(filter(lambda x: x['distance'] <= dist, stations)) 
        st = sorted(st, key= lambda x: x['distance'])
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
    return (ini <= current or current <= fin)

#afegeix headers de la taula 
def afegeixHeaders(table, bicing):
    tr = ET.SubElement(table, "tr")
    th = ET.SubElement(tr, "th",align="left").text = "Nom"  
    th = ET.SubElement(tr, "th",align="left").text = "Lloc"     
    th = ET.SubElement(tr, "th",align="left").text = "Adreça"   
    if bicing:     
        th = ET.SubElement(tr, "th",align="left").text = "Barri" 
        th = ET.SubElement(tr, "th", align="left").text = "Estacions amb Slots"
        th = ET.SubElement(tr, "th", align="left").text = "Estacions amb Bicis"
    else: 
        th = ET.SubElement(tr, "th",align="left").text = "Districte" 
        th = ET.SubElement(tr, "th",align="left").text = "Dia"    
        th = ET.SubElement(tr, "th",align="left").text = "Hora"    
 
#afegeix una activitat a la taula 
def afegeixActivitat(act,table, bicing):
    tr = ET.SubElement(table, "tr")
    th = ET.SubElement(tr, "td").text = act['nom']   
    th = ET.SubElement(tr, "td").text = act['lloc']   
    th = ET.SubElement(tr, "td").text = act['address']   
    if bicing: 
        th = ET.SubElement(tr, "td").text = act['barri']  
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

    else :
        th = ET.SubElement(tr, "td").text = act['districte']  
        th = ET.SubElement(tr, "td").text = act['data_init']+'-'+act['data_fi']    
        th = ET.SubElement(tr, "td").text = act['hora']  



   
#normalitza un text
def normalize(value):
    return ''.join(x for x in unicodedata.normalize('NFKD', value) if x in string.ascii_letters).lower()

#filtra segons les paraules clau
def filterEvent(key, elem, bicing):
    if isinstance(key, str):
        b = normalize(key) in normalize(elem['barri']) if bicing else normalize(key) in normalize(elem['districte'])
        return b or normalize(key) in normalize(elem['nom']) or normalize(key) in normalize(elem['address'])
    elif isinstance(key, list):
        return all(map(lambda x: filterEvent(x,elem, bicing), key))
    elif isinstance(key, tuple):
        return any(map(lambda x: filterEvent(x,elem, bicing), key))
    return False

#TODO: mirar si fer-ho amb l'interval de dates o amb data inici ja està bé
def dif_dates(elem, date):
    return abs((datetime.strptime(elem['data_init'],DATE_FORMAT)- datetime.strptime(date, DATE_FORMAT)).days)

#crea la taula html amb els actes
def make_html(llista, bicing):
    html = ET.Element('html')
    head = ET.SubElement(html,'head')
    ET.SubElement(html,"style").text = """
   @import "https://fonts.googleapis.com/css?family=Montserrat:300,400,700";

body {
  padding: 2em;
  min-width: 434px;
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
    title.text = 'Taula amb els actes buscats i les estacions de bicing' if bicing else 'Taula amb els actes buscats'
    body = ET.SubElement(html, 'body')
    titol = ET.SubElement(body,"h1", align= "center")
    titol.text = 'Taula amb els actes buscats i les estacions de bicing' if bicing else 'Taula amb els actes buscats'
    table = ET.SubElement(body,"table", width="100%")
    afegeixHeaders(table, bicing)
    for act in llista:
        afegeixActivitat(act,table, bicing)

    tree = ET.ElementTree(html)
    tree.write("output.html")



#modifica una data %d/%m/%Y per a avaluar-la afegint ""
def evalDate(date):
    date.insert(0,'\"')
    date.insert(len(date),'\"')
    return ''.join(date)


#carrega un xml d'un url
def carregarXML(url):
    return urllib.request.urlopen(url).read()

def main():
    bicing = False 
    ap = argparse.ArgumentParser()
    ap.add_argument("--distance", required= False, help = "afegir la distancia")
    ap.add_argument("--key", required= True, help="afegir les paraules clau")
    ap.add_argument("--date", required= False, help = "afegir el dia amb el format DIA/MES/ANY")
    args = vars(ap.parse_args())
    key = None if args['key'] == None else literal_eval(args['key'])
    if args['date'] == None :
        date = datetime.today().strftime(DATE_FORMAT)
        bicing = True
        ACTES = carregarXML(URL3)
        actes = parseDaily(ACTES)
    else: 
        date = literal_eval(evalDate(list(args['date'])))
        ACTES = carregarXML(URL2)
        actes = parseActes(ACTES)
    dist = 300 if args['distance'] == None else literal_eval(args['distance'])
    
    if bicing:  
        #TEMA BICING 
        BICING = carregarXML(URL1)
        stations = parseStations(BICING)
    
    #FILTRO LES ESTACIONS I EVENTS  
    if key:
        llista = list(filter(lambda x: filterEvent(key,x, bicing), actes))
    if bicing: 
        #filtrar per cada activitat les estacions a menys distance
        llista = afegirParkings(llista,stations,dist)
    else:
        llista = list(filter(lambda x: filterDate(x,date),llista))
         #ordenar segons la proximitat de data inici
        llista = sorted(llista, key = lambda x: dif_dates(x,date))
        
    make_html(llista, bicing)



if __name__ == '__main__':
    main()
