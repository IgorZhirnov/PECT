'''Данная программа позволяет расчитать температуру на ЭРИ 
   в зависимости от температуры нагретой зоны, где установлен
   данный ЭРИ и температуры среды, окружающей нагретую зону
   
   Методика расчета и эмпирические коэффициенты для расчета 
   взяты из книги: Роткоп Л.Л., Спокаойный Ю.Е.
   Обеспечение тепловых режимов при конструировании 
   радиоэлектронной аппаратуры. М., "Сов. радио", 1976.'''

from scipy.interpolate import interp1d
import numpy as np
from tkinter import *
#Ввод данных по методике расчета
VEL = np.linspace(0, 70, 15)
P999 = np.array([30., 35., 41., 48., 57., 67., 78., 90., 102., 114., 129., 145., 145., 145., 145.])
P995 = np.array([25., 30., 35., 42.5, 50., 57., 66., 76., 86., 97., 109., 122., 135., 150., 150.])
P099 = np.array([23.5, 27., 33., 39., 46., 53.5, 62., 70., 80., 88., 100., 112., 123., 135., 135.])
P098 = np.array([23., 26., 32., 37., 43., 50., 57., 66., 74., 83., 92., 103., 113., 124., 135.])
P097 = np.array([22., 25., 30., 35., 42., 48., 55., 63., 70., 78., 87., 96., 107., 117., 128.])
P096 = np.array([21., 24., 28., 34., 40., 46., 52.5, 60., 67., 75., 84., 92.5, 102., 112., 123.])
P095 = np.array([19., 23., 27., 32.5, 38., 44.5, 50.5, 57.5, 64., 72., 80., 87.5, 96.5, 105., 115.])

class Application(Frame):
    def __init__(self, master):
        super(Application, self).__init__(master)
        self.grid()
        self.create_widgets()
    
    def create_widgets(self):
        #Метка с инструкцией к программе
        '''Label(self,
              text = 'Данная программа с заданной вероятность позволяет определить ' \
              'температуру на ЭРИ в зависимости от температуры воздуха, окружающего ' \
              'нагретую зону, и температуры нагретой зоны при охлаждении естественной ' \
              'конвекцией.',
              ).grid(row = 0, column = 0, columnspan = 3, sticky = W)'''
        #Метка и поле ввода для температуры окуражуещей среды
        Label(self,
              text = 'Введите температуру среды (в цельсиях): '
              ).grid(row = 1, column = 0, sticky = W)
        self.env_temp = Entry(self)
        self.env_temp.grid(row = 1, column = 1, sticky = W)
        #Метка для ввода температуры нагретой зоны (печатной платы)
        Label(self,
              text = 'Введите температуру нагретой зоны (в цельсиях): '
              ).grid(row = 2, column = 0, sticky = W)
        self.zone_temp = Entry(self)
        self.zone_temp.grid(row = 2, column = 1, sticky = W)
        #Метка для группы флажков с переключателями вероятностей
        Label(self,
              text = 'Выберите вероятность расчета'
              ).grid(row = 3, column = 0, sticky = W)
        #Переменная содержащая вероятность расчета
        self.conf_lvl = StringVar()
        self.conf_lvl.set(None)
        #Переключатель вероятностей расчета
        conf_lvls = ['99,9 %', '99,5 %', '99 %', '98 %', '97 %', '96 %', '95 %']
        conf_variables = [P999, P995, P099, P098, P097, P096, P095]
        row = 4
        conf_variable = 0
        for lvls in conf_lvls:
            Radiobutton(self,
                        text = lvls,
                        variable = self.conf_lvl,
                        value = conf_variables[conf_variable]
                        ).grid(row = row, column = 0, sticky = W)
            conf_variable += 1
            row += 1
        #Кнопка расчета
        Button(self,
               text = 'Расчитать',
               command = self.calculate
               ).grid(row = 12, column = 0, sticky = W)
        #Вывод информации
        self.calculate_text = Text(self, width = 75, height = 10, wrap = WORD)
        self.calculate_text.grid(row = 13, column = 0, columnspan = 5)
    
    def calculate(self):
        #Получение данных от пользователя
        environment_temperature = float(self.env_temp.get())
        zone_temperature = float(self.zone_temp.get())
        confidence_interval = self.conf_lvl.get()
        #Определение функции по эмпирическим данным
        f = interp1d(VEL, confidence_interval, kind = 'cubic')
        #Расчет перегрева нагретой зоны
        zone_temp_diff = zone_temperature - environment_temperature
        #Расчет перегрева на элементе
        element_temp_diff = f(zone_temp_diff)
        #Расчет температуры элемента
        element_temp = zone_temperature + element_temp_diff
        #Создание текста ответа
        calculation_text = 'Температура на элементе равна: ' + str(element_temp)
        #Вывод текста ответа на экран
        self.calculate_text.delete(0.0, END)
        self.calculate_text.insert(0.0, calculation_text)

#Основная часть программы
root = Tk()
root.title('PECT')
app = Application(root)
root.mainloop()