
from msilib.schema import Font
from tkinter import *
from tkinter import ttk
from tkinter import font

Navbar_BackGround = ttk.Style()
Navbar_BackGround.configure("NB.TFrame", foreground="red",background="#efefef",font=("arial",16))

MainFrame_BackGround = ttk.Style()
MainFrame_BackGround.configure("MF.TFrame",foreground="black",background="#bfbfbf")

content = font.Font(family="arial",size=10,weight="normal")

Label_Style = ttk.Style()
Label_Style.configure("LB.TLabel",background="#bfbfbf",font=content)
