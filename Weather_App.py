import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, Label, Button
from geopy.geocoders import OpenCage
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests 
import pytz
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize the main window
root = tk.Tk()
root.title("Weather App")

# Set window size and position
width = 900
height = 500
x_offset = 300
root.geometry(f"{width}x{height}+{x_offset}+100")

def getWeather():
    city = textfield.get()
    if city:
        geolocator = OpenCage(api_key='b4dc84eb92564428a1cb2b2536b3ca8f')
        location = geolocator.geocode(city)
        if location:
            obj = TimezoneFinder()
            result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
            logging.info(f"Timezone: {result}")
        else:
            messagebox.showerror("Error", "City not found")
            return
    else:
        messagebox.showerror("Error", "Please enter a city name")
        return

    # Get local time
    home = pytz.timezone(result)
    local_time = datetime.now(home)
    current_time = local_time.strftime("%I:%M %p")
    clock.config(text=current_time)
    name.config(text="CURRENT WEATHER")

    # Fetch weather data
    api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=646824f2b7b86caffec1d0b16ea77f79"
    json_data = requests.get(api).json()
    condition = json_data['weather'][0]['main']
    description = json_data['weather'][0]['description']
    temp = int(json_data['main']['temp'] - 273.15)
    pressure = json_data['main']['pressure']
    humidity = json_data['main']['humidity']
    wind = json_data['wind']['speed']

    # Update UI with weather data
    t.config(text=(temp, "°"))
    c.config(text=(condition, "|", "FEELS", "LIKE", temp, "°"))
    w.config(text=wind)
    h.config(text=humidity)
    d.config(text=description)
    p.config(text=pressure)

# Load and place images
def load_image(file_path, error_message):
    if os.path.exists(file_path):
        return PhotoImage(file=file_path)
    else:
        messagebox.showerror("Error", error_message)
        return None

Search_image = load_image("search.png", "search.png file not found")
if Search_image:
    myimage = Label(image=Search_image)
    myimage.place(x=20, y=20)

Search_icon = load_image("search_icon.png", "search_icon.png file not found")
if Search_icon:
    myimage_icon = Button(image=Search_icon, borderwidth=0, cursor="hand2", bg="#404040", command=getWeather)
    myimage_icon.place(x=400, y=34)

Logo_image = load_image("logo.png", "logo.png file not found")
if Logo_image:
    logo = Label(image=Logo_image)
    logo.place(x=150, y=100)

Frame_image = load_image("box.png", "box.png file not found")
if Frame_image:
    frame_myimage = Label(image=Frame_image)
    frame_myimage.pack(padx=5, pady=5, side=tk.BOTTOM)

# Time and weather labels
name = Label(root, font=("arial", 15, "bold"))
name.place(x=30, y=100)
clock = Label(root, font=("Helvetica", 20))
clock.place(x=30, y=130)

# Search text field
textfield = tk.Entry(root, justify='center', width=17, font=('poppins', 25, 'bold'), bg="#404040", border=0, fg="white")
textfield.place(x=50, y=40)
textfield.focus()

# Weather information labels
label1 = Label(root, text="WIND", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label1.place(x=120, y=400)

label2 = Label(root, text="HUMIDITY", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label2.place(x=250, y=400)

label3 = Label(root, text="DESCRIPTION", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label3.place(x=430, y=400)

label4 = Label(root, text="PRESSURE", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label4.place(x=650, y=400)

# Dynamic weather data labels
t = Label(font=("arial", 70, "bold"), fg="#ee666d")
t.place(x=400, y=150)
c = Label(font=("arial", 15, "bold"))
c.place(x=400, y=250)

w = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
w.place(x=120, y=430)
h = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
h.place(x=280, y=430)
d = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
d.place(x=450, y=430)
p = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
p.place(x=670, y=430)

# Start the main loop
root.mainloop()
