
from tkinter.scrolledtext import ScrolledText
import database as dtb
from tkinter import *
from tkinter import ttk
import datetime as dt
import functions as fc

#-----------------------------------------------------------------------CONSTANTES---------------------------------------------------------------------------
BACK_CONTENT = "MF.TFrame"
BACKLABEL_CONTENT = "LB.TLabel"
OPTION_DAYJ = ["","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
OPTION_MONTH = ["","JANUARY","FEBRUARY","MARCH","APRIL","MAY","JUNE","JULY","AUGUST","SEPTEMBER","OCTOBER","NOVEMBER","DECEMBER"]
OPTION_SEARCHTASK = ["","Month","Date","Name"]

#Instancia de la clase que maneja el fichero
TaskClass = dtb.Tasks()
#Instancia para la clase DataFile
DataFileClass = dtb.Datafile()
#Lista de tareas rescatadas de el fichero binario
TaskListUser = {}


#-----------------------------------------------------------------------PANTALLA PARA VER TAREAS--------------------------------------------------------------
class Seetask(ttk.Frame):
    def __init__(self,parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        from constants.style import MainFrame_BackGround
        self.pack()
        self.config()
        self.propagate(0)

        #VARIABLES QUE ESTOY UTILIZANDO
        self.FrameSearchOptions = None      #frame principal que utiliza el usuario para elejir el metodo de busqueda
        self.ScrollCanvaClass = None        #Instancia de la clase Scrollcanva que me sirve para tener una frame con scrollbar
        self.SearchTaskClass = None         #Instancia que me permite hacer la busqueda de tareas

        #-------------------------------FRAME PRINCIPAL DE OPCIONES--------------------------------------------
        self.FrameSearchOptions = ttk.Frame(self,style=BACK_CONTENT)
        self.FrameSearchOptions.place(relheight=0.2,relwidth=0.99,x=1.5,y=0)
        self.ScrollCanvaClass = ScrollCanva(self)
        self.SearchTaskClass = Searchtask(self.FrameSearchOptions,self.ScrollCanvaClass,self)

        #BOTON DE TAREAS URGENTES
        ttk.Button(self.FrameSearchOptions,text="Urgent Tasks",command=self.UrgentTask_Screen).place(relheight=0.2,width=90,x=320,y=8)


    #------------------------------VER TAREAS QUE LA FECHA DE ENTREGA ESTRE ENTRE EL DIA ACTUAL A CUATRO DIAS MAS-------------------
    def UrgentTask_Screen(self):
        global TaskClass,TaskListUser
        CleanFrameOptions = ttk.Frame(self.FrameSearchOptions,style=BACK_CONTENT)
        CleanFrameOptions.place(relheight=0.3,relwidth=1,y=40,x=0)
        CleanFrameOptions.tkraise()
        CleanFrameContent = ttk.Frame(self.ScrollCanvaClass.scrollable_frame,style=BACK_CONTENT)
        CleanFrameContent.place(relheight=1,relwidth=1)
        CleanFrameContent.tkraise()
        TaskClass.urgent_task(self.SearchTaskClass.SectionValue.get())
        self.SearchTaskClass.SeeTask()


#-----------------------------------------------------------------------PANTALLA DE AGREGAR TAREAS------------------------------------------------------------
class Addtask(ttk.Frame):
    global DataFileClass
    def __init__(self,parent,root,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        from constants.style import MainFrame_BackGround
        self.pack()
        self.config(style=BACK_CONTENT)
        self.propagate(0)

        #VARIABLES QUE UTILIZO
        # self.FrameAddTask = None
        # self.TaskNameValue = None
        # self.DescriptionEntry = None
        # self.DeliveryDateDayValue = None
        # self.DeliveryDateMonthValue = None
        # self.MonthOptionEntry = None
        # self.DayOptionEntry = None
        # self.DeliveryDateValue = None
        # self.AdressDateValue = None
        # self.NametaskEntry = None
        # self.SectionOptionEntry = None
        # self.FrameCondition = None


        #FRAME DONDE SE MUESTRA TODA LA INFORMACION
        self.FrameAddTask = ttk.Frame(self,style=BACK_CONTENT)
        self.FrameAddTask.pack(padx=20,pady=20,expand=True,fill=BOTH)

        #VALORES DE LA TAREA QUE VA A SER AGREGADA
        self.TaskNameValue = StringVar()
        self.DeliveryDateDayValue = StringVar()
        self.DeliveryDateMonthValue = StringVar()
        self.DeliveryDateValue = None
        self.AdressDateValue = dt.date.today()

#--------------------------------------TaskName------------------------------------------------------------------------
        ttk.Label(self.FrameAddTask,text="Task Name: ",style=BACKLABEL_CONTENT,padding=(0,0,0,5),anchor=NE).grid(row=0,column=0)
        self.NametaskEntry = ttk.Entry(self.FrameAddTask,justify=CENTER,textvariable=self.TaskNameValue)
        self.NametaskEntry.place(x=120,y=1)
        self.NametaskEntry.focus()
#--------------------------------------Descripcion---------------------------------------------------------------------        
        ttk.Label(self.FrameAddTask,text="Description: ",style=BACKLABEL_CONTENT,padding=(0,0,0,5),).grid(row=1,column=0,)
        self.DescriptionEntry = ScrolledText(self.FrameAddTask,width=15,height=5,)
        self.DescriptionEntry.grid(row=1,column=1,pady=10,padx=5)
#--------------------------------------Delivery Date-------------------------------------------------------------------
        ttk.Label(self.FrameAddTask,text="Delivery Date: ",style=BACKLABEL_CONTENT,padding=(10,0,0,5),).grid(row=2,column=0)
        self.MonthOptionEntry = ttk.OptionMenu(self.FrameAddTask,self.DeliveryDateMonthValue,*OPTION_MONTH)
        self.MonthOptionEntry.place(x=120,y=130)

        self.DayOptionEntry = ttk.OptionMenu(self.FrameAddTask,self.DeliveryDateDayValue,*OPTION_DAYJ)
        self.DayOptionEntry.place(y=130,x=220)
#---------------------------------------Section-----------------------------------------------------------------------
        ttk.Label(self.FrameAddTask,text="Choose Section:",style=BACKLABEL_CONTENT,padding=(15,10,0,5)).grid(row=3,column=0)
        DataFileClass.see_sections()
        self.SectionValue = StringVar(value="Sections")
        self.SectionOptionEntry = ttk.OptionMenu(self.FrameAddTask,self.SectionValue,*DataFileClass.SectionList)
        self.SectionOptionEntry.place(x=120,y=165)
#--------------------------------------Buttons-------------------------------------------------------------------------
        ttk.Button(self.FrameAddTask,text="Save",command= lambda:self.condition_task(True)).grid(row=4,column=1,pady=20)
        root.bind("<Return>", self.condition_task)
        ttk.Button(self.FrameAddTask,text="Reset",command= lambda: self.condition_task(False)).grid(row=4,column=0,pady=20)

#--------------------------------------Functions-----------------------------------------------------------------------
    def condition_task(self,est):
        frame = None

        #ESTO ME RESETA EL FRAME DONDE LE MUESTRO LA INFORMACION AL USARIO SI HAY ALGUN ERROR O SE AGREGO CORRACTAMENTE LA TAREA
        if est == False:
            self.FrameCondition = ttk.Frame(self,width=180,height=100,style=BACK_CONTENT)
            self.FrameCondition.place(x=290,y=80)
            self.FrameCondition.tkraise()
            self.TaskNameValue.set("")
            self.DeliveryDateDayValue.set("")
            self.DeliveryDateMonthValue.set("")
            self.DescriptionEntry.delete("0.0","end")

        #ESTO TIENE UN FRAME QUE MUESTRA EN PANTALLA SI HAY ALGUN ERROR O SE AGREGGO CORRECTAMENTE LA TAREA
        else:
            self.FrameCondition = ttk.Frame(self,style=BACK_CONTENT)
            self.FrameCondition.place(x=290,y=80,width=300)
            
            #AQUI VALIDO QUE NO ENTEN EN BLANCO LOS CAMPOS
            if (self.TaskNameValue.get()!="") and (self.DescriptionEntry.get("0.0","end")!="") and (self.DeliveryDateDayValue.get()!="") and (self.DeliveryDateMonthValue.get()!=""):
                
                #AQUI VALIDO QUE EL NOMBRE NO ESTE REPETIDO
                ValiTaskName = fc.Vali_TaskName(self.TaskNameValue.get())
                if ValiTaskName == False:
                    
                    #AQUI CREO LA FECHA DE ENTREGA Y LA VALIDO
                    self.DeliveryDateValue = fc.Vali_Date(self.DeliveryDateMonthValue.get(),self.DeliveryDateDayValue.get())
                    if self.DeliveryDateValue != False: 
                        
                        #AQUI ENVIO LA INFORMACION A GUARDARSE en el archivo database
                        global TaskClass
                        TaskClass.agg_task(self.TaskNameValue.get(),self.DescriptionEntry.get("0.0","end"),self.AdressDateValue,self.DeliveryDateValue,self.SectionValue.get(),None) 
                        #AQUI VALIDO SI LA TAREA SE PUDO AGREGAR 
                        if TaskClass.value_aggtask == True:
                            labe1 = ttk.Label(self.FrameCondition,text="Task Added!!!",font=("arial",14,"normal"),style=BACKLABEL_CONTENT,foreground="green").grid()
                        else:
                            labe1 = ttk.Label(self.FrameCondition,text="Task Not Added!!",font=("arial",14,"normal"),style=BACKLABEL_CONTENT,foreground="red").grid()
                    
                    else:
                        ttk.Label(self.FrameCondition,text="Date incorrect",font=("arial",14,"normal"),style=BACKLABEL_CONTENT,foreground="red").grid()
                
                else:
                    ttk.Label(self.FrameCondition,text="Task Name in Use",font=("arial",14,"normal"),style=BACKLABEL_CONTENT,foreground="red").grid()

            else:
                labe1 = ttk.Label(self.FrameCondition,text="Fill the Inputs!!",font=("arial",14,"normal"),style=BACKLABEL_CONTENT,foreground="red").grid()        
            

    def press(self,event):
        ttk.Label(self,text="you press enter").pack()


#-----------------------------------------------------------------------PANTALLA PARA MODIFICAR TAREAS---------------------------------------------------------
class Modifytask(ttk.Frame):
    def __init__(self,parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        from constants.style import MainFrame_BackGround
        self.pack()
        self.config(style=BACK_CONTENT)
        self.propagate(0)

        #VARIABLES QUE UTILIZO
        # self.TaskNameValue = None
        # self.DeliveryDateDayValue = None
        # self.DeliveryDateMonthValue = None
        # self.DeliveryDateValue = None
        # self.AdressDateValue = None
        # self.IdValue = None
        # self.FrameOptions = None
        # self.TaskFrame = None
        # self.NametaskEntry = None
        # self.DescriptionEntry = None
        # self.MonthOptionEntry = None
        # self.DayoptionEntry = None
        # self.ScrollCanvaClass = None
        # self.SearchTaskclass = None

        self.FrameOptions = ttk.Frame(self,style=BACK_CONTENT)
        self.FrameOptions.place(relheight=0.2,relwidth=0.99,x=1.5,y=0)

        self.ScrollCanvaClass = ScrollCanva(self)
        #--------------------------------------------------OPTION BAR---------------------------------------------------------------
        self.SearchTaskclass = Searchtask(self.FrameOptions,self.ScrollCanvaClass,self)
    

    def modify_options(self,section):
        self.IdValue = StringVar()
        ttk.Label(self.FrameOptions,text="modify enter Id:",style=BACKLABEL_CONTENT).place(y=50,x=305)
        ttk.Entry(self.FrameOptions,textvariable=self.IdValue).place(y=50,x=400,width=20)
        ttk.Button(self.FrameOptions,text="Mod",command=self.modify_frame).place(y=50,x=425,width=40,height=22)

    def modify_frame(self,):
        global TaskClass
        if self.IdValue.get() != "":
            #LLAMADA A LA BASE DE DATOS
            TaskClass.see_taskID(self.SearchTaskclass.SectionValue.get(),int(self.IdValue.get()))
            #VALORES DE LA TAREA ANTES DE MODIFICAR
            try:
                self.TaskInformation = TaskClass.TaskListUser[int(self.IdValue.get())]
            except:
                self.TaskInformation = ["None","None","None","None"]

            self.TaskNameValue = StringVar(value=self.TaskInformation[0])
            self.DeliveryDateDayValue = StringVar(value=self.TaskInformation[3].day)
            self.DeliveryDateMonthValue = StringVar(value=self.TaskInformation[3].month)
            self.DeliveryDateValue = None

            if self.TaskInformation[3].day < 10:
                self.DeliveryDateDayValue = StringVar(value=str(f"0{self.TaskInformation[3].day}"))
            if self.TaskInformation[3].day < 10:
                self.DeliveryDateMonthValue = StringVar(value=str(f"0{self.TaskInformation[3].month}"))

            #_------------------------------------------------FRAME----------------------------------------------------------------
            self.TaskFrame = ttk.Frame(self,style=BACK_CONTENT)
            self.TaskFrame.place(relheight=1,relwidth=0.97,x=0,y=0)
            self.TaskFrame.tkraise()
            #--------------------------------------TaskName------------------------------------------------------------------------
            ttk.Label(self.TaskFrame,text="Task Name: ",style=BACKLABEL_CONTENT,padding=(0,0,0,5),anchor=NE).place(x=50,y=40)
            self.NametaskEntry = ttk.Entry(self.TaskFrame,justify=CENTER,textvariable=self.TaskNameValue,)
            self.NametaskEntry.place(x=150,y=40)
            self.NametaskEntry.focus()
            #--------------------------------------Descripcion---------------------------------------------------------------------        
            ttk.Label(self.TaskFrame,text="Description: ",style=BACKLABEL_CONTENT,padding=(0,0,0,5),).place(x=50,y=70)
            self.DescriptionEntry = ScrolledText(self.TaskFrame,width=15,height=5,)
            self.DescriptionEntry.place(x=150,y=70)
            self.DescriptionEntry.insert(INSERT,self.TaskInformation[1])
            #--------------------------------------Delivery Date-------------------------------------------------------------------
            ttk.Label(self.TaskFrame,text="Delivery Date:",style=BACKLABEL_CONTENT,padding=(10,0,0,5),).place(x=40,y=160)
            self.MonthOptionEntry = ttk.OptionMenu(self.TaskFrame,self.DeliveryDateMonthValue,*OPTION_MONTH)
            self.MonthOptionEntry.place(x=150,y=160)

            self.DayoptionEntry = ttk.OptionMenu(self.TaskFrame,self.DeliveryDateDayValue,*OPTION_DAYJ)
            self.DayoptionEntry.place(x=250,y=160)
            print(self.DeliveryDateMonthValue.get())
            #----------------------------------------------------Buttons---------------------------------------------------------------
            ttk.Button(self.TaskFrame,text="R",width=2,command=self.reset_modify_frame()).place(x=425,y=1)
            ttk.Button(self.TaskFrame,text="X",width=2,command=lambda:self.TaskFrame.destroy()).place(x=450,y=1)
            print(self.DeliveryDateValue)
            ttk.Button(self.TaskFrame,text="Modify",command=lambda:self.modify()).place(x=50,y=200)
        
    def modify(self):
        global TaskClass
        self.DeliveryDateValue = fc.Vali_Date(self.DeliveryDateMonthValue.get(),self.DeliveryDateDayValue.get())
        TaskClass.modify_task(int(self.IdValue.get()),self.TaskNameValue.get(),self.DescriptionEntry.get("0.0","end"),self.DeliveryDateValue,self.TaskInformation[4])
        
    def reset_modify_frame(self):
        pass


#-----------------------------------------------------------------------PANTALLA PARA BORRAR TAREAS------------------------------------------------------------
class Deletetask(ttk.Frame):
    def __init__(self,parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        from constants.style import MainFrame_BackGround
        self.pack()
        self.config(style=BACK_CONTENT)
        self.propagate(0)
    
    def SeeTask(self):
        pass


#-----------------------------------------------------------------------PANTALLA QUE ME PERMITE TENER UN SCROLLBAR PARA UN FRAME-------------------------------
class ScrollCanva():
    def __init__(self,parent):
        self.canvas = Canvas(parent,background="#bfbfbf")
        self.scrollbar = ttk.Scrollbar(parent,orient=VERTICAL,command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas,style=BACK_CONTENT)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e : self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0,0),window=self.scrollable_frame,anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.place(relheight=0.9,relwidth=1,x=0,y=80)
        self.scrollbar.pack(side=RIGHT,fill="y")
        self.scrollable_frame.propagate(0)
    

#-----------------------------------------------------------------------BUSCA Y MUESTRA TAREAS------------------------------------------------------------------
class Searchtask():
    global DataFileClass,TaskClass
    def __init__(self,parent,canva,master):

        #VARIABLES QUE UTILIZO
        # self.SectionValue = None
        # self.SearchOptionValue = None
        # self.SearchSectionEntry = None
        # self.FrameOptions = None
        # self.ScrollCanvaClass = None
        # self.SearchOptionFrame = None


        self.FrameOptions = parent
        #-----------Para escoger la seccion---------------------------------------------------------------------------------------------------------------
        DataFileClass.see_sections()
        self.SectionValue = StringVar()
        SectionList = ["All",]
        for task in DataFileClass.SectionList:
            SectionList.append(task)
        self.SearchSectionEntry = ttk.OptionMenu(self.FrameOptions,self.SectionValue,*SectionList)
        self.SearchSectionEntry.place(x=5,y=8)

        #---------------------------------------------------Para escoger el tipo de busqueda-------------------------------------------------------------
        ttk.Label(self.FrameOptions,text="Search By: ",style=BACKLABEL_CONTENT).place(relheight=0.2,relwidth=0.2,x=105,y=8)
        self.SearchOptionValue = StringVar()
        self.SearchOptionEntry = ttk.OptionMenu(self.FrameOptions,self.SearchOptionValue,*OPTION_SEARCHTASK)
        self.SearchOptionEntry.place(relheight=0.19,x=175,y=8)
        #al presionar boton Search se dirige a la funcion Search
        ttk.Button(self.FrameOptions,text="Search",command=lambda:self.Search()).place(relheight=0.19,width=50,x=255,y=8)
        #FRAME PRINCIPAL DE LA APLICACION CON UN SCROLLBAR
        self.ScrollCanvaClass = canva
        self.master = master

    def Search(self):
        if self.SearchOptionValue.get() == "Month":
            self.Month_Screen()
        elif self.SearchOptionValue.get() == "Date":
            self.Date_Screen()
        elif self.SearchOptionValue.get() == "Name":
            self.Name_Screen()
        try:
            self.master.modify_options(self.SectionValue.get())
        except:
            pass

    #--------------------------------------------BUSCAR POR MES-----------------------------------------------------    
    def Month_Screen(self):
        #Para Limpiar La Pantalla
        CleanFrameOptions = ttk.Frame(self.FrameOptions,style=BACK_CONTENT)
        CleanFrameOptions.place(relheight=0.3,relwidth=0,y=40,x=0)
        CleanFrameOptions.tkraise()
        CleanFrameContent = ttk.Frame(self.ScrollCanvaClass.scrollable_frame,style=BACK_CONTENT)
        CleanFrameContent.place(relheight=1,relwidth=0)
        CleanFrameContent.tkraise()

        self.SearchOptionFrame = ttk.Frame(self.FrameOptions,style=BACK_CONTENT)
        self.SearchOptionFrame.place(relheight=0.3,relwidth=1,y=45,x=10)
        tex = self.SearchOptionValue.get()
        self.month = StringVar()
        ttk.Label(self.SearchOptionFrame,text=f"{tex} :",style=BACKLABEL_CONTENT).grid(row=0,column=0)
        self.MonthOption = ttk.OptionMenu(self.SearchOptionFrame,self.month,*OPTION_MONTH)
        self.MonthOption.grid(row=0,column=1)
        ttk.Button(self.SearchOptionFrame,text="Search Month",command=lambda:self.select_Value("month")).grid(row=0,column=2,padx=10)

    #-----------------------------------------------------BUSCAR POR FECHA-------------------------------------------------------
    def Date_Screen(self):
        CleanFrameOptions = ttk.Frame(self.FrameOptions,style=BACK_CONTENT)
        CleanFrameOptions.place(relheight=0.3,relwidth=0,y=40,x=0)
        CleanFrameOptions.tkraise()
        CleanFrameContent = ttk.Frame(self.ScrollCanvaClass.scrollable_frame,style=BACK_CONTENT)
        CleanFrameContent.place(relheight=1,relwidth=0)
        CleanFrameContent.tkraise()

        self.SearchOptionFrame = ttk.Frame(self.FrameOptions,style=BACK_CONTENT)
        self.SearchOptionFrame.place(relheight=0.3,relwidth=1,y=45,x=10)
        tex = self.SearchOptionValue.get()
        self.month = StringVar()
        self.day = StringVar()
        ttk.Label(self.SearchOptionFrame,text=f"{tex} :",style=BACKLABEL_CONTENT).grid(row=0,column=0)
        self.MonthOption = ttk.OptionMenu(self.SearchOptionFrame,self.month,*OPTION_MONTH)
        self.MonthOption.grid(row=0,column=1,padx=5)
        self.DayOption = ttk.OptionMenu(self.SearchOptionFrame,self.day,*OPTION_DAYJ)
        self.DayOption.grid(row=0,column=2,padx=5)
        ttk.Button(self.SearchOptionFrame,text="Search Date",command=lambda:self.select_Value("date")).grid(row=0,column=3,padx=10)
    
    #----------------------------------------------------BUSCAR POR NOMBRE--------------------------------------------------------
    def Name_Screen(self):
        CleanFrameOptions = ttk.Frame(self.FrameOptions,style=BACK_CONTENT)
        CleanFrameOptions.place(relheight=0.3,relwidth=0,y=40,x=0)
        CleanFrameOptions.tkraise()
        CleanFrameContent = ttk.Frame(self.ScrollCanvaClass.scrollable_frame,style=BACK_CONTENT)
        CleanFrameContent.place(relheight=1,relwidth=0)
        CleanFrameContent.tkraise()

        self.SearchOptionFrame = ttk.Frame(self.FrameOptions,style=BACK_CONTENT)
        self.SearchOptionFrame.place(relheight=0.3,relwidth=1,y=45,x=10)
        self.name = StringVar()
        NameEntry = ttk.Label(self.SearchOptionFrame,text=f"{self.SearchOptionValue.get()} :",style=BACKLABEL_CONTENT)
        NameEntry.grid(row=0,column=0)
        NameEntry.focus()
        ttk.Entry(self.SearchOptionFrame,textvariable=self.name,).grid(row=0,column=1)
        ttk.Button(self.SearchOptionFrame,text="Search Name",command=lambda:self.select_Value("name")).grid(row=0,column=2,padx=10)

    #--------------------------------------------------Cargar las tareas del fichero-----------------------------------------------
    def select_Value(self,val):
        global TaskClass
        CleanFrameContent = ttk.Frame(self.ScrollCanvaClass.scrollable_frame,style=BACK_CONTENT)
        CleanFrameContent.place(relheight=1,relwidth=1)
        CleanFrameContent.tkraise()

        if val  == "month":
            month = fc.Vali_Month(self.month.get())
            if month != None:
                TaskClass.see_taskMonth(month,self.SectionValue.get())
        elif val == "date":
            date = fc.Vali_Date(self.month.get(),self.day.get())
            if date != False:
                TaskClass.see_taskDate(date,self.SectionValue.get())
        elif val == "name":
                TaskClass.see_taskName(self.name.get(),self.SectionValue.get())
        self.SeeTask()

    #--------------------------------------------------Ver Lista De Tareas----------------------------------------------------------
    def SeeTask(self):
        global TaskClass
        i = 0
        if TaskClass.TaskListUser != {}:
            for t in TaskClass.TaskListUser:
                task = TaskClass.TaskListUser[t]
                i = i+1
                self.TaskFrame = ttk.Frame(self.ScrollCanvaClass.scrollable_frame,relief=GROOVE,border=10)
                self.TaskFrame.grid(row=i+1,column=0,padx=23,pady=10)

                #-------------------------------------------------------id-Section---------------------------------------------------------------
                self.IdFrame = ttk.Frame(self.TaskFrame,width=300,height=30)
                self.IdFrame.grid(row=0,column=0)
                ttk.Label(self.IdFrame,text="Id:").place(relheight=0.5,relwidth=0.5,x=10,y=0)
                ttk.Label(self.IdFrame,text=t).place(relheight=0.5,relwidth=0.5,x=100,y=0)
                ttk.Label(self.IdFrame,text=task[4],font=("arial",10,"bold")).place(relheight=1,relwidth=0.5,x=190,y=0)

                #-----------------------------------------------------NombreTarea-----------------------------------------------------------------
                self.TaskNameFrame = ttk.Frame(self.TaskFrame,width=300,height=30)
                self.TaskNameFrame.grid(row=1,column=0)
                ttk.Label(self.TaskNameFrame,text="Task Name:").place(relheight=0.5,relwidth=0.5,x=10,y=0)
                ttk.Label(self.TaskNameFrame,text=task[0]).place(relheight=0.5,relwidth=0.5,x=100,y=0)

                #------------------------------------------------------Descripcion-----------------------------------------------------------
                self.DescriptionFrame = ttk.Frame(self.TaskFrame,width=300,height=150)
                self.DescriptionFrame.grid(row=2,column=0)
                ttk.Label(self.DescriptionFrame,text="Description: ").place(relheight=0.4,relwidth=0.5,x=10,y=0)
                des = task[1]
                ttk.Label(self.DescriptionFrame,text=f"{des[0:29]}\n{des[29:59]}\n{des[59:89]}\n{des[89:119]}\n{des[119:149]}\n{des[149:179]}\n{des[179:209]}").place(relheight=1,relwidth=1,x=100,y=7)

                #---------------------------------------------------------------fecha de agregado---------------------------------------------
                self.AddresDateFrame = ttk.Frame(self.TaskFrame,width=300,height=30)
                self.AddresDateFrame.grid(row=3,column=0)
                ttk.Label(self.AddresDateFrame,text="Adress Date: ").place(relheight=0.5,relwidth=0.5,x=10,y=0)
                ttk.Label(self.AddresDateFrame,text=task[2]).place(relheight=0.5,relwidth=0.5,x=100,y=0)

                #----------------------------------------------------------------fecha de entrega----------------------------------------------
                self.DeliveryDateFrame = ttk.Frame(self.TaskFrame,width=300,height=30)
                self.DeliveryDateFrame.grid(row=4,column=0)
                ttk.Label(self.DeliveryDateFrame,text="Delivery Date: ").place(relheight=0.5,relwidth=0.5,x=10,y=0)
                ttk.Label(self.DeliveryDateFrame,text=task[3]).place(relheight=0.5,relwidth=0.5,x=100,y=0)