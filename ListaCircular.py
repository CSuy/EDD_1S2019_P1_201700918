from nodo import Nodo_4
import os

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
                print("<---", temporal.jugador,"--->")
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

    def graficar(self):
        archivo="ListaCircular.jpg"
        a=open("ListaDobleCircular.dot","w")
        a.write("digraph listaCircular{\n")
        a.write("rankdir=LR;\n")
        a.write("node[shape = record];\n")
        temporal=self.primero
        con=0
        for g in range(self.tam):
            a.write("nodo"+str(g)+" [label="+chr(34)+"{|"+str(temporal.jugador)+"|}"+chr(34)+"];\n")
            temporal=temporal.siguiente
            aux=g
        for h in range(self.tam-1):
            c=h+1
            a.write("nodo"+str(h)+"->nodo"+str(c)+";\n")
            a.write("nodo"+str(c)+"->nodo"+str(h)+";\n")
            con=c
        a.write("nodo"+str(con)+"->nodo0;\n")
        a.write("nodo0->nodo"+str(con)+";\n")
        a.write("}")
        a.close()
        os.system("dot -Tjpg ListaDobleCircular.dot -o"+archivo)
        os.system(archivo)