from nodo import Nodo_4

class ListaCircular():
    def __init__(self):
        self.primero=None
        self.tam=0
    
    def vacia(self):
        return self.tam==0

    def insertar(self,jugador):
        nuevo=Nodo_4(jugador)
        if self.vacia():
            self.primero=nuevo
            self.primero.siguiente=self.primero
            self.primero.anterior=self.primero
            self.tam +=1
        else:
            aux=self.primero
            x=1
            while(x<self.tam):
                aux=aux.siguiente
                x +=1
            aux.siguiente=nuevo
            nuevo.siguiente=self.primero
            nuevo.anterior=aux
            self.primero.anterior=nuevo
            self.tam +=1
    
    def mostrar_siguientes(self):
        if self.vacia():
            print("La Lista esta vacia")
        else:
            temporal=self.primero
            print("-----Impresion de los siguientes-----")
            for j in range(self.tam):
                print("El jugador es: ", temporal.jugador)
                temporal=temporal.siguiente
                
    def mostrar_anteriores(self):
        if self.vacia():
            print("La Lista esta vacia")
        else:
            temporal=self.primero
            print("-----Impresion de los anteriores-----")
            for j in range(self.tam):
                print("El jugador es: ", temporal.jugador)
                temporal=temporal.anterior