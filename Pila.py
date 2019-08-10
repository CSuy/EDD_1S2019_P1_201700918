from nodo import Nodo_2
import os

class Pila():
    def __init__(self):
        self.primero=None
        self.tam=0

    def vacia(self):
        return self.tam==0

    def meter(self, valorX, valorY):
        nuevo=Nodo_2(valorX,valorY)
        if self.vacia():
            self.primero=nuevo
            self.primero.siguiente=None
            self.tam +=1
        else:
            nuevo.siguiente=self.primero
            self.primero=nuevo
            self.tam +=1

    def sacar(self):
        aux=self.primero
        self.primero=aux.siguiente
        self.tam=self.tam-1

    def mostrar(self):
        if self.vacia():
            print("esta vacia la lista")
        else:
            temporal=self.primero
            print("----- los valores de la Pila -----")
            for j in range(self.tam):
                print("El valor X: ",temporal.valorX, " y el valor Y: ", temporal.valorY)
                temporal=temporal.siguiente
    
    def graficar(self):
        archivo="pila.jpg"
        a=open("Pila.dot","w")
        a.write("digraph listaCircular{\n")
        a.write("rankdir=LR;\n")
        a.write("node[shape = record];\n")
        temporal=self.primero
        a.write("nodo0 [label="+chr(34))
        for h in range(self.tam):
            a.write("|"+str(temporal.valorY))
            temporal=temporal.siguiente
        a.write(chr(34)+"];")
        a.write("}")
        a.close()
        os.system("dot -Tjpg Pila.dot -o"+archivo)
        os.system(archivo)