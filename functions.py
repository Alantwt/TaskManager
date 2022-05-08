
import datetime as dt
import database as dtb

#VALIDA QUE LA FECHA DE ENTREGA SEA CORRECTA
def Vali_Date(monthr,day):
    year = dt.date.today().year
    month = Vali_Month(monthr)
    try:
        if int(month) == int(dt.date.today().month) and int(day) >= int(dt.date.today().day):
            year,month,day = str(year),str(month),str(day)
            print(year,month,day)
            date = dt.date.fromisoformat(f"{year}-{month}-{day}")
        elif int(month) > int(dt.date.today().month):
            year,month,day = str(year),str(month),str(day)
            print(year,month,day)
            date = dt.date.fromisoformat(f"{year}-{month}-{day}")
        else:
            date = False
    except:
        date = False
    return date

#PASA EL MES ESCOGIDO A NUMERO PARA PODER AGREGAR A LA FECHA
def Vali_Month(month):
    if "1" == month or month == "JANUARY":
        return "01"
    elif "2" == month or month == "FEBRUARY":
        return "02"
    elif "3" == month or month == "MARCH":
        return "03"
    elif "4" == month or month == "APRIL":
        return "04"
    elif "5" == month or month == "MAY":
        return "05"
    elif "6" == month or month == "JUNE":
        return "06"
    elif "7" == month or month == "JULY":
        return "07"
    elif "8" == month or month == "AUGUST":
        return "08"
    elif "9" == month or month == "SEPTEMBER":
        return "09"
    elif "10" == month or month == "OCTOBER":
        return "10"
    elif "11" == month or month == "NOVEMBER":
        return "11"
    elif "12" == month or month == "DECEMBER":
        return "12"
    else:
        return month

#VALIDA QUE EL NOMBRE DE LA TAREA NO ESTE EN USO YA
def Vali_TaskName(taskname):
    task = dtb.Tasks()
    if len(dtb.TaskList) != 0:
        for k in dtb.TaskList:
            if taskname == k:
                return True
            else:
                return False
    else:
        return False
    