import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint

height = 30
width = 55
pos_y = 0
pos_x = 0

class Serpiente(object):
    Direccion_ = {
        KEY_UP: KEY_DOWN, KEY_DOWN: KEY_UP,
        KEY_LEFT: KEY_RIGHT, KEY_RIGHT: KEY_LEFT,
    }
    def __init__(self, pos_x1,pos_y1,window):
        self.lista=[]
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
        return 'Score : {}'.format(self.puntuacion)
    def agregar(self,cuerpo):
        self.lista.extend(cuerpo)
    def comer(self,comida,signo):
        comida.reinicio_bocado()
        if signo=="+":
            self.puntuacion +=1
            cuerpo=Cuerpo(self.despues_cabeza[0],self.despues_cabeza[1])
            self.lista.insert(-1,cuerpo)
        else:
            self.puntuacion -=1
            cuerpo=Cuerpo(self.despues_cabeza[0],self.despues_cabeza[1])
            self.lista.pop()
        

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

if __name__ == '__main__':
    stdscr = curses.initscr() 
    window = curses.newwin(height,width,0,0)
    window.keypad(True)
    curses.noecho()
    window.timeout(100)
    snake=Serpiente(4,2,window)
    food=Comida(window)
    prueba=randint(0,10)
    while True:
        window.clear()
        window.border(0)
        snake.actualizacion()
        food.bocado(prueba)
        window.addstr(0, 5, snake.punteo)
        event = window.getch()
        #if event == 27:
            #break
        if event in [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT]:
            snake.cambio_posicion(event)
        if snake.cabeza.coorX == food.posx and snake.cabeza.coorY == food.posy:
            snake.comer(food,food.bocado1)
            prueba=randint(0,10)
        if event == 32:
            key = -1
            while key != 32:
                key = window.getch()
        snake.animacion()
        if snake.gameOver:
            break
    curses.endwin()