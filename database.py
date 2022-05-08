
from asyncio import Task
import datetime as dt
import os
import pickle
from typing import List, final

#lista de secciones para mostrar al usuario
SectionsList = []
#Diccionario donde se guardaran las tareas
TaskList = {}

class Datafile():
    def __init__(self):
        self.valueF = False          #Variable para validar  si un archivo esta creado o no
        self.file = None             #Variable para abrir x archivo de almacenamiento de tareas
        self.path = None             #Variable que tendra el path para verificar si el archivo esta creado
        self.DelCrea_Section = False #Variable que uso para almacenar un valor booleano que confirma si se creo o se borro una seccion
        self.SectionList = []        #variable que uso para almacenar los datos de los archivos binaios

        self.default()
        
    #----------------------------------------------------Crea un archivo defauld-----------------------------------------------------
    def default(self):
        self.path = "C:\TaskManager\TKManager\Data\DefaultData"
        self.validate()
        if self.valueF == False:
            self.file = open("C:\TaskManager\TKManager\Data\DefaultData","wb")
            self.file.close()
            self.sections_list("DefaultData")

    #----------------------------------------------------Crea los archivos de las diferentes secciones-------------------------------
    def create_sections(self,section):
        self.DelCrea_Section = False
        self.path = f"C:\TaskManager\TKManager\Data\{section}"
        self.validate()
        if self.valueF == False and section != "":
            self.file = open(f"C:\TaskManager\TKManager\Data\{section}","wb")
            self.file.close()
            self.sections_list(section)
            self.DelCrea_Section = True

    #----------------------------------------------------Delete Section-------------------------------------------------------------
    def delete_sections(self,section):
        if section != "DefaultData":
            try:
                os.remove(f"C:\TaskManager\TKManager\Data\{section}")
                self.DelCrea_Section = True
                self.see_sections()
                if section in self.SectionList:
                    self.SectionList.remove(section)
                    self.sections_list(self.SectionList)
            except:
                self.DelCrea_Section = False
    #------------------------------------------------------Agregar las secciones a un fichero binario--------------------------------
    def sections_list(self,section):
        self.path = f"C:\TaskManager\TKManager\Data\Sections"
        self.validate()
        if self.valueF == False:
            self.file  = open("C:\TaskManager\TKManager\Data\Sections","wb")
            pickle.dump(["DefaultData",],self.file)
            self.file.close()
        else:
            self.file = open("C:\TaskManager\TKManager\Data\Sections","rb")
            self.file.seek(0)
            try:
                if type(section)!=type([]):
                    self.SectionList = pickle.load(self.file)
                    self.SectionList.append(section)

                self.file = open("C:\TaskManager\TKManager\Data\Sections","wb")
                pickle.dump(self.SectionList,self.file)
            except:
                pass
            finally:
                self.file.close()
        self.SectionList = SectionsList 
    #--------------------------------------------------------Ver Lista de Sections----------------------------------------------------
    def see_sections(self):
        self.file = open("C:\TaskManager\TKManager\Data\Sections","rb")
        try: 
            self.SectionList = pickle.load(self.file)
        except:
            self.SectionList = []
        finally:
            self.file.close()

    #-----------------------------------------------------Validar si un archivo esta creado-------------------------------------------
    def validate(self):
        self.valueF = os.path.exists(self.path)

#Datafile()

#ESQUEMA DE COMO SE GUARDAN LAS TAREAS(SE GUARDAN EN UN DICCIONARIO)
#{ID TAREA : [NOMBRETAREA,DESCRIPCION, FECHA DE AGREGADO, FECHA DE ENTREGA, SECTION]}

class Tasks():
    def __init__(self):
        self.id = None
        self.taskname = None
        self.description = None
        self.adate = None
        self.ddate = None
        self.Fdata = None
        self.value_aggtask = False
        self.TaskListUser = {}
        self.section = None
        self.auto_delete()
    
    #RECIVE LOS VALORES DE LA TAREA
    def agg_task(self,taskname,description,adate,ddate,section,id):
        global TaskList
        self.section = section
        self.get_()
        if id == None:
            self.create_id()
        else:
            self.id = id
        self.taskname = taskname
        self.description = description
        self.adate = adate
        self.ddate = ddate
        self.section = section

        if len(TaskList) > 0:
            for t in TaskList:
                if self.taskname == str(t):
                    self.value_aggtask = False
                    break
                else:
                    self.value_aggtask = True
        else:
            self.value_aggtask = True

        if self.value_aggtask == True:
            try:
                self.get_()
                self.agg_()
                self.value_aggtask = True
            except: 
                self.value_aggtask = False

    def modify_task(self,id,taskname,description,ddate,section):
        global TaskList
        self.section = section
        self.get_()
        for t in TaskList:
            if id == t:
                task = TaskList[t]
                self.agg_task(taskname,description,task[2],ddate,section,id)

                      

    #PERMITE VER LAS TAREAS POR MES, RECIBE EL VALOR DEL MES
    def see_taskMonth(self,month,section):
        global TaskList,clssDF
        self.TaskListUser = {}
        if section == "All" and section != "Sections":
            clssDF.see_sections()
            for sec in  clssDF.SectionList:
                self.section = sec
                self.get_()
                if len(TaskList) != 0:   
                    for t in TaskList:
                        task = TaskList[t]
                        if task[3].month == int(month):
                            self.TaskListUser[t] = TaskList[t]
        elif section != "All" and section != "Sections":
            self.section = section
            self.get_()
            if len(TaskList) != 0:   
                for t in TaskList:
                    task = TaskList[t]
                    if task[3].month == int(month):
                        self.TaskListUser[t] = TaskList[t]

    #PERMIE VER LAS TAREAS POR FECHA, RECIBE EL VALOR DE LA FECHA
    def see_taskDate(self,date,section):
        global TaskList,clssDF
        self.TaskListUser = {}
        if section == "All" and section != "Sections":
            clssDF.see_sections()
            for sec in clssDF.SectionList:
                self.section = sec
                self.get_()
                if len(TaskList) != 0:
                    for t  in TaskList:
                        task = TaskList[t]
                        if task[2] == date:
                            self.TaskListUser[t] = TaskList[t] 
        elif section != "All" and section != "Sections":
            self.section = section
            self.get_()
            if len(TaskList) != 0:
                for t  in TaskList:
                    task = TaskList[t]
                    if task[2] == date:
                        self.TaskListUser[t] = TaskList[t] 


    #PERMITE VER LAS TAREAS POR NOMBRE
    def see_taskName(self,name,section):
        global TaskList
        self.TaskListUser = {}
        self.section = section
        self.get_()
        if len(TaskList) != 0:
            for t  in TaskList:
                task = t
                if task[0:len(name)] == name:
                    self.TaskListUser[t] = TaskList[t] 

    #PERMITE VER LAS TAREAS POR ID
    def see_taskID(self,section,id):
        global TaskList, clssDF
        if section == "All" or section == "Sections":
            clssDF.see_sections()
            for sec in clssDF.SectionList:
                self.section = sec
                self.get_()
                if len(TaskList) != 0:
                    for t  in TaskList:
                        if id == t:
                            self.TaskListUser[t] = TaskList[t]
        elif section != "All" and section != "Sections":
            self.section = section
            self.get_()
            if len(TaskList) != 0:
                for t in TaskList:
                    if int(id) == t:
                        self.TaskListUser[t] = TaskList[t]

    #PERMITE VER LAS TAREAS URGENTES
    def urgent_task(self,section):
        global TaskList,clssDF
        clssDF.see_sections()
        self.TaskListUser = {}
        if section == "All" or section == "Sections":
            for sec in clssDF.SectionList:
                self.section = sec
                self.get_()
                if len(TaskList) != 0:
                    date = dt.date.today()
                    datef = None
                    m = date.month
                    d = date.day+3
                    b = True
                    while b == True:
                        if int(d) < 10:
                            d = f"0{d}"
                        if int(m) < 10:
                            m = f"0{m}"
                        try:
                            datef = dt.date.fromisoformat(f"{date.year}-{m}-{d}")
                            b = False
                        except:
                            m= int(m)
                            m = m+1
                            d = 3
                    for t in TaskList:
                        task = TaskList[t]

                        if int(datef.month) > int(date.month):
                            if int(task[3].day) < int(datef.day) or 25 <= int(task[3].day) <= 31:
                                self.TaskListUser[t] = TaskList[t]
                                print(self.TaskListUser)
                        elif int(datef.month) == int(date.month):
                            if int(date.day) < int(task[3].day) < int(datef.day):
                                self.TaskListUser[t] = TaskList[t]
                                print(self.TaskListUser)

                
        elif section != "All" and section != "Sections":
            self.section = section
            self.get_()
            if len(TaskList) != 0:
                date = dt.date.today()
                datef = None
                m = date.month
                d = date.day+3
                b = True
                while b == True:
                    if int(d) < 10:
                        d = f"0{d}"
                    if int(m) < 10:
                        m = f"0{m}"
                    try:
                        datef = dt.date.fromisoformat(f"{date.year}-{m}-{d}")
                        b = False
                    except:
                        m= int(m)
                        m = m+1
                        d = 3
                for t in TaskList:
                    task = TaskList[t]

                    if int(datef.month) > int(date.month):
                        if int(task[3].day) <= int(datef.day) or 25 <= int(task[3].day) <= 31:
                            self.TaskListUser[t] = TaskList[t]
                            print(self.TaskListUser)
                    elif int(datef.month) == int(date.month):
                        if int(date.day) < int(task[3].day) < int(datef.day):
                            self.TaskListUser[t] = TaskList[t]
                            print(self.TaskListUser)

    #BORRA AUTOMATICAMENTE LAS TAREAS QUE YA HAYA PASADO SI FECHA DE ENTREGA CUANDO SE INICIA EL PROGRAMA
    def auto_delete(self):
        global TaskList,clssDF
        TaskList = {}
        day,month,year = int(dt.date.today().day),int(dt.date.today().month),int(dt.date.today().year)
        clssDF.see_sections()
        for sec in clssDF.SectionList:
            self.section = sec
            self.get_()
            try:
                if len(TaskList) > 0:
                    for t in TaskList:
                        task = TaskList[t]  
                        if year >= task[3].year:
                            if month > task[3].month:
                                self.del_task(t)
                            elif month == task[3].month:
                                if day > task[3].day:
                                    self.del_task(t)
            except:
                pass


    #PERMITE BORRAR TAREAS INTRODUCIENDO LA KEY DEL DICCIONARIO QUE ES EL NOMBRE 
    def del_task(self,id):
        global TaskList
        try:
            del TaskList[id]
        except:
            print("task not deleted")
        self.Fdata = open(f"C:\TaskManager\TKManager\Data\{self.section}","wb")
        pickle.dump(TaskList,self.Fdata)
        self.Fdata.close()

    #OBTIENE TODAS LAS TAREAS DEL FICHERO 
    def get_(self):
        global TaskList
        self.Fdata = open(f"C:\TaskManager\TKManager\Data\{self.section}","rb")
        self.Fdata.seek(0)
        try:
            TaskList = pickle.load(self.Fdata)
        except:
            TaskList = {}
        finally:
            self.Fdata.close()
        
    #AGREGA DIRECTAMENTE TAREAS AL FICHERO 
    def agg_(self):
        global TaskList
        TaskContent =[self.taskname,self.description,self.adate,self.ddate,self.section]
        TaskList[self.id]=TaskContent
        self.Fdata = open(f"C:\TaskManager\TKManager\Data\{self.section}","wb")
        pickle.dump(TaskList,self.Fdata)
        self.Fdata.close()
        print(TaskList)

    def create_id(self):
        global TaskList,clssDF
        IdTask = []
        idMayor = 0
        clssDF.see_sections()
        for section in clssDF.SectionList:
            try:
                self.section = section
                self.get_()
                for id in TaskList:
                    IdTask.append(int(id))
            except:
                pass
        if len(IdTask)>0:
            for id in IdTask:
                if id > idMayor:
                    idMayor = id
            self.id = int(idMayor)+1
        else:
            self.id = 1

clssDF = Datafile()
