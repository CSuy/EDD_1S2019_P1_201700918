import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint
from ListaDoble import ListaDoble
from Pila import Pila
from ListaCircular import ListaCircular
from Cola import Cola
import csv

height = 30
width = 55
pos_y = 0
pos_x = 0
lista = ListaDoble()
pila = Pila()
listac=ListaCircular()
cola=Cola()
usuario=""
class Player(object): #No hace nada 
    def __init__(self,wind):
        self.window=wind
        self.player=[]
    def asignacion(self,user):
        if self.player[0] is None:
            self.player.append(user)
        else:
            self.player.pop(0)
            self.player.append(user)
    @property
    def jugador(self):
        return "Jugador: {}".format(self.player[0])


class Serpiente(object):
    Direccion_ = { #se verifica que solo direcciones correctas puede tomar(ejemplo no puede ir de izquierda a derecha)
        KEY_UP: KEY_DOWN, KEY_DOWN: KEY_UP,
        KEY_LEFT: KEY_RIGHT, KEY_RIGHT: KEY_LEFT,
    }
    def __init__(self, pos_x1,pos_y1,window):
        self.lista=[] #solo servira para guardar el cuerpo de la serpiente
        self.puntuacion=0 #puntuacion
        for i in range(2,0,-1):
            self.lista.append(Cuerpo(pos_x1-i,pos_y1))
        self.lista.append(Cuerpo(pos_x1,pos_y1))
        self.window=window
        self.direction = KEY_RIGHT
        self.despues_cabeza=(pos_x1,pos_y1)
        self.direccion = { #para mejor manejo del movimiento de la serpiente
            KEY_UP: self.arriba,
            KEY_DOWN: self.abajo,
            KEY_LEFT: self.izquierda,
            KEY_RIGHT: self.derecha
        }
    @property
    def punteo(self):#funciona como un get por el @property, devuelve punteo
        return 'Score : {}'.format(self.puntuacion)
    def agregar(self,cuerpo):
        self.lista.extend(cuerpo)
    def comer(self,comida,signo):#aqui solo hacemos la logica del juego con cambio de tener 2 bocados
        if signo=="+":#agregarmos un simbolo mas al cuerpo
            self.puntuacion +=1
            cuerpo=Cuerpo(self.despues_cabeza[0],self.despues_cabeza[1])
            self.lista.insert(-1,cuerpo)
        elif signo=="*" and len(self.lista)>3:#quitamos pero sin perder el tamaño inicial de 3
            self.puntuacion -=1
            cuerpo=Cuerpo(self.despues_cabeza[0],self.despues_cabeza[1])
            self.lista.pop()
            pila.sacar()
        comida.reinicio_bocado()
        
    def reinicio(self):#metodo solo para reiniciar los datos cuando se inicia nuevo juego o pasa de nivel
        for i in range(len(self.lista),3,-1):
            cuerpo=Cuerpo(self.despues_cabeza[0],self.despues_cabeza[1])
            self.lista.pop()
        for i in range(pila.tam):
            pila.sacar()

    @property
    def gameOver(self):#si la serpiente se come a ella misma, hacemos la lista vacia
        return any([cuerpo.coordenadas1==self.cabeza.coordenadas1
                    for cuerpo in self.lista[:-1]])

    def animacion(self):#esto nos ayudara a realizar el movimiento de la serpiente dependiendo donde se mueva
        despues_cuerpo = self.lista.pop(0)
        despues_cuerpo.coorX=self.lista[-1].coorX
        despues_cuerpo.coorY=self.lista[-1].coorY
        self.lista.insert(-1,despues_cuerpo)
        self.despues_cabeza=(self.cabeza.coorX,self.cabeza.coorY)
        self.direccion[self.direction]()
        self.window.addstr(0,30,str(self.cabeza.coorX))

    def cambio_posicion(self,direccion):#aqui solo tomamos la direccion que el jugador elija
        if direccion != Serpiente.Direccion_[self.direction]:
            self.direction=direccion
    
    def actualizacion(self):#para dibujar de nuevo el cuerpo en las nuevas que va tomando segun el movimiento
        for cuerpo in self.lista:
            self.window.addstr(cuerpo.coorY,cuerpo.coorX,cuerpo.signo)
    @property
    def cabeza(self):#solo para definir quien sera la cabeza de la serpiente
        return self.lista[-1]
    @property
    def coor(self):
        return self.cabeza.pos_x1, self.cabeza.pos_y1
    def arriba(self):#movimientos de la serpiente, tomar en consideracion algunos if, para no de error curses
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

    def agregarLista(self):#ingresamos a la lista doble donde se maneja la serpiente
        for i in range(len(self.lista)-1,-1,-1):
            lista.insertar(self.lista[i].coorX,self.lista[i].coorY)

    def agregarPila(self,x,y):#agregamos coordenadas de la comida en la pantalla a la pila
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
        if tipoBocado<13:
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
    win.addstr(0,20,"Juego De Snake")
    win.addstr(13,18,"1.Play")
    win.addstr(14,18,"2.Puntuaciones")
    win.addstr(15,18,"3.Jugadores")
    win.addstr(16,18,"4.Reportes")
    win.addstr(17,18,"5.Carga Masiva")
    win.timeout(-1)

def menu_reportes(win):
    win.clear()
    win.border(0)
    win.addstr(0,15,"Reportes de Estructuras")
    win.addstr(13,18,"1.Serpiente")
    win.addstr(14,18,"2.Puntuacion")
    win.addstr(15,18,"3.Puntuaciones")
    win.addstr(16,18,"4.Usuarios")
    win.timeout(-1)
    while True:
        key=win.getch()
        if key==49:
            lista.graficar()
        elif key==50:
            pila.graficar()
        elif key==51:
            cola.graficar()
        elif key==52:
            listac.graficar()
        elif key==27:
            break

def juego(windows,user):      
        stdscr1 = curses.initscr() 
        window=windows
        window = curses.newwin(height,width,0,0)
        window.keypad(True)
        curses.noecho()
        window.timeout(100)
        snake=Serpiente(4,2,window)
        food=Comida(window)
        snake.reinicio()
        prueba=randint(0,15)
        key=KEY_DOWN
        nivel=1
        next_level=15
        time=100
        lista.quitar()
        while key!=27:
            window.clear()
            window.border(0)
            snake.actualizacion()
            food.bocado(prueba)
            window.addstr(0, 5, snake.punteo)
            window.addstr(0,25,"Jugador: "+user)
            window.addstr(29,5,"Nivel: "+str(nivel))
            event = window.getch()
            if event is not -1:
                key=event
            if event in [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT]:#tomamos la direccion del teclado
                snake.cambio_posicion(event)
            if snake.cabeza.coorX == food.posx and snake.cabeza.coorY == food.posy:#para cuando comamos
                snake.comer(food,food.bocado1)
                if food.bocado1=="+":
                    snake.agregarPila(food.posx,food.posy)
                prueba=randint(0,15)
            if snake.puntuacion==next_level:#condicion para mejorar niveles(dificultad=sube de velocidad)
                snake.reinicio()
                nivel +=1
                next_level=next_level+10
                time=time-20
                window.timeout(time)
            if event==48:#poner pausa al juego
                window.timeout(-1)
                window.addstr(1,25,"Presiona 9 para reanudar")
                snake.agregarLista()
            if event==56:#se puede tomar como un game over automatico
                snake.agregarLista()
                cola.colar(user,snake.puntuacion)
                break
            if event==57:#reanudamos el juego
                window.timeout(100)
                lista.quitar()
            if event == 32:#para no elegir espacio
                key = -1
                while key != 32:
                    key = window.getch()
            if event == 49:#generar reporte del snake actual
                lista.graficar()
            if event == 50:#generar reporte del score
                pila.graficar()
            snake.animacion()
            if snake.gameOver:#si se come la serpiente
                snake.agregarLista()
                cola.colar(user,snake.puntuacion)
                break
        curses.endwin()

def carga(windo):#carga masiva, recordar apachar esc
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
            try:
                with open(archivo) as f:
                    reader = csv.reader(f)
                    for fila in reader:
                        user="{}".format(fila[0])
                        listaUser.append(user)
                    for i in range(1,len(listaUser)):
                        listac.insertar(listaUser[i])
                windo.addstr(5,2,"Se ingreso con exito")
                break
            except Exception:
                archivo=""
        elif key1 is "+":
            break
        else:
            archivo=archivo+key1
        windo.refresh()

def scores(win):#para mostrar puntuaciones, recordar apachar esc
    win.clear()
    win.border(0)
    win.addstr(0,21,"Puntuaciones")
    win.addstr(3,15,"Jugadores")
    win.addstr(3,30,"Puntuaciones")
    while True:
        win.clear()
        win.border(0)
        win.addstr(0,21,"Puntuaciones")
        win.addstr(3,15,"Jugadores")
        win.addstr(3,30,"Puntuaciones")
        key=win.getch()
        if cola.tam>0 and cola.tam<=10:
            temporal=cola.primero
            for i in range(cola.tam):
                win.addstr(4+i,15,temporal.nombre)
                win.addstr(4+i,36,str(temporal.puntuacion))
                temporal=temporal.siguiente
        else:
            cola.descolar()
            temporal=cola.primero
            for i in range(cola.tam):
                win.addstr(4+i,15,temporal.nombre)
                win.addstr(4+i,36,str(temporal.puntuacion))
                temporal=temporal.siguiente
        if key==27:
            break
        win.refresh()

def wait_esc(win):
    key = win.getch()
    while key!=27:
        key = win.getch()

stdscr = curses.initscr() 
window = curses.newwin(height,width,0,0)
windo=window
window.keypad(True)
curses.noecho()
window.border(0)
keystroke = -1
menu_principal(window)
play=""
while(keystroke==-1):
    keystroke = window.getch()
    if(keystroke==49):#comenzar juego
        lista.quitar()
        if play is not "":#definimos si no hemos elegido jugador, debemos crear 1 nuevo
            juego(window,play)
            wait_esc(window)
            window.clear()
            menu_principal(window)
        else:
            windo.clear()
            windo.refresh()
            windo.border(0)
            curses.noecho()
            windo.addstr(0,15,"Creacion de Jugador")
            windo.addstr(3,2,"Nombre del jugador")
            nombre=""
            listaUser=[]
            while True:
                windo.clear()
                windo.border(0)
                windo.addstr(0,15,"Creacion de Jugador")
                windo.addstr(3,2,"Nombre del jugador")
                windo.addstr(4,2,nombre)
                key1=windo.getkey()
                if key1 is chr(10):
                    listac.insertar(nombre)
                    play=nombre
                    windo.addstr(5,2,"Se ingreso con exito el jugador: "+play)
                    break
                elif key1 is "+":
                    break
                else:
                    nombre=nombre+key1
                windo.refresh()
            window.clear()
            juego(window,play)
            wait_esc(window)
            window.clear()
            menu_principal(window)
        keystroke=-1
    elif(keystroke==50):#puntuaciones hasta el momento
        scores(window)
        wait_esc(window)
        window.clear()
        menu_principal(window)
        keystroke=-1
    elif(keystroke==51):#para seleccionar jugadores
        windo.clear()
        windo.refresh()
        windo.border(0)
        curses.noecho()
        windo.addstr(0,15,"Modulo de Jugadores")
        pos=1
        usuario1=""
        while True:
            windo.clear()
            windo.border(0)
            windo.addstr(0,15,"Modulo de Jugadores")
            if pos==1:
               temporal=listac.primero
               windo.addstr(15,25-len(temporal.jugador),temporal.jugador+"-->")
               usuario1=temporal.jugador
            elif pos==listac.tam:
                temporal=listac.primero
                for i in range(listac.tam-1):
                    temporal=temporal.siguiente
                window.addstr(15,25-len(temporal.jugador),"<--"+temporal.jugador)
                usuario1=temporal.jugador
            else:
                temporal=listac.primero
                for i in range(pos-1):
                    temporal=temporal.siguiente
                window.addstr(15,28-len(temporal.jugador),"<--"+temporal.jugador+"-->")
                usuario1=temporal.jugador
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
                    windo.addstr(15,15,"Se eligio al Jugador: "+usuario1)
                    play=usuario1
                    break
                if pos<0:
                    pos=1
                if pos>listac.tam:
                    pos=listac.tam
            windo.refresh()
        wait_esc(window)
        window.clear()
        menu_principal(window)
        keystroke=-1
    elif(keystroke==52):#para mostrar los reportes
        menu_reportes(window)
        window.clear()
        wait_esc(window)
        menu_principal(window)
        keystroke=-1
    elif(keystroke==53):#para carga masiva
        carga(window)
        wait_esc(window)
        menu_principal(window)
        keystroke=-1
    elif(keystroke==54):#salir del juego
        pass
    else:
        keystroke=-1

curses.endwin()