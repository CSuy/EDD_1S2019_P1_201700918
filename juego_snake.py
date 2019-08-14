import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint
from ListaDoble import ListaDoble
from Pila import Pila
from ListaCircular import ListaCircular
import csv

height = 30
width = 55
pos_y = 0
pos_x = 0
lista = ListaDoble()
pila = Pila()
listac=ListaCircular()
usuario=""
class Serpiente(object):
    Direccion_ = { #se verifica que solo estas direcciones puede tomar dentro de la ventana
        KEY_UP: KEY_DOWN, KEY_DOWN: KEY_UP,
        KEY_LEFT: KEY_RIGHT, KEY_RIGHT: KEY_LEFT,
    }
    def __init__(self, pos_x1,pos_y1,window):
        self.lista=[] #solo servira para guardar el cuerpo
        self.puntuacion=0
        for i in range(2,0,-1):
            self.lista.append(Cuerpo(pos_x1-i,pos_y1))
        self.lista.append(Cuerpo(pos_x1,pos_y1))
        self.window=window
        self.direction = KEY_RIGHT
        self.despues_cabeza=(pos_x1,pos_y1)
        self.direccion = {
            KEY_UP: self.arriba,
            KEY_DOWN: self.abajo,
            KEY_LEFT: self.izquierda,
            KEY_RIGHT: self.derecha
        }
    @property
    def punteo(self):
        return 'Score : {}'.format(self.puntuacion)+ " Jugador: "+usuario
    def agregar(self,cuerpo):
        self.lista.extend(cuerpo)
    def comer(self,comida,signo):
        if signo=="+":
            self.puntuacion +=1
            cuerpo=Cuerpo(self.despues_cabeza[0],self.despues_cabeza[1])
            self.lista.insert(-1,cuerpo)
        elif signo=="*" and len(self.lista)>3:
            self.puntuacion -=1
            cuerpo=Cuerpo(self.despues_cabeza[0],self.despues_cabeza[1])
            self.lista.pop()
            pila.sacar()
        comida.reinicio_bocado()
        

    @property
    def gameOver(self):
        return any([cuerpo.coordenadas1==self.cabeza.coordenadas1
                    for cuerpo in self.lista[:-1]])

    def animacion(self):
        despues_cuerpo = self.lista.pop(0)
        despues_cuerpo.coorX=self.lista[-1].coorX
        despues_cuerpo.coorY=self.lista[-1].coorY
        self.lista.insert(-1,despues_cuerpo)
        self.despues_cabeza=(self.cabeza.coorX,self.cabeza.coorY)
        self.direccion[self.direction]()
        self.window.addstr(0,30,str(self.cabeza.coorX))

    def cambio_posicion(self,direccion):
        if direccion != Serpiente.Direccion_[self.direction]:
            self.direction=direccion
    
    def actualizacion(self):
        for cuerpo in self.lista:
            self.window.addstr(cuerpo.coorY,cuerpo.coorX,cuerpo.signo)
    @property
    def cabeza(self):
        return self.lista[-1]
    @property
    def coor(self):
        return self.cabeza.pos_x1, self.cabeza.pos_y1
    def arriba(self):
        self.cabeza.coorY -=1
        if self.cabeza.coorY<1:
            self.cabeza.coorY=height-2
    def abajo(self):
        self.cabeza.coorY +=1
        if self.cabeza.coorY>height-2:
            self.cabeza.coorY=1
    def izquierda(self):
        self.cabeza.coorX -=1
        if self.cabeza.coorX<1:
            self.cabeza.coorX=width-2
    def derecha(self):
        self.cabeza.coorX +=1
        if self.cabeza.coorX>width-2:
            self.cabeza.coorX=1

    def agregarLista(self):
        for i in range(len(self.lista)):
            lista.insertar(self.lista[i].coorX,self.lista[i].coorY)
        lista.graficar()

    def agregarPila(self,x,y):
        pila.meter(x,y)


class Cuerpo(object):
    def __init__(self,coorX,coorY):
        self.coorX=coorX
        self.coorY=coorY
        self.signo="#"
    @property
    def coordenadas1(self):
        return self.coorX,self.coorY
    def coordenadas(self):
        return '({},{})'.format(self.coorX,self.coorY)

class Comida(object):
    def __init__(self,window):
        self.posx=randint(1,53)
        self.posy=randint(1,28)
        self.window=window
        self.bocado1=""
    def bocado(self,tipoBocado):
        if tipoBocado<7:
            self.window.addstr(self.posy,self.posx,"+")
            self.bocado1="+"
        else:
            self.window.addstr(self.posy,self.posx,"*")
            self.bocado1="*"

    def reinicio_bocado(self):
        self.posx=randint(1,53)
        self.posy=randint(1,28)

def menu_principal(win):
    win.clear()
    win.border(0)
    win.addstr(13,18,"1.Play")
    win.addstr(14,18,"2.Puntuaciones")
    win.addstr(15,18,"3.Jugadores")
    win.addstr(16,18,"4.Reportes")
    win.addstr(17,18,"5.Carga Masiva")
    win.timeout(-1)

def juego(windows):      
    #if __name__ == '__main__':
        stdscr1 = curses.initscr() 
        window=windows
        window = curses.newwin(height,width,0,0)
        window.keypad(True)
        curses.noecho()
        window.timeout(100)
        snake=Serpiente(4,2,window)
        food=Comida(window)
        prueba=randint(0,10)
        key=KEY_DOWN
        player=usuario
        while key!=27:
            window.clear()
            window.border(0)
            snake.actualizacion()
            food.bocado(prueba)
            window.addstr(0, 5, snake.punteo)
            window.addstr(0,30,"Jugador: ")
            event = window.getch()
            #if event == 27:
                #ciclo==False
                #menu_principal(window)
            if event is not -1:
                key=event
            if event in [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT]:
                snake.cambio_posicion(event)
            if snake.cabeza.coorX == food.posx and snake.cabeza.coorY == food.posy:
                snake.comer(food,food.bocado1)
                if food.bocado1=="+":
                    snake.agregarPila(food.posx,food.posy)
                prueba=randint(0,10)
            if event==49:
                window.timeout(-1)
                snake.agregarLista()
            if event==57:
                window.timeout(100)
                lista.quitar()
            if event == 32:
                key = -1
                while key != 32:
                    key = window.getch()
            snake.animacion()
            if snake.gameOver:
                snake.agregarLista()
                pila.graficar()
                break
        curses.endwin()

def carga(windo):
    windo.clear()
    windo.refresh()
    windo.border(0)
    curses.noecho()
    windo.addstr(0,15,"Modulo de Carga Masiva")
    windo.addstr(3,2,"Nombre del .csv:")
    archivo=""
    listaUser=[]
    while True:
        windo.clear()
        windo.border(0)
        windo.addstr(0,15,"Modulo de Carga Masiva")
        windo.addstr(3,2,"Nombre del .csv:")
        windo.addstr(4,2,archivo)
        key1=windo.getkey()
        if key1 is chr(10):
                with open(archivo) as f:
                    reader = csv.reader(f)
                    for fila in reader:
                        user="{}".format(fila[0])
                        listaUser.append(user)
                    for i in range(1,len(listaUser)):
                        listac.insertar(listaUser[i])
                windo.addstr(5,2,"Se ingreso con exito")
                break
        elif key1 is "+":
            break
        else:
            archivo=archivo+key1
        windo.refresh()
        
def jugador(windo):
    windo.clear()
    windo.refresh()
    windo.border(0)
    curses.noecho()
    windo.addstr(0,15,"Modulo de Jugadores")
    pos=1
    while True:
        windo.clear()
        windo.border(0)
        windo.addstr(0,15,"Modulo de Jugadores")
        if pos==1:
            temporal=listac.primero
            windo.addstr(15,25-len(temporal.jugador),temporal.jugador+"-->")
            usuario=temporal.jugador
        elif pos==listac.tam:
            temporal=listac.primero
            for i in range(listac.tam-1):
                temporal=temporal.siguiente
            window.addstr(15,25-len(temporal.jugador),"<--"+temporal.jugador)
            usuario=temporal.jugador
        else:
            temporal=listac.primero
            for i in range(pos-1):
                temporal=temporal.siguiente
            window.addstr(15,28-len(temporal.jugador),"<--"+temporal.jugador+"-->")
            usuario=temporal.jugador
        key=windo.getch()
        if listac.vacia():
            windo.addstr(1,2,"No hay jugadores en la lista")
        else:
            if key==curses.KEY_RIGHT:
                pos +=1
            elif key == curses.KEY_LEFT:
                pos -=1
            elif key==27:
                break
            elif key == 10:
                windo.clear()
                windo.refresh()
                windo.border(0)
                curses.noecho()
                windo.addstr(0,15,"Modulo de Jugadores")
                windo.addstr(15,15,"Se eligio al Jugador: "+usuario)
                break
            if pos<0:
                pos=1
            if pos>listac.tam:
                pos=listac.tam
        windo.refresh()


def wait_esc(win):
    key = win.getch()
    while key!=27:
        key = win.getch()

stdscr = curses.initscr() 
window = curses.newwin(height,width,0,0)
window.keypad(True)
curses.noecho()
window.border(0)
keystroke = -1
menu_principal(window)
while(keystroke==-1):
    keystroke = window.getch()  #get current key being pressed
    if(keystroke==49): #1
        juego(window)
        wait_esc(window)
        window.clear()
        menu_principal(window)
        keystroke=-1
    elif(keystroke==50):
        paint_title(window, ' SCOREBOARD ')
        wait_esc(window)
        paint_menu(window)
        keystroke=-1
    elif(keystroke==51):
        listac.graficar()
        jugador(window)
        wait_esc(window)
        window.clear()
        menu_principal(window)
        keystroke=-1
    elif(keystroke==52):
        paint_title(window, ' REPORTS ')
        wait_esc(window)
        paint_menu(window)
        keystroke=-1
    elif(keystroke==53):
        carga(window)
        wait_esc(window)
        menu_principal(window)
        keystroke=-1
    elif(keystroke==54):
        pass
    else:
        keystroke=-1

curses.endwin()