from nodo import Nodo_1

class ListaDoble():
    def __init__(self):
        self.primero=None
        self.tam=0

    def vacia(self):
        return self.tam==0
    
    def insertar(self, valorX, valorY):
        nuevo=Nodo_1(valorX,valorY)
        if self.vacia():
            self.primero=nuevo
            self.primero.siguiente=None
            self.primero.anterior=None
            self.tam +=1
        else:
            temporal=self.primero
            while (temporal.siguiente!=None):
                temporal=temporal.siguiente
            temporal.siguiente=nuevo
            nuevo.siguiente=None
            nuevo.anterior=temporal
            self.tam +=1
    
    def quitar(self):
        temporal=self.primero
        x=1
        while (temporal.siguiente!=None and x<self.tam):
            temporal=temporal.siguiente
            x +=1
        temporal.siguiente=None
        self.tam=self.tam-1
    
    def mostrar(self):
        if self.vacia():
            print("esta vacia la lista")
        else:
            temporal=self.primero
            print("----- los valores de la lista -----")
            for j in range(self.tam):
                print("El valor X: ",temporal.valorX, " y el valor Y: ", temporal.valorY)
                temporal=temporal.siguiente
        
        
lista = ListaDoble()
lista.insertar(2,3)
lista.insertar(2,4)
lista.insertar(2,5)
lista.insertar(6,7)
lista.insertar(9,34)
lista.mostrar()
lista.quitar()
lista.mostrar()