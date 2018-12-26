import xml.etree.ElementTree as ET

xml = """<response>
<header module="QueryLlistaAG" operation="getLlistaAG" session=""/>
<body idioma="CA">
<resultat>
<info>
<num_resultats>4582</num_resultats>
<primer>1</primer>
<ultim>1500</ultim>
</info>
<actes>
<acte>
<id>99400607803</id>
<nom>
Exposició 'Creadors de consciència. 40 fotoperiodistes compromesos'
</nom>
<lloc_simple>
<id>92086011621</id>
<nom>Palau Robert - Centre d'Informació de Catalunya</nom>
<seccio>#</seccio>
<adreca_simple>
<carrer codi="148307">Pg Gràcia</carrer>
<numero davant="0" enter="107">107</numero>
<districte codi="02">Eixample</districte>
<codi_postal>08008</codi_postal>
<municipi codi="019">BARCELONA</municipi>
<coordenades>
<geocodificacio x="29832514" y="83274671"/>
<dibuix x="0" y="0"/>
</coordenades>
</adreca_simple>
</lloc_simple>
<data>
<data_inici>07/09/2018</data_inici>
<hora_inici/>
<data_fi>10/02/2019</data_fi>
<data_proper_acte>26/12/2018</data_proper_acte>
<data_aproximada/>
<data_relativa/>
</data>
<tipus_acte>P</tipus_acte>
<estat>C</estat>
<estat_cicle>V</estat_cicle>
<classificacions>
<nivell codi="0040001009">Exposicions</nivell>
<nivell codi="0040002009022">Fotografia</nivell>
<nivell codi="0040002023024">Nadal</nivell>
</classificacions>
</acte>
</actes>
</resultat>
</body>
</response>"""

root = ET.fromstring(xml)

y = root.find('body')
print(y.items())
print(y.get('idioma'))



for acte in root.iter('acte'):
    print(acte.find('nom').text)
    y = acte.find('lloc_simple')
    # print(y.getchildren())
    print('Adreça:')
    # print(y.find('adreca_simple').getchildren())
    print(y.find('adreca_simple').find('carrer').text)
    print(y.find('adreca_simple').find('coordenades').find('geocodificacio').items())
    z = acte.find('data')
    # print(z.getchildren())
    print(z.find('data_inici').text)
    print(z.find('hora_inici').text)
    print(z.find('data_fi').text)
 

