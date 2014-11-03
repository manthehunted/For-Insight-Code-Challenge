from Tkinter import *
from ttk import Frame, Button, Style
from tkFileDialog import askopenfilename, asksaveasfilename
import numpy as np
import os
import csv
from sudoku import *

class Gui():

    def __init__(self):
        self.root = Tk()
        self.root.title("Fast Sudoku Solver")
        self.root.geometry("380x435+400+400")
        self.style = Style()
        self.style.theme_use("default")

        self.topFrame = Frame(self.root)
        self.topFrame.pack(fill=BOTH,side=TOP)
        self.txt = Text(self.root,width=300,height=25)
        self.txt.pack(fill=BOTH,side=TOP)

        self.bottomFrame = Frame(self.root)
        self.bottomFrame.pack(fill=BOTH,side=BOTTOM)

        #store a sudoku problem or solution
        self.var = StringVar(self.root)

        #Buttons
        openFileButton = Button(self.bottomFrame, text="New Problem!", command=self.openfile)
        openFileButton.pack(fill=BOTH,side=LEFT)

        processFileButton = Button(self.bottomFrame, text="Get Solution!!", command=self.processSudoku)
        processFileButton.pack(fill=BOTH,side=LEFT)

        refreshTxtButton = Button(self.bottomFrame, text="Clean Window")
        refreshTxtButton.bind("<Button-1>", self.refresh)
        refreshTxtButton.pack(fill=BOTH,side=LEFT)

        saveButton = Button(self.bottomFrame, text="Save Solution")
        saveButton.bind("<Button-1>", self.save)
        saveButton.pack(fill=BOTH,side=LEFT)

        quitButton = Button(self.bottomFrame, text='Quit', command=self.root.quit)
        quitButton.pack(fill=BOTH,side=LEFT)

        self.root.mainloop()


    def refresh(self, event):
        '''clear all the contents in the text window and clear the variable'''
        #print('refresh called')
        self.var.set(None)
        self.txt.delete(1.0, END)


    def save(self, event):
        '''save a solution'''
        #print('save called')
        val = self.var.get()
        val = list(val)

        n = int(np.sqrt(len(val)))
        val = np.array(val).reshape((n,n))

        filepath = os.path.abspath(__file__)
        filename = asksaveasfilename(initialdir=filepath)

        writer = csv.writer(open(filename+'.csv','wb'))
        for items in val:
            writer.writerow(items)


    def openfile(self):
        '''open a sudoku problem csv file'''
        #print("openfile called")
        self.txt.insert(END,"A loaded Sudoku problem is")
        self.txt.insert(END,"\n")
        filepath = os.path.abspath(__file__)
        filename = askopenfilename(initialdir=filepath)

        if filename:
            with open(filename, 'r') as csvfile:
                read = csv.reader(csvfile)
                storage = list()
                for content in read:
                    storage.append(content)

            self.var.set(storage)
            self.show()
        self.txt.insert(END,"\nIf the problem is correct, please press Solution button; "
                               "otherwise, please reload a problem")
        self.txt.config(wrap=WORD)
        self.txt.insert(END,"\n")


    def processSudoku(self):
        '''process the loaded problem, solve, and display'''

        problem = sudoku(self.var.get())
        solution = problem.solve()

        var = self.var.set(solution)

        self.txt.insert(END,"\nThe solution to the problem is")
        self.txt.insert(END,"\n")
        self.show()
        self.txt.insert(END,"\n")


    def show(self):
        '''show variable (problem or solution) in the format of sudoku grid'''

        val = self.var.get()

        if val != 'None': #if the solution is valid, then show
            val = val.translate(None,"'[],.:")
            val = ''.join(val.split())
            self.var.set(val)

            n = np.sqrt(len(val))
            flag = np.linspace(n-1, n*n-1, num=n)

            for ind, i in enumerate(val):
                if ind in flag:
                    self.txt.insert(END,i)
                    self.txt.insert(END,"\n")
                else:
                    if i == '0':
                        self.txt.insert(END,'-')
                        self.txt.insert(END," ")
                    else:
                        self.txt.insert(END,i)
                        self.txt.insert(END," ")
        else:
            self.txt.insert(END,"\n***Warning***\nNot a proper problem\nPlease reload a problem")
            self.txt.insert(END,"\n")
