from Pila import Pila
from ListaDoble import ListaDoble
from Cola import Cola
from ListaCircular import ListaCircular

class prueba():
    pila = Pila()
    pila.meter(2,2)
    pila.meter(2,3)
    pila.meter(2,4)
    pila.meter(2,5)
    pila.meter(2,6)
    #pila.mostrar()
    #pila.sacar()
    #pila.mostrar()
    pila.graficar()

    lista = ListaDoble()
    lista.insertar(2,3)
    lista.insertar(2,4)
    lista.insertar(2,5)
    lista.insertar(6,7)
    lista.insertar(9,34)
    lista.graficar()

    cola = Cola()
    cola.colar("jose",12)
    cola.colar("miguel",13)
    cola.colar("cristian",14)
    cola.colar("alberto",15)
    cola.colar("maria",16)
    cola.graficar()

    lista1 = ListaCircular()
    lista1.insertar("Dennis")
    lista1.insertar("Jennifer")
    lista1.insertar("Victor")
    lista1.insertar("Mario")
    lista1.insertar("Jonathan")
    lista1.insertar("Samantha")
    lista1.mostrar_siguientes()
    lista1.mostrar_anteriores()
    lista1.graficar()

    print("no hago nada")