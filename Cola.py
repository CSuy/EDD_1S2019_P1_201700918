from nodo import Nodo_3

class Cola():
    def __init__(self):
        self.primero=None
        self.tam=0

    def vacia(self):
        return self.tam==0

    def colar(self, nombre, puntuacion):
        nuevo=Nodo_3(nombre,puntuacion)
        if self.vacia():
            self.primero=nuevo
            self.primero.siguiente=None
            self.tam +=1
        else:
            temporal=self.primero
            while (temporal.siguiente!=None):
                temporal=temporal.siguiente
            temporal.siguiente=nuevo
            nuevo.siguiente=None
            self.tam +=1
        
    def descolar(self):
        aux=self.primero
        self.primero=aux.siguiente
        self.tam=self.tam-1

    def mostrar(self):
        if self.vacia():
            print("La cola esta vacia")
        else:
            temporal=self.primero
            print("-----Los elementos de la cola son-----")
            for j in range(self.tam):
                print("El nombre: ",temporal.nombre," y su puntuacion: ",temporal.puntuacion)
                temporal=temporal.siguiente