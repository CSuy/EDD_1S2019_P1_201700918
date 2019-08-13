import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint

height = 30
width = 55
pos_y = 0
pos_x = 0
class serpiente():
    def __init__(self, pos_x1, pos_y1): #iniciamos el juego con un score
        self.puntuacion=0
        self.cuerpo=[] #donde se dibujara el cuerpo
        for i in range(3,0,-1): #tam_snake,donde termina,decrece en -1
            self.cuerpo.append(cuerpo(pos_x1,pos_y1))

    @property #definimos un formato para la puntuacion -> toString()
    def punteo(self):
        return 'Score : {}'.format(self.puntuacion)
        
class cuerpo():
    def __init__(self,coorX,coorY):
        self.coorX=coorX
        self.coorY=coorY
        self.signo="#"

    @property
    def coordenadas(self):
        return '({},{})'.format(self.coorX,self.coorY)

class comida():
    def __init__(self,bocado):
        self.posx=randint(1,53)
        self.posy=randint(1,28)
        self.bocado=bocado




stdscr = curses.initscr()
window = curses.newwin(height,width,pos_y,pos_x)
window.keypad(True)
curses.noecho()
curses.curs_set(0)
window.border(0)
window.nodelay(True) 
window.addstr(0,25,"Snake")
y,x=window.getmaxyx()
key=KEY_RIGHT
while key!=27:
    window.timeout(100)
    keystroke = window.getch()
    

curses.endwin()