import json
from tokenize import Name
import xml.etree.ElementTree as ET


class OwnerCantBeInteger(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            print('OwnerCantBeInteger, {0} '.format(self.message))
            return  'OwnerCantBeInteger, {0} '.format(self.message)

        else:
            print('Owner cant be integer')
            return  'Owner cant be integer'


class NothingToGet(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return  'NothingToGet, {0} '.format(self.message)
        else:
            return  'Nothing to get'

class SomeThingLayedUndefined(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'SomethingLayedUndefined, {0} '.format(self.message)
        else:
            return 'Something layed undefined'

class Vehicle:
    def __init__(self, Class="", RegistrationNumber=""):
        self.Class = Class
        self.RegistrationNumber = RegistrationNumber
    def GiveRegistrationNumber(self):
        return self.RegistrationNumber
def FromXml(FileName):
    try:
        tree = ET.parse(FileName)
    except Exception:
        print("Файл - хрень")
        raise Exception
    root = tree.getroot()
    Vehicles = {}
    i = 0
    for Veh in root:

        for elem in Veh:
            if elem.tag =="Class":
                Class = elem.text
            elif elem.tag == "RegistrationNumber":
                RegistrationNumber = elem.text
                Vehicles[i] = [Class,RegistrationNumber]
                i += 1
    return Vehicles



def ToXml(Vehicle,FileName):
    try:
        tree = ET.parse(FileName)
        Root = tree.getroot()
    except Exception:
        Root = ET.Element('Vehicles')
    myfile = open(FileName, "w")
    Data = ET.SubElement(Root,'Vehicle')
    Class = ET.SubElement(Data,'Class')
    RegNum = ET.SubElement(Data,'RegistrationNumber')
    Class.set('name','Class')
    RegNum.set('name','RegistrationNumber')
    Class.text = Vehicle.Class
    RegNum.text = Vehicle.RegistrationNumber
    mydata = ET.tostring(Root)
    mydata = mydata.decode('utf8')
    myfile.write(mydata)



class Accounter:
    def GetRegistrationNumber(self,Vehicle):
        self.RegistrationNumber = Vehicle.GiveRegistrationNumber()
    def GetInfo(self,Database):
        Database.GetContainer(self.RegistrationNumber)
        self.Price = Database.Price
        self.Owner = Database.Owner
    def GiveInfo(self):
        print(self.RegistrationNumber, self.Owner, self.Price)



class Container:
    def __init__(self,RegistrationNumber="",Owner="",Price=0):
        self.RegistrationNumber = RegistrationNumber
        self.Owner = Owner
        self.Price = Price
        self.NextContainer = None
    def FromJson(self,dict):
        self.RegistrationNumber = dict['RegistrationNumber']
        self.Owner = dict['Owner']
        self.Price = dict['Price']
        if dict['NextContainer'] is not None:
            self.NextContainer = Container("","",0).FromJson(dict['NextContainer'])
        return self



class Database:
    def __init__(self,Filename=" "):
        self.Head = None
        self.Price = 0
        self.Owner = ""

        if Filename == " ":
            return
        try:
            with open(Filename,"r") as ReadFile:
                Dict = json.loads(ReadFile.read())
                self.Price = Dict['Price']
                self.Owner = Dict['Owner']
                if Dict['Head'] is not None:
                    self.Head = Container("","",0).FromJson(Dict['Head'])
        except Exception:
            print("Фигня ваш файл, ничего прочитать невозможно")
    def IsHere(self,RegistrationNumber):
        LastContainer = self.Head
        while (LastContainer):
            if RegistrationNumber == LastContainer.RegistrationNumber:
                return True
            else:
                LastContainer = LastContainer.NextContainer
            return False
    def AddContainer(self,RegistrationNumber,Owner,Price):
        NewContainer = Container(RegistrationNumber,Owner,Price)
        if self.Head is None:
            self.Head = NewContainer
            return
        LastContainer = self.Head
        while (LastContainer.NextContainer):
            if LastContainer.RegistrationNumber == NewContainer.RegistrationNumber:
                print("Обнаружено совпадение номеров, добавление в базу данных остановленно")
                return
            LastContainer = LastContainer.NextContainer
        if LastContainer.RegistrationNumber == NewContainer.RegistrationNumber:
            print("Обнаружено совпадение номеров, добавление в базу данных остановленно")
            return
        LastContainer.NextContainer = NewContainer
    def GetContainer(self,RegistrationNumber):
        
        CurrentContainer = self.Head
        if CurrentContainer == None:
            return False
        while (CurrentContainer.RegistrationNumber != RegistrationNumber):
            if CurrentContainer.NextContainer == None:
                
                return False
            else:
                CurrentContainer = CurrentContainer.NextContainer
        self.Owner = CurrentContainer.Owner
        self.Price = CurrentContainer.Price
        return True

    def ToJson(self,FileName):
        try:
            with open(FileName, "w") as write_file:
                json.dump(self,write_file,default=lambda o: o.__dict__, indent=4)
        except Exception:
            print("Чёт ваш файл хрень полная или его вообще нету")
            



UnparsedInput = []
if (str(input("Желаете подгрузить базу данных из файла .json? Y/N\n")) == 'Y'):
    File = str(input("Введите название файла"))
    Cars = Database(File)
else:
    Cars = Database()
print("Введите данные для заполнения базы в формате: НомераМашины Владелец Цена")
while True:
    UnparsedInput = input().split()
    try:
        InputRegNum = str(UnparsedInput[0])
        InputOwner = str(UnparsedInput[1])
        InputPrice = int(UnparsedInput[2])
    except Exception:
        print("Если вы ошиблись в вводе данных и хотите продолжить, введите 'continue', если вы хотите закончить ввод, нажмите Enter")
        if (str(input()) != 'continue'):
            break
    else:
        try:
            int(InputOwner)
        except:
            pass
        else:
            raise OwnerCantBeInteger()


        try:
            Cars.AddContainer(InputRegNum, InputOwner, InputPrice)
        except SomeThingLayedUndefined(NameError):
            pass
CarsOnTheRoad = {}
Car2 = Vehicle("Semerka","TestMashine")
if str(input("Желаете подгрузить данные об автомобиле с xml файла Y/N\n")) == 'Y':
    File = str(input("Введите название файла\n"))
    AllCars = FromXml(File)

    for it in AllCars:
        CarsOnTheRoad[it] = Vehicle(AllCars[it][0],AllCars[it][1])
else:
    i = 0
    while str(UnparsedInput) != 'N':
        try:
            UnparsedInput = list(map(str,input("Введите данные машины в формате: Класс НомераМашины\n").split()))

        except Exception:
            print("Неправильный ввод")
        finally:
            print("Введите N для окончания ввода или продолжите его")
        try:
            InputClass = str(UnparsedInput[0])
            InputRegNum = str(UnparsedInput[1])
            CarsOnTheRoad[i] = Vehicle(InputClass, InputRegNum)
            i += 1
        except Exception:
            print("Если вы ошиблись в вводе данных и хотите продолжить, введите 'continue', если вы хотите закончить ввод, нажмите Enter")
            if (str(input()) != 'continue'):
                break
Police = Accounter()
Police.GetRegistrationNumber(CarsOnTheRoad[0])
Police.GetInfo(Cars)
Police.GiveInfo()
if str(input("Желаете загрузить базу данных в файл .json? Y/N\n")) == 'Y':
    File = str(input("Введите название файла"))
    Cars.ToJson(File)
if str(input("Желаете сохранить данные об автомобиле в xml файл Y/N\n")) == 'Y':
    File = str(input("Введите название файла\n"))
    for i in CarsOnTheRoad:
        ToXml(CarsOnTheRoad[i],File)





