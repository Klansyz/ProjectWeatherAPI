import requests

from tkinter import *
from tkinter import ttk
import time
from os import *
import locale
import tkinter_page as tkp
from tkinter import messagebox
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config
import pytz
from pyowm.commons.exceptions import NotFoundError  # Импорт ошибки как NotFoundError
from pyowm.commons.exceptions import UnauthorizedError
from datetime import datetime, date
from babel.dates import format_date, format_datetime, format_time
from geopy.geocoders import Nominatim  # Находит долготу и широту в приложении
from suntime import Sun, SunTimeException  # Нахождение Заката и рассвета
from PIL import Image, ImageTk
from random import randint
from math import *

session = requests.Session()
session.verify = False

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


window = Tk()

window.resizable(width=False, height=False)
window.title("ПОГОДА ОНЛАЙН")
window.geometry("1100x600")

# Создаем Время
seconds = time.time()
local_time = time.localtime(seconds)
string_time = time.strftime("%d %B %Y  %H:%M:%S", local_time)

"""
def time_Litva():
    tz_place = pytz.timezone(f'Europe/Vilnius') #Europe/Vilnius
    datetime_place = datetime.now(tz_place) 
    string_time = datetime_place.strftime("%d %B,%Y %H:%M:%S")        
    timer_London["text"] = string_time  

    timer_London.after(200, time_Litva)

def time_Helsinki():
    tz_place = pytz.timezone(f'Europe/Helsinki') #Europe/Helsinki
    datetime_place = datetime.now(tz_place) 
    string_time = datetime_place.strftime("%d %B,%Y %H:%M:%S")        
    timer_London["text"] = string_time

    timer_London.after(200, time_Helsinki)

def time_China():
    tz_place = pytz.timezone(f'Asia/Shanghai') #Asia/Shanghai 
    datetime_place = datetime.now(tz_place) 
    string_time = datetime_place.strftime("%d %B,%Y %H:%M:%S")        
    timer_London["text"] = string_time

    timer_London.after(200, time_China)

"""


def time_Moscow():
    seconds = time.time()
    local_time = time.localtime(seconds)
    string_time = time.strftime("%d %B %Y %H:%M:%S", local_time)
    clock["text"] = string_time
    clock.after(200, time_Moscow)


"""
def time_London():
    tz_place = pytz.timezone(f'Europe/London') 
    datetime_place = datetime.now(tz_place) 
    string_time = datetime_place.strftime("%d %B,%Y %H:%M:%S")    
    timer_London["text"] = string_time

    timer_London.after(200, time_London)


def time_France():
    tz_place = pytz.timezone(f'Europe/Paris') 
    datetime_place = datetime.now(tz_place) 
    string_time = datetime_place.strftime("%d %B,%Y %H:%M:%S")    

    timer_France["text"] = string_time

    timer_France.after(200, time_France)      
"""
"""
def time_Poland():
    tz_place = pytz.timezone(f'Europe/Warsaw') 
    datetime_place = datetime.now(tz_place) 
    string_time = datetime_place.strftime("%d %B,%Y %H:%M:%S") 

    timer_Poland["text"] = string_time

    timer_Poland.after(200, time_Poland)
"""

"""
tz_place = pytz.timezone(f'Europe/{place}') 
datetime_place = datetime.now(tz_place) 
clock_2 = datetime_place.strftime("%d %B,%Y  %H:%M:%S")
clock["text"] = clock_2
"""


# Получение Api
def apply_Api():
    APi = insert_Api.get()
    if len(APi) == 32:
        label_Api["fg"] = "#32CD32"
        return APi
    else:
        label_Api["fg"] = "#FF0000"
        messagebox.showerror("Error0x06", "Символов должно быть 32!")


# Информация о погоде
def statistic_main(place):
    config_dict = get_default_config()
    config_dict['language'] = 'ru'
    owm = OWM(apply_Api(), config_dict)  # "c46d676a6a93f1484be8cb1014377db0"
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(place)
    w = observation.weather

    # Добавление id Города/Страны class Location
    location_id = observation.location

    # Рабочий каталог для geolacator
    work_catalog = path.realpath(__file__)  # Получает рабочий путь с файлом
    filename = path.basename(work_catalog)  # Имя файла

    '''
    work_cat = os.getcwd() получает рабочий путь без файла
    print(os.listdir(work_cat)) Список файлов в каталоге
    '''

    # Закат и Рассвет
    geolocator = Nominatim(user_agent=filename)
    location = geolocator.geocode(place)
    long = location.longitude  # Долгота
    lat = location.latitude  # Ширина

    # Вызов погоды feels_like
    one_call_temp = mgr.one_call(lat=lat, lon=long, exclude='minutely', units='metric')
    feels_like_temp = one_call_temp.current.temperature()["feels_like"]
    temp_describe["text"] = f"Ощущается как: {ceil(feels_like_temp)}°C"

    # Вывод Закат и Рассвет
    sun = Sun(lat, long)

    today_sr = sun.get_sunrise_time()
    today_ss = sun.get_sunset_time()

    get_sunrise["text"] = f"{today_sr.strftime('%H:%M')} ч."
    get_sunset["text"] = f"{today_ss.strftime('%H:%M')} ч."

    label_title_in["text"] = f"Город/Страна: {place}."

    degree = w.wind()["deg"]
    visibility = w.visibility_distance // 1000
    wind = w.wind()["speed"]
    temp = w.temperature('celsius')["temp"]
    humidity = w.humidity
    status = w.detailed_status
    pressure = w.pressure["press"]

    id_number_city["text"] = f"id:{location_id.id}"

    visibility_describe["text"] = str(ceil(visibility)) + "км"

    temp_now["text"] = str(ceil(temp)) + "°C"

    # wind_now["text"] = str(ceil(wind)) + " м/с"

    humidity_now["text"] = str(humidity) + "%"

    clouds_describe["text"] = str(w.clouds) + "%"

    status_describe["text"] = str(status) + "."

    status_now["text"] = "Сейчас"

    get_pressure["text"] = "{0} мм рт. столба".format(ceil(pressure * 0.75 - 12))  # Конвертируем из гПа в
    # мм рт столба

    if 0 <= wind <= 5.99:
        wind_describe["text"] = "Слабый"
    elif 6 <= wind <= 14.99:
        wind_describe["text"] = "Умеренный"
    elif 15 <= wind <= 24.99:
        wind_describe["text"] = "Сильный"
    elif 25 <= wind <= 32.99:
        wind_describe["text"] = "Очень Сильный"
    else:
        wind_describe["text"] = "Ураганный"

    if 0 <= degree <= 44:
        wind_now["text"] = str(ceil(wind)) + " м/с,С"
    elif 45 <= degree <= 89:
        wind_now["text"] = str(ceil(wind)) + " м/с,СВ"
    elif 90 <= degree <= 139:
        wind_now["text"] = str(ceil(wind)) + " м/с,В"
    elif 140 <= degree <= 179:
        wind_now["text"] = str(ceil(wind)) + " м/с,ЮВ"
    elif 180 <= degree <= 224:
        wind_now["text"] = str(ceil(wind)) + " м/с,Ю"
    elif 225 <= degree <= 269:
        wind_now["text"] = str(ceil(wind)) + " м/с,ЮЗ"
    elif 270 <= degree <= 314:
        wind_now["text"] = str(ceil(wind)) + " м/с,З"
    elif 315 <= degree <= 359:
        wind_now["text"] = str(ceil(wind)) + " м/с,СЗ"

    """ 
    if -40 <= temp <= -10.99:
        temp_describe["text"] = "Очень холодно"
    elif -9 <= temp <= 0:
        temp_describe["text"] = "Холодно"
    elif 1 <= temp <= 10.99:
        temp_describe["text"] = "Нормально"
    elif 11 <= temp <= 19.99:
        temp_describe["text"] = "Тепло"
    elif 20 <= temp <= 40.99:
        temp_describe["text"] = "Душно и жарко"
    """


# Оформляем декоратор для функции IsChecked()
def find_sr_and_ss(func):
    def wrapper():
        """
        Декоратор для нахождении погоды
        для Checkbutton
        """
        try:
            statistic_main(func())
            """
        except UnauthorizedError:
            messagebox.showerror("Error0x02", "Неверный Api код!")
            label_Api["fg"] = "#FF0000"
        except AssertionError:
            print(1)
            """
        except Exception:
            messagebox.showerror("Error0x02", "Неверный Api код!")
            label_Api["fg"] = "#FF0000"

    return wrapper


def weather_search(event=None):
    """
    Поиск Погоды по всем
    многочисленным параметрам
    """
    place = entry_weather.get()
    if place:
        try:
            statistic_main(place)  # "c46d676a6a93f1484be8cb1014377db0"
        except NotFoundError:
            messagebox.showerror("Error0x01", "Данные не корректны!")
            entry_weather.delete(0, END)
        except UnauthorizedError:
            messagebox.showerror("Error0x02", "Неверный Api код!")
            entry_weather.delete(0, END)

    elif not place:
        messagebox.showerror("Error0x03", "Данные не корректны!")


window.bind('<Return>', weather_search)


# Для очистки данных погоды
def statistics_clear():
    """
    Очистка текста
    """
    id_number_city["text"] = "..."
    visibility_describe["text"] = "..."
    temp_now["text"] = "..."
    wind_now["text"] = "..."
    humidity_now["text"] = "..."
    wind_describe["text"] = "..."
    temp_describe["text"] = "..."
    status_describe["text"] = "..."
    clouds_describe["text"] = "..."
    status_now["text"] = "..."
    get_sunrise["text"] = "..."
    get_sunset["text"] = "..."
    label_title_in["text"] = "Город/Страна: "
    get_pressure["text"] = "... мм рт. столба"


def delete_krest(event=None):
    """
    Очистка текста функции
    weather_search()
    Картинка в виде креста
    """
    clearing = entry_weather.get()
    if clearing:
        entry_weather.delete(0, END)
        statistics_clear()
    elif not clearing:
        messagebox.showerror("Error0x04", "Вы уже очистили текст!")


def clear(event=None):
    clearing = entry_weather.get()
    '''
    По нажатию кнопки BackSpace 
    будет очищаться текст и данные 
    по погоде
    '''
    if not clearing:
        # messagebox.showerror("Error0x02", "Вы уже очистили!")
        entry_weather.delete(0, END)
        statistics_clear()


window.bind('<BackSpace>', clear)


# Меняет цвет при нажатии на Label == name_weather
def change_color(event):
    colors = ["#FF1493", "#DDA0DD", "#90EE90", "#1E90FF", "#8B4513", "#87CEEB", "#3368FF", "#FF3333"]
    number = randint(0, len(colors))
    name_weather["fg"] = colors[number]


# Проверка CheckButoon (Очистка)
def b_country_1():
    placement_Moscow = Moscow.get()
    placement_Shatura = Shatura.get()
    placement_Kapotnya = Kapotnya.get()
    placement_Zolotovo = Zolotovo.get()
    placement_Electrostal = Electrostal.get()
    if placement_Moscow == True:
        Moscow.set(False)
        statistics_clear()
    if placement_Shatura == True:
        Shatura.set(False)
        statistics_clear()
    if placement_Kapotnya == True:
        Kapotnya.set(False)
        statistics_clear()
    if placement_Zolotovo == True:
        Zolotovo.set(False)
        statistics_clear()
    if placement_Electrostal == True:
        Electrostal.set(False)
        statistics_clear()
    elif (placement_Moscow == False) and (placement_Shatura == False) and (placement_Kapotnya == False) and (
            placement_Zolotovo == False) and (placement_Electrostal == False):
        messagebox.showerror("Error0x05", "Вы уже очистили!")


# Закрывет окно приложения
def destroy(event=None):
    result_message = messagebox.askquestion(title='ПОГОДА ОНЛАЙН', message='Вы хотите точно закрыть окно?')
    if result_message == 'yes':
        window.destroy()


window.bind('<Escape>', destroy)


# Из 1 до 5 IsChecked()
@find_sr_and_ss
def IsChecked():
    placement = Moscow.get()
    place = "Moscow"
    if placement == True:
        return place


@find_sr_and_ss
def IsChecked_2():
    placement = Zolotovo.get()
    place = "Золотово"
    if placement == True:
        return place


@find_sr_and_ss
def IsChecked_3():
    placement = Shatura.get()
    place = "Шатура"
    if placement == True:
        return place


@find_sr_and_ss
def IsChecked_4():
    placement = Kapotnya.get()
    place = "Капотня"
    if placement == True:
        return place


@find_sr_and_ss
def IsChecked_5():
    placement = Electrostal.get()
    place = "Электросталь"
    if placement == True:
        return place


# Дизайн
high_color = Frame(window, width=90, height=1, bg="#FD974F")
high_color.pack(fill=BOTH, side=TOP, expand=True)  # Верхний слой

desktop_color = Frame(window, width=1930, height=500, bg="#E6E6FA")
desktop_color.pack(fill=BOTH, side=TOP, expand=True)  # Задний фон

Botomm_color = Frame(window, width=90, height=1, bg="#FD974F")
Botomm_color.pack(fill=BOTH, side=BOTTOM, expand=True)  # Для нижнего слоя

label_frame = Frame(window)
label_frame.place(relwidth=0.90, relheight=0.90, relx=0.05, rely=0.05)  # Для изображения

# Основное окно
frame = Frame(window, bg="#FFDEAD")  # FFDEAD
frame.place(relwidth=0.67, relheight=0.7, relx=0.15, rely=0.15)

# Внутри Основного окна
frame_in = Frame(frame, bg="#87CEEB", bd=4, relief=RIDGE)
frame_in.place(relwidth=0.27, relheight=0.44, relx=0.04, rely=0.03)

# Название Города или Страны
label_title_in = Label(frame_in, bg="#87CEEB", text="Город/Страна: ", font=("Times", "12"))
label_title_in.pack()

# Создание Восхода и Заката и Атм.сфера данных
sunrise = Label(frame_in, bg="#87CEEB", text="Время Восхода:", font=("Times", "12"))
sunrise.pack()

get_sunrise = Label(frame_in, bg="#87CEEB", text="... ч.", font=("Times", "12"))
get_sunrise.pack()

sunset = Label(frame_in, bg="#87CEEB", text="Время Заката:", font=("Times", "12"))
sunset.pack()

get_sunset = Label(frame_in, bg="#87CEEB", text="... ч.", font=("Times", "12"))
get_sunset.pack()

presser = Label(frame_in, bg="#87CEEB", text="   Атмосферное давление: ", font=("Times", "12")).pack(anchor=W)

get_pressure = Label(frame_in, bg="#87CEEB", text="... мм рт. столба", font=("Times", "12"))
get_pressure.pack()

# Время Лондон
label_London = Label(frame, height=1, text="London", font=("Times", "17"), bg="#7CFC00")
# label_London.place(relx = 0.01,rely = 0.01,relwidth = 0.2)


timer_London = Label(frame, height=1, text="...", bg="#7CFC00")
# timer_London.place(relx = 0.01,rely = 0.08,relwidth = 0.2)


# Время Франция
label_France = Label(frame, height=1, text="France", font=("Times", "17"), bg="#7CFC00")
# label_France.place(relx = 0.01,rely = 0.13,relwidth = 0.2)

timer_France = Label(frame, height=1, text="...", bg="#7CFC00")
# timer_France.place(relx = 0.01,rely = 0.20,relwidth = 0.2)

# Время Польша
label_Poland = Label(frame, height=1, text="Poland", font=("Times", "17"), bg="#7CFC00")
# label_Poland.place(relx = 0.79,rely = 0.14,relwidth = 0.2)

timer_Poland = Label(frame, height=1, text="...", bg="#7CFC00")
# timer_Poland.place(relx = 0.79,rely = 0.21,relwidth = 0.2)

# Изображение

# canvas = Canvas(label_frame, height=1000, width=700)
# image = canvas.create_image(0, 0, anchor=NW ,image=photo)


image = Image.open("natural_lake.png")
photo = ImageTk.PhotoImage(image)
label = Label(label_frame, image=photo)
label.image_ref = photo
label.pack()

"""
def natural():
    pictures = ["natural.png", "natural_lake.png", "natural_Montains.png"]
    image = Image.open("natural.png")
    photo = ImageTk.PhotoImage(image)
    label = Label(label_frame,image=photo)
    label.image_ref = photo
    label.pack()
"""

# but_pict = Button(frame, text = "менять", command = natural)
# but_pict.place(relx = 0.1, rely = 0.09)


krest = PhotoImage(file="krestik.png")  # Изображение креста

# Названия
name_weather = Label(frame, bg="#FFDEAD", font=("Times", "19"), text="Погода Онлайн", fg="black")  # FFDEAD
name_weather.bind("<Button-1>", change_color)
name_weather.pack(pady=30)

search = Label(frame, bg="#FFDEAD", font=("Times", "14"), text="Введите Город/Страну:")
# search.place(relx = 0.05, rely = 0.23, relwidth = 0.3)

# Время МСК
clock = Label(frame, bg="#FFDEAD", font=("Times", "14"), text=string_time)
clock.place(relx=0.35, rely=0.17, relwidth=0.3)

# Создание поиска погоды и APi

entry_weather = Entry(frame, font=("Arial", "12"), width=20, relief=GROOVE, bg="#F2F4F4", fg="#5C4033", bd=2,
                      cursor="xterm")
entry_weather.place(relx=0.35, rely=0.24, relwidth=0.3)
entry_weather.insert(0, "Москва")
entry_weather.focus()

insert_Api = Entry(frame, font=("Arial", "8"), width=40, relief=GROOVE, bg="#F2F4F4", fg="#5C4033", bd=2, show="*",
                   cursor="xterm")
insert_Api.insert(0, "c46d676a6a93f1484be8cb1014377db0")
insert_Api.place(relx=0.66, rely=0.46)

label_Api = Label(frame, text="Введите API код: ", font=("Arial", "11"), width=20, bg="#FFDEAD", fg="black")
label_Api.place(relx=0.62, rely=0.4)

button_Api = Button(frame, text="Принять", relief=RIDGE, bg="#ADFF2F", font=("Times", "11"), activebackground="#ADFF2F",
                    cursor="hand2", command=apply_Api)
button_Api.place(relx=0.9, rely=0.52)

# Создание Копки "Узнать погоду"
button_weather = Button(frame, text="Узнать погоду", relief=RIDGE, bg="#ADFF2F", font=("Times", "14"),
                        activebackground="#ADFF2F", cursor="hand2", command=weather_search)
button_weather.place(relx=0.35, rely=0.30, relwidth=0.3)

# Очищение
button_clear = Button(frame, text="Очистить", relief=RIDGE, bg="#FF4500", font=("Times", "14"),
                      activebackground="#FF4500", command=clear)
# button_clear.place(relx = 0.35,rely=0.40,relwidth=0.3)

button_break = Button(frame, relief=RIDGE, bg="#D3D3D3", activebackground="#D3D3D3", image=krest, cursor="hand2",
                      command=delete_krest)
button_break.place(relx=0.65, rely=0.24, relwidth=0.04, relheight=0.06)

# Закрытие программы
button_break_window = Button(frame, text="Закрыть окно", relief=RIDGE, bg="#87CEEB", font=("Times", "14"),
                             activebackground="#87CEEB", cursor="hand2", command=destroy)
button_break_window.place(relx=0.35, rely=0.40, relwidth=0.3)

# Описание всех задач для погоды

# detailed.status()
status_describe = Label(frame, font=("Times", "14"), bd=5, justify=LEFT, relief=GROOVE, text="...", bg="#FFD700")
status_describe.place(relx=0.50, rely=0.51, relwidth=0.3)

status_now = Label(frame, font=("Times", "14"), bd=5, relief=GROOVE, text="...", bg="#FFD700")
status_now.place(relx=0.19, rely=0.51, relwidth=0.3)

# row = 0 colomn = 1

temp_now = Label(frame, font=("Times", "14"), bd=5, relief=GROOVE, text="...", bg="#FFD700")
temp_now.place(relx=0.35, rely=0.61, relwidth=0.3)

# row = 0 colomn = 2

temp_describe = Label(frame, font=("Times", "14"), bd=5, relief=GROOVE, text="...", bg="#FFD700")
temp_describe.place(relx=0.66, rely=0.61, relwidth=0.3)

# row 1 colomn = 1

wind_now = Label(frame, font=("Times", "14"), bd=5, relief=GROOVE, text="...", bg="#FFD700")
wind_now.place(relx=0.35, rely=0.71, relwidth=0.3)

# row 1 colomn = 2

wind_describe = Label(frame, font=("Times", "14"), bd=5, relief=GROOVE, text="...", bg="#FFD700")
wind_describe.place(relx=0.66, rely=0.71, relwidth=0.3)

# row 2 colomn = 1

humidity_now = Label(frame, font=("Times", "14"), bd=5, relief=GROOVE, text="...", bg="#FFD700")
humidity_now.place(relx=0.35, rely=0.81, relwidth=0.3)

# row 2 colomn = 2

clouds_describe = Label(frame, font=("Times", "14"), bd=5, relief=GROOVE, text="...", bg="#FFD700")
clouds_describe.place(relx=0.66, rely=0.81, relwidth=0.3)

# row = 0 colomn = 0

name_temp = Label(frame, font=("Times", "14"), bd=5, relief=GROOVE, text="Температура", bg="#FFD700")
name_temp.place(relx=0.04, rely=0.61, relwidth=0.3)

# row 1 colomn = 0

name_wind = Label(frame, font=("Times", "14"), bd=5, relief=GROOVE, text="Ветер", bg="#FFD700")
name_wind.place(relx=0.04, rely=0.71, relwidth=0.3)

# row 2 colomn = 0

name_humidity = Label(frame, font=("Times", "14"), bd=4, relief=GROOVE, text="Влажность и облачность", justify=LEFT,
                      bg="#FFD700")
name_humidity.place(relx=0.04, rely=0.81, relwidth=0.3)

# row 3 colomn = 0

name_visibility = Label(frame, font=("Times", "14"), bd=4, relief=GROOVE, text="Видимость и id Ст/Гор.", justify=LEFT,
                        bg="#FFD700")
name_visibility.place(relx=0.04, rely=0.9, relwidth=0.3)

# row 3 colomn = 1

visibility_describe = Label(frame, font=("Times", "14"), bd=4, relief=GROOVE, text="...", justify=LEFT, bg="#FFD700")
visibility_describe.place(relx=0.35, rely=0.9, relwidth=0.3)

# row 3 colomn = 2

id_number_city = Label(frame, font=("Times", "14"), bd=4, relief=GROOVE, text="...", justify=LEFT, bg="#FFD700")
id_number_city.place(relx=0.66, rely=0.9, relwidth=0.3)

# Окно задачи
country = LabelFrame(frame, text='Страны/Города', bd=5, relief=GROOVE, bg="#FFDEAD")
country.place(relx=0.85, rely=0.01)

b_country = Button(frame, text="Стереть все", bd=2, width=12, relief=GROOVE, font=("Times", "11"), bg="#E97451",
                   activebackground="#E97451", cursor="hand2", command=b_country_1)
b_country.place(relx=0.85, rely=0.35)

Moscow = BooleanVar()
Zolotovo = BooleanVar()
Shatura = BooleanVar()
Kapotnya = BooleanVar()
Electrostal = BooleanVar()

Checkbutton(country, text='Москва', bg="#FFDEAD", activebackground="#FFDEAD", variable=Moscow, cursor="hand2",
            command=IsChecked).pack(anchor=W)

Checkbutton(country, text='Золотово', bg="#FFDEAD", activebackground="#FFDEAD", variable=Zolotovo, cursor="hand2",
            command=IsChecked_2).pack(anchor=W)

Checkbutton(country, text='Шатура', bg="#FFDEAD", activebackground="#FFDEAD", variable=Shatura, cursor="hand2",
            command=IsChecked_3).pack(anchor=W)

Checkbutton(country, text='Капотня', bg="#FFDEAD", activebackground="#FFDEAD", variable=Kapotnya, cursor="hand2",
            command=IsChecked_4).pack(anchor=W)

Checkbutton(country, text='Электросталь', bg="#FFDEAD", activebackground="#FFDEAD", variable=Electrostal,
            cursor="hand2", command=IsChecked_5).pack(anchor=W)

time_Moscow()
window.mainloop()




