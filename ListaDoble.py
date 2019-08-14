from nodo import Nodo_1
import os

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
        #temporal=self.primero
        #x=1
        #while (temporal.siguiente!=None and x<self.tam):
            #temporal=temporal.siguiente
            #x +=1
        #temporal.siguiente=None
        #self.tam=self.tam-1
        self.primero=None
        self.tam=0
    
    def mostrar(self):
        if self.vacia():
            print("esta vacia la lista")
        else:
            temporal=self.primero
            print("----- los valores de la lista -----")
            for j in range(self.tam):
                print("El valor X: ",temporal.valorX, " y el valor Y: ", temporal.valorY)
                temporal=temporal.siguiente
        
    def graficar(self):
            archivo = "ListaDoble.jpg"
            a = open("ListaDobleEnlazada.dot","w")
            a.write("digraph lista{\n")
            a.write("rankdir=LR;\n")
            a.write("node[shape = record];\n")
            a.write("nodonull1[label="+chr(34)+"null"+chr(34)+"];\n")
            a.write("nodonull2[label="+chr(34)+"null"+chr(34)+"];\n")
            temporal=self.primero
            con=0
            for g in range(self.tam):
                a.write("nodo"+str(g)+" [label="+chr(34)+"{|("+str(temporal.valorX)+","+str(temporal.valorY)+")|}"+chr(34)+"];\n")
                temporal=temporal.siguiente
            a.write("nodonull1->nodo0 [dir=back];\n")
            for h in range(self.tam-1):
                c=h+1
                a.write("nodo"+str(h)+"->nodo"+str(c)+";\n")
                a.write("nodo"+str(c)+"->nodo"+str(h)+";\n")
                con=c
            a.write("nodo"+str(con)+"->nodonull2;\n")
            a.write("}")
            a.close()
            os.system("dot -Tjpg ListaDobleEnlazada.dot -o"+archivo)
            os.system(archivo)
            