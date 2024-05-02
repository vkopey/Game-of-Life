from nodebox.graphics import *
#import numpy as np
#np.random.randint(0,2,size=(10,10))
#import pyglet
import random

def neighbours(x,y):
    O=[(x+1,y),(x-1,y),(x,y+1),(x,y-1),(x+1,y+1),(x-1,y-1),(x-1,y+1),(x+1,y-1)]
    N=set()
    for a in A:
        if (a.x, a.y)!=(x,y):
            if (a.x, a.y) in O: N.add(a)
    return N

def exist(x,y):
    for a in A:
        if (a.x, a.y)==(x,y): return True
    return False

class CA(object):
    def __init__(self, x, y, live=True):
        self.x, self.y = x, y
        self.live=live
    def draw(self):
        rect(self.x*10, self.y*10, 10, 10)
    def rule(self):
        x, y = self.x, self.y
        O=[(x+1,y),(x-1,y),(x,y+1),(x,y-1),(x+1,y+1),(x-1,y-1),(x-1,y+1),(x+1,y-1)]
        S=set()
        if y==1: return S
        if x==1: return S
        if not exist(x,y-1):
            S.add((x,y-1))
            self.live=False
            return S
        d=random.choice([-1,1])
        if not exist(x-d,y-1):
            S.add((x-d,y-1))
            self.live=False
            return S
        return S


A={CA(10,10,True), CA(11,10,True), CA(12,10,True)}

def drawGrid(a=0):
    stroke(0, 0.1)
    for i in range(0,500,10):
        line(i, 0, i, 500)
        line(0, i, 500, i)


def draw(canvas):
    global step, pause
    if canvas.keys.char==" ": pause=not pause
    if canvas.mouse.button==LEFT:
        x,y=canvas.mouse.x, canvas.mouse.y
        x,y=x//10, y//10
        if not exist(x,y): A.add(CA(x,y))
    canvas.clear()
    drawGrid()
    text("Step %d\n\nN %d"%(step, len(A)), 510,450)
    for a in A:
        a.draw()
    if canvas.frame%10==9 and not pause:
        step+=1
        S=set()
        for a in A.copy():
            S.update(a.rule())
        for a in A.copy():
            if not a.live: A.remove(a)
        for i,j in S:
            if not exist(i,j):
                if 0<i<50 and 0<j<50: A.add(CA(i,j))


step=0
pause=False
canvas.size = 500, 500
canvas.run(draw)
