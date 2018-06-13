import time
from tkinter import *
root= Tk()
root.geometry('200x200')
v = StringVar()

def boom1():
    v.set('vivek')
    root.after(1000,geek)
i=9
def geek():
    global i,v
    v.set(i)
    i-=1
frame =Frame(root)
frame.grid(row=0)
label =Label(frame,textvariable=v,bg='white')
label.grid(row=1)
button =Button(frame,text="boom",bg='white',command=lambda :boom1())
button.grid(row=0)
# button.bind('<Button-1>',boom)

root.mainloop()