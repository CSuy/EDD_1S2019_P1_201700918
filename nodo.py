class Nodo_1(): #ESTE NODO SERVIRA PARA LA LISTA DOBLEMENTE ENLAZADA
    def __init__(self,valorX, valorY):
        self.siguiente=None
        self.anterior=None
        self.valorX=valorX
        self.valorY=valorY

class Nodo_2(): #ESTE NODO SERVIRA PARA LA PILA
    def __init__(self,valorX, valorY):
        self.siguiente=None
        self.valorX=valorX
        self.valorY=valorY

class Nodo_3(): #ESTE NODO SERVIRA PARA LA COLA 
    def __init__(self,nombre, puntuacion):
        self.siguiente=None
        self.nombre=nombre
        self.puntuacion=puntuacion


class Nodo_4(): # ESTE NODO SERVIRA PARA LA LISTA CIRCULAR DOBLEMENTE ENLAZADA
    def __init__(self,jugador):
        self.siguiente=None
        self.anterior=None
        self.jugador=jugador