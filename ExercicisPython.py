from functools import reduce
import math

#funcions amb llistes

def elements_diferents(llista):
    print("Té", len(set(llista)), "elements diferents.")
    
def max_llista(llista):
    print("El seu valor màxim és", reduce(lambda x, y: x if x>y else y, llista))

def mitjana(llista):
    print("El valor de la mitjana és", reduce(lambda x, y: x+y,llista)/ len(llista))

def flatten(llista):
    if isinstance(llista,list):
        l = []
        for x in llista: l+= flatten(x)
        return l
    else: return [llista]

def insert(llista, elem):
    #TODO:preguntar si algu ho ha fet sense fors o sense bisect
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

def separallista(llista):
    parell = [i for i in llista if i%2==0]
    imparell = [i for i in llista if i%2!=0]
    print("Imparells", imparell)
    print("Parells", parell)
    return (imparell,parell)

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


#funcions d'ordre superior

def product(llista):
   return reduce(lambda x,y: x*y,llista)


def howmanytimes(llista, elem):
    return llista.count(elem)
    
def invertir(llista):
    #preguntar al profe 
    print("TT")

def productpar(llista):
    return reduce(lambda x,y: x*y if y%2 == 0 else x,llista)


if __name__ == '__main__':
    #TODO: preguntar què passa si son de tipus diferents 
    llista=[1,2,2.3,9]
    print("Llista que estem avaluant", llista)
    print()
    elements_diferents(llista)
    print()
    max_llista(llista)
    print()
    mitjana(llista)
    print()
    insert(llista,-1)
    insert(llista,4)
    print()
    llista_to_flatten=[1,[2,3,4],[2],[3]]
    print("LLista que hem d'aplanar", llista_to_flatten)
    print("LLista aplanada", flatten(llista_to_flatten))
    print()
    llistaparellsimparells = [1,2,3,4,5,6,7,8]
    print("Llista de parells i imparells", llistaparellsimparells)
    separallista(llistaparellsimparells)
    print()
    print("Llistat de divisors primers de",1560 )
    print(primeDivisors(1560))
    print()
    print("Producte dels elements de", llista)
    print(product(llista))
    print()
    print("Multiplica tots els elements parells de", [1,2,3,4])
    print(productpar([1,2,3,4]))
    print()
    print("Invertir la llista",llista, "amb reduce")
    print(invertir(llista))
    print()
    print("Quants cops apareix", 4,"a",llista,"?")
    print(howmanytimes(llista, 4))

