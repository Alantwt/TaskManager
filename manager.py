

from tkinter import *
from tkinter import ttk
import screens as sc
import database as dtb

clssDF = dtb.Datafile()

SEETASKSCREEN = "see"
ADDTASKSCREEN = "add"
MODIFYTASKSCREEN = "mod"
DELETETASKSCREEN = "del"

#RAIZ DE LA APLICACION
class Root(Tk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.title("TKM")
        self.geometry("500x700")
        #self.iconbitmap("constants\images\pro.ico")
        self.resizable(0,1)
        App(self)


#FRAME PRINCIPAL DE LA APLICACION
class App():
    def __init__(self,parent):
        self.Notebook = None
        self.parent = parent
        self.create_navbar()
        self.pages_screens("see")
        
        #VARIABLES QUE USO
        # self.menu = None
        # self.OptionMenu = None
        # self.ConfigSectionMenu = None
        # self.HelpMenu = None
        # self.Notebook = None
        # self.AddTask = None
        # self.SeeTask = None
        # self.ModTask = None
        # self.DelTask = None
        # self.FrameSection = None

    #------------------------------------------------------------------------------MENU----------------------------------------------------------------
        self.menu = Menu(self.parent)
        self.parent.config(menu= self.menu)
    #-------------------------------------------------Options(add,see,mod,del)---------------------------------------------------------------------------
        self.OptionMenu = Menu(self.menu,tearoff=0,)
        self.OptionMenu.add_command(label="Add Task",command=lambda:self.pages_screens("add"))
        self.OptionMenu.add_command(label="See Task",command=lambda:self.pages_screens("see"))
        self.OptionMenu.add_command(label="Modify Task",command=lambda:self.pages_screens("mod"))
        self.OptionMenu.add_command(label="Delete Task",command=lambda:self.pages_screens("del"))
        self.menu.add_cascade(label="Options",menu=self.OptionMenu)
    #-------------------------------------------------Settings------------------------------------------------------------------------------------    
        self.ConfigSectionMenu = Menu(self.menu,tearoff=0)
        self.ConfigSectionMenu.add_command(label="Sections",command=lambda:self.sections_screen())
        self.menu.add_cascade(label="Settings",menu=self.ConfigSectionMenu)    
    #--------------------------------------------------Help----------------------------------------------------------------------------------------------
        self.HelpMenu = Menu(self.menu,tearoff=0)
        self.menu.add_cascade(label="help",menu=self.HelpMenu)

    def create_navbar(self,):
        from constants.style import Navbar_BackGround
        self.Notebook = ttk.Notebook(self.parent,style="NB.TFrame",padding=(7,3,7,7))
        self.Notebook.place(relheight=1,relwidth=1,relx=0,rely=0)
    
    #------------------------------------------------------------Pestañas(add,see,del,mod task)----------------------------------------------------------    
    def pages_screens(self,pag):
        self.Notebook.tkraise()
        if pag == "add":
            try:
                self.del_pages(self.AddTask)
            except:
                pass
            self.AddTask = sc.Addtask(self.Notebook,self.parent)
            self.Notebook.add(self.AddTask,text="AddTasks")
            ttk.Button(self.AddTask,text="x",command=lambda:self.del_pages(self.AddTask),width=2).place(y=2,x=462)
            ttk.Button(self.AddTask,text="R",command=lambda:self.pages_screens("add"),width=2).place(y=2,x=438)

        elif pag == "see":
            try:    
                self.del_pages(self.SeeTask)
            except:
                pass
            self.SeeTask = sc.Seetask(self.Notebook)
            self.Notebook.add(self.SeeTask,text="See Tasks")
            ttk.Button(self.SeeTask,text="x",command=lambda:self.del_pages(self.SeeTask),width=2).place(y=2,x=445)
            ttk.Button(self.SeeTask,text="R",command=lambda:self.pages_screens("see"),width=2).place(y=2,x=420)
        elif pag == "mod":
            try:    
                self.del_pages(self.ModTask)
            except:
                pass
            self.ModTask = sc.Modifytask(self.Notebook)
            self.Notebook.add(self.ModTask,text="Modify Tasks")
            ttk.Button(self.ModTask,text="x",command=lambda:self.del_pages(self.ModTask),width=2).place(y=2,x=445)
            ttk.Button(self.ModTask,text="R",command=lambda:self.pages_screens("mod"),width=2).place(y=2,x=420)
        elif pag == "del":    
            try:    
                self.del_pages(self.DelTask)
            except:
                pass
            self.DelTask = sc.Deletetask(self.Notebook)
            self.Notebook.add(self.DelTask,text="Delete tasks")
            ttk.Button(self.DelTask,text="x",command=lambda:self.del_pages(self.DelTask),width=2).place(y=2,x=445)
            ttk.Button(self.DelTask,text="R",command=lambda:self.pages_screens("del"),width=2).place(y=2,x=420)

    def del_pages(self,page):
        self.Notebook.forget(page)

    #--------------------------------------------------------SECCIONES----------------------------------------------------------------------------
    def sections_screen(self):
        global clssDF
        self.FrameSection = ttk.Frame(self.parent,style=sc.BACK_CONTENT)
        self.FrameSection.place(relheight=1,relwidth=1,y=0,x=0)
        self.FrameSection.tkraise()
        
        #----------------------------------------------------FRAME-CREAR-SECCION--------------------------------------------------------------------
        Screate = ttk.Labelframe(self.FrameSection,text="Create Section",)
        Screate.place(relheight=0.47,relwidth=0.98,relx=0.01,y=10)
        ttk.Label(Screate,text="Se Creara en\nRuta: C:\TaskManager\TKManager\Data").grid(row=0,column=0,padx=10,pady=10)
        ttk.Label(Screate,text="Enter de Section Name:").grid(row=1,column=0)
        self.SectionValue = StringVar()
        sec = ttk.Entry(Screate,textvariable=self.SectionValue,width=10).grid(row=1,column=2)
        ttk.Button(Screate,text="Create",command=lambda:clssDF.create_sections(self.SectionValue.get())).grid(row=1,column=3,padx=5)
        #----------------------------------------------------FRAME-DELETE-SECCION-------------------------------------------------------------------
        #FRAME
        Sdelete = ttk.Labelframe(self.FrameSection,text="Delete Section")
        Sdelete.place(relheight=0.47,relwidth=0.98,relx=0.01,y=360)
        ttk.Label(Sdelete,text="Select the Section to delete").grid(row=0,column=0,pady=30)
        #OPTION SECTION
        clssDF.see_sections()
        self.SectionOptionValue = StringVar()
        SearchSection = ttk.OptionMenu(Sdelete,self.SectionOptionValue,*clssDF.SectionList).grid(row=0,column=1,pady=30)
        #BOTONES
        ttk.Button(Sdelete,text="delete",command=lambda:clssDF.delete_sections(self.SectionOptionValue.get())).grid(row=0,column=2,pady=30)
        ttk.Button(self.FrameSection,text="x",command= lambda:self.FrameSection.destroy(),padding=(0,0,0,0)).place(x=470,y=10,height=25,width=25)
        ttk.Button(self.FrameSection,text="R",command=lambda:self.reset_secction_screen(self.FrameSection)).place(x=445,y=10,height=25,width=25)
    
    def reset_secction_screen(self,frame):
        frame.destroy()
        self.sections_screen()
        




