from nodo import Nodo_3
import os

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

    def graficar(self):
            archivo = "Cola_J.jpg"
            a = open("Cola.dot","w")
            a.write("digraph lista{\n")
            a.write("rankdir=LR;\n")
            a.write("node[shape = record];\n")
            a.write("nodonull2[label="+chr(34)+"null"+chr(34)+"];\n")
            temporal=self.primero
            con=0
            for g in range(self.tam):
                a.write("nodo"+str(g)+" [label="+chr(34)+"{("+str(temporal.nombre)+","+str(temporal.puntuacion)+")|}"+chr(34)+"];\n")
                temporal=temporal.siguiente
            for h in range(self.tam-1):
                c=h+1
                a.write("nodo"+str(h)+"->nodo"+str(c)+";\n")
                con=c
            a.write("nodo"+str(con)+"->nodonull2;\n")
            a.write("}")
            a.close()
            os.system("dot -Tjpg Cola.dot -o"+archivo)
            os.system(archivo)