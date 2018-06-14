from tkinter import *
from tkinter import ttk
root = Tk()

root.geometry('220x454')

mpb = ttk.Progressbar(root,orient ="horizontal",length = 200, mode ="determinate")
mpb.pack()
mpb["maximum"] = 100
mpb["value"] = 25
root.mainloop()