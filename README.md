# Exercicis de Python
### Funcions amb llistes
- Nombre d'elements diferents d'una llista
```python
def elements_diferents(llista):
    print("Té", len(set(llista)), "elements diferents.")
```  
- Màxim d'una llista
```python    
def max_llista(llista):
    print("El seu valor màxim és", reduce(lambda x, y: x if x>y else y, llista))
```
- Mitjana d'una llista
```python
def mitjana(llista):
    print("El valor de la mitjana és", reduce(lambda x, y: x+y,llista)/ len(llista))
```
- Aplanar llistes
```python
def flatten(llista):
    if isinstance(llista,list):
        l = []
        for x in llista: l+= flatten(x)
        return l
    else: return [llista]
```

- Inserir un element en una llista ordenada
```python
def insert(llista, elem):
    print("Anem a inserir", elem, "a la llista")
    if llista[-1] < elem:
        llista.insert(len(llista), elem)
    for i in range(len(llista)):
        if llista[i] < elem:
            continue
        else :
            llista.insert(i, elem)
            break
    print("Resultat de l'inserció", llista)
```
- Separar en parells i imparells una llista
```python
def separallista(llista):
    parell = [i for i in llista if i%2==0]
    imparell = [i for i in llista if i%2!=0]
    print("Imparells", imparell)
    print("Parells", parell)
    return (imparell,parell)
```
- Llistar els divisors primers d'un nombre
    return (imparell,parell)
```python
def isPrime(x):
    if x<=1: return False
    if x == 2 or x == 3: return True
    for i in range(2, int(math.sqrt(x))+1):
        if x%i == 0: return False
    return True

def primeDivisors(n):
    if isPrime(n): return n
    else:
        divisors = [x for x in range(2,n) if n%x ==0]
        divisorsPrimers = [x for x in divisors if isPrime(x)]
        return divisorsPrimers
```
### Funcions d'ordre superior
- Producte d'una llista
```python
def product(llista):
   return reduce(lambda x,y: x*y,llista)
```
- Nombre de vegades que hi ha un elements en una llista
```python
def howmanytimes(llista, elem):
    return llista.count(elem)
```
- Invertir una llista amb reduce 

- Fer el producte dels números pars d'una llista
```python
def productpar(llista):
    return reduce(lambda x,y: x*y if y%2 == 0 else x,llista)
```
- 7.3.1 Només ZipWith
- 7.4.4 Factors d'un nombre 
- 7.4.5 Ternes pitagòriques

# Lab 2
- Problemes de classes
- Problema del Bicing 
```python 
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

```
       
