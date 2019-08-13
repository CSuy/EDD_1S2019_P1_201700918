import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint

height = 30
width = 55
pos_y = 0
pos_x = 0
class serpiente():
    def __init__(self, pos_x1, pos_y1,window): #iniciamos el juego con un score
        self.puntuacion=0
        self.cuerpo=[] #donde se dibujara el cuerpo
        self.window=window
        for i in range(2,0,-1): #tam_snake,donde termina,decrece en -1
            self.cuerpo.append(cuerpo(pos_x1-i,pos_y1))
        self.cuerpo.append(cuerpo(pos_x1,pos_y1))
        self.despues_cabeza=(pos_x1,pos_y1)

    #definimos un formato para la puntuacion -> toString()
    def punteo(self):
        return 'Score : {}'.format(self.puntuacion)
        
    def agregar(self,cuerpo):
        self.cuerpo.extend(cuerpo)
    
    def comer(self,comida):
        comida.reinicio_bocado()
        cuerpo=cuerpo(self.despues_cabeza[0],self.despues_cabeza[1])
        self.cuerpo.insert(-1,cuerpo)
        self.puntuacion +=1

    def GameOver(self):
        return any([cuerpo.coordenadas1==self.cabeza.coordenadas1
                        for cuerpo in self.cuerpo[:-1]])

    def animacion(self):
        despues_cuerpo=self.cuerpo.pop(0)
        despues_cuerpo.coorX=self.cuerpo[-1].coorX
        despues_cuerpo.coorY=self.cuerpo[-1].coorY
        self.cuerpo.insert(-1,despues_cuerpo)
        self.despues_cabeza=(self.cabeza.coorX,self.cabeza.coorY)

    def render(self):
        for cuerpo in self.cuerpo:
            self.window.addstr(cuerpo.coorY, cuerpo.coorX, cuerpo.signo)

    def Cabeza(self):
        return self.cuerpo[-1]

class cuerpo():
    def __init__(self,coorX,coorY):
        self.coorX=coorX
        self.coorY=coorY
        self.signo="#"

    def coordenadas1(self):
        return self.coorX,self.coorY
    def coordenadas(self):
        return '({},{})'.format(self.coorX,self.coorY)

class comida():
    def __init__(self):
        self.posx=randint(1,53)
        self.posy=randint(1,28)

    def bocado(self):
        tipoBocado=randint(1,5)
        return tipoBocado

    def reinicio_bocado(self):
        self.posx=randint(1,53)
        self.posy=randint(1,28)



stdscr = curses.initscr()
window = curses.newwin(height,width,pos_y,pos_x)
window.keypad(True)
curses.noecho()
curses.curs_set(0)
window.border(0)
window.nodelay(True) 
window.addstr(0,40,"Snake")
snake=serpiente(4,2,window)
food = comida()
boca=food.bocado()
window.addstr(0,5,snake.punteo())
if boca==3:
    window.addstr(food.posy,food.posx,"*")
else:
    window.addstr(food.posy,food.posx,"+")
key=KEY_RIGHT
while key!=27:
    window.timeout(100)
    keystroke = window.getch()
    snake.render()
curses.endwin()