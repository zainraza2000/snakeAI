import curses
from importlib import import_module
import random
from re import T
import sys
import time
import os
from webbrowser import Galeon
class snake:
    def __init__(self):
        self.direction = curses.KEY_UP
        self.cords = [[3,3]]
    def set_direction(self, ch):
        if ch == curses.KEY_LEFT and self.direction == curses.KEY_RIGHT:
            return
        if ch == curses.KEY_RIGHT and self.direction == curses.KEY_LEFT:
            return
        if ch == curses.KEY_UP and self.direction == curses.KEY_DOWN:
            return
        if ch == curses.KEY_DOWN and self.direction == curses.KEY_UP:
            return 

        self.direction = ch
    def move(self):
        head = self.cords[-1][:]

        if self.direction == curses.KEY_UP:
            head[0]-=1
        elif self.direction == curses.KEY_DOWN:
            head[0]+=1
        elif self.direction == curses.KEY_RIGHT:
            head[1]+=1
        elif self.direction == curses.KEY_LEFT:
            head[1]-=1
        del(self.cords[0])
        self.cords.append(head)

    def add_unit(self):
        a = self.cords[0]
        b = self.cords[1]
        c_tail = a[:]
        if a[0] < b[0]:
            c_tail[0] -= 1
        elif a[0] > b[0]:
            c_tail[0] += 1
        elif a[1] < b[1]:
            c_tail[0] -= 1
        elif a[1] > b[1]:
            c_tail[0] += 1
class game:
    def __init__(self,size):
        self.board = [[' ' for i in range(size)] for j in range(size)]
        self.size = size
        for i in range(0,size):
            for j in range(0,size):
                if i==0 or i==size-1 or j==0 or j==size-1:
                    self.board[i][j] = '#'
                    continue
                self.board[i][j] = ' '
        self.a_cord = [-1,-1]
        self.snake = snake()
    def change_disp(self,x_c,y_c):
        self.board[x_c][y_c].change_unit()
    def render_board(self):
        for i, j in self.snake.cords:
            self.board[i][j] = 'x'
    def disp_board(self,screen):
        for i in range(0,self.size):
            row = ''
            for j in range(0,self.size):
                row += (self.board[i][j] + " ")
            screen.addstr(i, 0, row)
    def generate_apple(self):
        rand_x = 0
        rand_y = 0
        while(1):
            rand_x = random.randint(1,self.size-2)
            rand_y = random.randint(1,self.size-2)
            if self.board[rand_x][rand_y] == ' ':
                if self.a_cord[0] != -1:
                    self.board[self.a_cord[0]][self.a_cord[1]] = ' '
                self.a_cord[0] = rand_x
                self.a_cord[1] = rand_y
                break
            else:
                continue
        self.board[rand_x][rand_y] = 'O'
    def forward_frame(self):
        self.snake.move()
        if self.snake.cords[-1][0] == 0 or self.snake.cords[-1][1] == 0 or self.snake.cords[-1][0] == self.size - 2 or self.snake.cords[-1][1] == self.size - 2:
            return 1
        elif self.snake.cords[-1][:] == self.a_cord[:]:
            self.generate_apple()
            return 0
        else:
            return 0
        
def main(screen):
    screen.timeout(0)
    gam = game(10)
    gam.generate_apple()
    while(1):
        ch = screen.getch()
        gam.render_board()
        screen.addstr(11, 0, str(gam.snake.cords[-1][0]))
        if gam.forward_frame():
           continue
           #break
        gam.disp_board(screen=screen)
        time.sleep(0.5)
        screen.refresh()
if __name__=='__main__':
    curses.wrapper(main)
    
