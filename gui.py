import tkinter as tk
import numpy as np
import sympy as sy

#import solver as sl
from components import *

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.frame = tk.Frame(parent)
        self.frame.pack()
        self.frame1 = tk.Frame(self.frame)
        self.frame1.pack(side = tk.LEFT)
        self.b1 = tk.Button(self.frame1, text = 'Point', command = self.point)
        self.b1.pack(side = tk.TOP)
        self.b2 = tk.Button(self.frame1, text = 'Mass', command = self.mass)
        self.b2.pack(side = tk.TOP)
        self.b3 = tk.Button(self.frame1, text = 'Connector', command = self.connector)
        self.b3.pack(side = tk.TOP)
        self.b4 = tk.Button(self.frame1, text = 'Spring', command = self.spring)
        self.b4.pack(side = tk.TOP)
        self.b5 = tk.Button(self.frame1, text = 'Drum', command = self.drum)
        self.b5.pack(side = tk.TOP)

        self.canvas = tk.Canvas(self.frame, height = 500, width = 500, bg = 'white')
        self.canvas.pack(side = tk.RIGHT)

        self.parent.bind('<Escape>', self.esc)

        self.canvas.bind("<Button-1>", self.place)

        self.selected = None

        self.prior_con = []
        self.prior_spr = []

        self.con = 0
        self.spr = 0

    def point(self):
        self.selected = 0

    def mass(self):
        self.selected = 1

    def connector(self):
        self.selected = 2

    def spring(self):
        self.selected = 3

    def drum(self):
        self.selected = 4

    def esc(self, event):
        self.prior_con = []
        self.selected = None

    def place(self, event):
        if self.selected is None:
            return

        if self.selected == 0:
            self.prior_con = []
            self.prior_spr = []
            self.canvas.create_oval(event.x, event.y, event.x + 10, event.y + 10, fill = 'red')
        
        if self.selected == 1:
            self.prior_con = []
            self.prior_spr = []
            self.canvas.create_rectangle(event.x, event.y, event.x + 50, event.y + 50, fill = 'green')

        if self.selected == 2:
            if self.con > 1:
                self.selected = None
                self.con = 0
                self.prior_con = []
                return
            if self.prior_con:
                self.canvas.create_line(self.prior_con[0], self.prior_con[1], event.x, event.y, fill = 'black', width = 4)
            self.prior_con = [event.x, event.y]
            self.con += 1

        if self.selected == 3:
            if self.spr > 1:
                self.selected = None
                self.spr = 0
                self.prior_spr = []
                return
            if self.prior_spr:
                self.canvas.create_line(self.prior_spr[0], self.prior_spr[1], event.x, event.y, fill = 'yellow', width = 4)
            self.prior_spr = [event.x, event.y]
            self.spr += 1

        if self.selected == 4:
            self.prior_con = []
            self.prior_spr = []
            self.canvas.create_oval(event.x, event.y, event.x + 50, event.y + 50, fill = 'purple')




        

if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
