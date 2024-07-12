"""
Important Guidelines and Information about the Project:
1. This project requires Internet Connection to work as supposed to be.
2. This project is build up on few major libraries and api's as follows:
    a)Tkinter
    b)pillow
    c)datetime
    d)requests
    e)fetchify
    f)OpenWeatherMap API
    g)ipinfo API
    h)timeapi
3. It is advised to open this porject on 1920x1080 resolution at 125% scale display for best experience.
4. Few Libraries used may require individual installation instead of grouped.
5. The library 'fetchify' is developed by Anupam Kanoongo i.e me. (Github : Anupam1707).
6. To report any issue or bug, user can drop a mail at anupamkanoongo@gmail.com
"""

from tkinter import *
from tkinter import messagebox
from tkinter import END
from time import *
from time import sleep
from threading import Timer
import os
try: 
    from datetime import datetime
    from PIL import Image, ImageTk
    import requests
    from fetchify import fetch
except ImportError:
    print("Installing Libraries")
    print()
    os.system("pip install datetime pillow requests fetchify")
from io import BytesIO
from datetime import datetime
from PIL import Image, ImageTk, ImageSequence
import requests

weather = ""

root = Tk() 
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
 
def time_format_for_location(utc_with_tz):
    local_time = datetime.utcfromtimestamp(utc_with_tz)
    return local_time.time()

def get_location():
    response = requests.get('https://ipinfo.io')
    data = response.json()
    return data
 
city_value = StringVar()
# city_value.set("Enter a City")

now = datetime.now()

def customWeather():
    global weather
    lng = 0
    lat = 0
    
    api_key = "141f5109c5c29634665af4a4a59e95a6"
    
    cus_city_name=city_value.get()
    
    inpfield.delete("1.0", "end") 

    try:
        weather_url = 'http://api.openweathermap.org/data/2.5/weather?q=' + cus_city_name + '&appid=' + api_key
    
        response = requests.get(weather_url)
        weather_info = response.json()
    
        kelvin = 273 
        tempc = int(weather_info['main']['temp'] - kelvin)
        tempk = int(weather_info['main']['temp'])
        tempf = ((9*tempc)/5)+32
        tempf = round(tempf,1)
        pressure = weather_info['main']['pressure']
        humidity = weather_info['main']['humidity']
        sunrise = weather_info['sys']['sunrise']
        sunset = weather_info['sys']['sunset']
        timezone = weather_info['timezone']
        cloudy = weather_info['clouds']['all']
        description = weather_info['weather'][0]['description']
        wind_speed = weather_info['wind']['speed']

        sunrise_time = time_format_for_location(sunrise + timezone)
        sunset_time = time_format_for_location(sunset + timezone)
         
        weather = f"Weather of: {cus_city_name}\nTemperature (Celsius): {tempc}°C\nTemperature (Kelvin): {tempk}K\nTemperature (Farenheit) :{tempf}°F\nPressure: {pressure} hPa\nWind Speed: {wind_speed} m/s\nHumidity: {humidity}%\nSunrise at {sunrise_time} and Sunset at {sunset_time}\nCloud: {cloudy}%\nWeather Info: {description}"

    except:
        weather = f"Error Processing the Data\nPlease retry or report the problem"
            
    inpfield.insert(INSERT, weather)
     
def showWeather():
    global weather
    lng = 0
    lat = 0
    country = "Unknown"

    api_key = "141f5109c5c29634665af4a4a59e95a6"
 
    cus_city_name=get_location().get("city")
    
    autofield.delete("1.0", "end") 

    try:
        lat = get_location().get('loc').split(",")[0]
        lng = get_location().get('loc').split(",")[1]
        country = get_location().get("country")
        time_url = "https://www.timeapi.io/api/Time/current/coordinate?latitude="+str(lat)+"&longitude="+str(lng)
        weather_url = 'http://api.openweathermap.org/data/2.5/weather?q=' + cus_city_name + '&appid='+api_key
    
        response = requests.get(weather_url)
        responset = requests.get(time_url)
        weather_info = response.json()
        time_info = responset.json()
    
        kelvin = 273 
        tempc = int(weather_info['main']['temp'] - kelvin)
        tempk = int(weather_info['main']['temp'])
        tempf = ((9*tempc)/5)+32
        tempf = round(tempf,1)
        pressure = weather_info['main']['pressure']
        humidity = weather_info['main']['humidity']
        sunrise = weather_info['sys']['sunrise']
        sunset = weather_info['sys']['sunset']
        timezone = weather_info['timezone']
        cloudy = weather_info['clouds']['all']
        description = weather_info['weather'][0]['description']
        time = time_info.get("time")
        wind_speed = weather_info['wind']['speed']

        if lat == 0 and lng == 0:
            time = "Unable to Fetch Time"
        sunrise_time = time_format_for_location(sunrise + timezone)
        sunset_time = time_format_for_location(sunset + timezone)
         
        weather = f"Weather of: {cus_city_name}, {country}\nTime : {time}\nTemperature (Celsius): {tempc}°C\nTemperature (Kelvin): {tempk}K\nTemperature (Farenheit) :{tempf}°F\nPressure: {pressure} hPa\nWind Speed: {wind_speed} m/s\nHumidity: {humidity}%\nSunrise at {sunrise_time} and Sunset at {sunset_time}\nCloud: {cloudy}%\nWeather Info: {description}"

    except:
        weather = f"Error determining your Location"
            
    autofield.insert(INSERT, weather)

class RepeatedTimer:
    def __init__(self, interval, function, *args, **kwargs):
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.timer = None
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self.timer = Timer(self.interval, self._run)
            self.timer.daemon = True
            self.timer.start()
            self.is_running = True

    def stop(self):
        self.timer.cancel()
        self.is_running = False

class AnimatedGIF(Label):
    def __init__(self, master, gif_path, width, height, *args, **kwargs):
        Label.__init__(self, master, *args, **kwargs)
        self.gif_path = gif_path
        self.width = width
        self.height = height
        self.sequence = []
        self.load_frames()
        self.image = self.sequence[0]
        self.configure(image=self.image)
        self.delay = 100
        self.current_frame = 0
        self.animate_gif()

    def load_frames(self):
        gif = Image.open(BytesIO(fetch(self.gif_path, "LT", image=True)))
        for frame in ImageSequence.Iterator(gif):
            frame = frame.resize((self.width, self.height), Image.LANCZOS)
            self.sequence.append(ImageTk.PhotoImage(frame))

    def animate_gif(self):
        self.current_frame = (self.current_frame + 1) % len(self.sequence)
        self.configure(image=self.sequence[self.current_frame])
        self.after(self.delay, self.animate_gif)
    
def date():
    dtfield.delete("1.0", "end")
    url = "https://www.timeapi.io/api/Time/current/coordinate?latitude="+str(get_location().get('loc').split(",")[0])+"&longitude="+str(get_location().get('loc').split(",")[1])
    responsed= requests.get(url)
    info = responsed.json()
    day = info.get("dayOfWeek")
    d = info.get("day")
    m = info.get("month")
    y = info.get("year")
    data = f"{day}  {d}/{m}/{y}"

    dtfield.insert(END, data)
    dtfield.tag_add("center", "1.0", "end")
            
def showtime():
    string = strftime('%H:%M:%S %p')
    lbl.config(text=string)
    lbl.after(1000, showtime)

def quit():
        result = messagebox.askyesno("Confirmation", "Are you sure you want to quit?")
        if result == True:
            root.destroy()
        
def background():
    try:
        img = Image.open(BytesIO(fetch("Learntricks.png", "we", image=True)))
        img = img.resize((width,height), Image.LANCZOS)
        test = ImageTk.PhotoImage(img)
        bk = Label(image=test)
        bk.image = test
        bk.place(x=0, y=0)  
    except:
        print("Failed")
        background()
        
animated_gif = AnimatedGIF(root, "Learntricks.gif", width, height)
animated_gif.place(x=0,y=0)
##background()

#Display
root.attributes('-fullscreen', True)
root.title("Global Weather Bulletin") 

title = Label(root, text= 'Global Weather Bulletin', font= 'Arial 40 bold', bg='yellow').pack(pady=0)
name = Label(root, text= ' Programmed by Anupam Kanoongo', font= 'Arial 30 bold', bg="white").pack(side = "left", anchor = "sw")
city_head= Label(root, text = 'City of your choice :-', font = 'Arial 20 bold', bg='lightblue').place(x=width-555, y=int(height/3)+55)
cus_city_head= Label(root, text = 'Weather Report of your Location', font = 'Arial 20 bold', bg='lightblue').place(x=50, y=int(height/3)+55)

inp_city = Entry(root, textvariable = city_value,  width = 25, font='Arial 16 bold').place(x=width-555, y=int(height/3)+97)

Button(root, text = 'Exit', font = 'Arial 20 bold', bg='red', command=quit).pack(side = "right", anchor = "se")
Button(root, command = customWeather, text = "Check Weather", font="Arial 20", bg='lightblue', fg='black', activebackground="teal").place(x=width-555, y=int(height/3)-5)
Button(root, command = showWeather, text = "Refresh", font="Arial 20", bg='lightblue', fg='black', activebackground="teal").place(x=50, y=int(height/3)-10)

RepeatedTimer(60, date)

inpfield = Text(root, width=36, height=10, font="Arial 19",bg="BlanchedAlmond", highlightcolor = "BlanchedAlmond")
inpfield.place(x=width-555, y=int(height/3)+130)
autofield = Text(root, width=36, height=11, font="Arial 19",bg="BlanchedAlmond")
autofield.place(x=50, y=int(height/3)+100)
dtfield = Text(root, width = 20, height = 1, font="Arial 30",bg = "BlanchedAlmond")
dtfield.tag_configure("center", justify='center')
dtfield.place(x = int(width/2)-210, y = 2 * int(height/6-100))
lbl = Label(root, font="Arial 30",bg='BlanchedAlmond')
lbl.place(x = int(width/2)-110, y = 2 * int(height/6)-140)


showtime()
showWeather()
date()
root.mainloop()
