import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from geopy.geocoders import Nominatim

API_KEY = "1a9253dd6e00c2d0d8379bc2a906f0c8"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

recent_searches = []
favorite_cities = []

def get_weather():
    city = city_entry.get().strip()

    loading_spinner.start()

    if not city:
        messagebox.showerror("Error", "Please enter a city name!")
        loading_spinner.stop()
        return

    params = {
        "q": f"{city},tn",
        "appid": API_KEY,
        "units": "metric",
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        weather_data = response.json()
        display_weather(weather_data)
        recent_searches.insert(0, city)
        if len(recent_searches) > 5:
            recent_searches.pop()
    except requests.exceptions.HTTPError as e:
        messagebox.showerror("Error", f"Error: {e.response.json()['message']}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Network error: {str(e)}")
    finally:
        loading_spinner.stop()

def display_weather(data):
    try:
        city_name = data["name"]
        temp = data["main"]["temp"]
        weather = data["weather"][0]["description"]
        icon_code = data["weather"][0]["icon"]
        weather_main = data["weather"][0]["main"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        weather_label.config(
            text=f"City: {city_name}\nTemperature: {temp}°C\nWeather: {weather.capitalize()}\n"
                 f"Humidity: {humidity}%\nWind Speed: {wind_speed} m/s",
            foreground="#ffffff",
        )

        update_background(weather_main)

        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url)
        icon_response.raise_for_status()
        image_data = Image.open(BytesIO(icon_response.content))
        weather_icon = ImageTk.PhotoImage(image_data)
        icon_label.config(image=weather_icon)
        icon_label.image = weather_icon

    except KeyError:
        messagebox.showerror("Error", "Unexpected response format from API.")
    except requests.exceptions.RequestException:
        messagebox.showerror("Error", "Error loading weather icon.")

def update_background(weather_main):
    global bg_image, bg_photo
    weather_backgrounds = {
        "Clear": "img/sunny.jpg",
        "Clouds": "img/cloudy.jpg",
        "Rain": "img/rainy.jpg",
        "Snow": "img/snowy.jpg",
        "Thunderstorm": "img/stormy.jpg",
        "Drizzle": "img/drizzle.jpg",
        "Mist": "img/mist.jpg",
    }
    image_file = weather_backgrounds.get(weather_main, "img/stormy.jpg")

    try:
        bg_image = Image.open(image_file)
        resized_image = bg_image.resize((500, 400), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(resized_image)
        canvas.create_image(0, 0, anchor=tk.NW, image=bg_photo)
        canvas.image = bg_photo
    except FileNotFoundError:
        messagebox.showerror("Error", f"Background image not found: {image_file}")

def toggle_units(unit):
    city = city_entry.get().strip()
    if city:
        params = {
            "q": f"{city},tn",
            "appid": API_KEY,
            "units": unit,
        }
        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            weather_data = response.json()
            display_weather(weather_data)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Error: {str(e)}")

def save_favorite():
    city = city_entry.get().strip()
    if city and city not in favorite_cities:
        favorite_cities.append(city)
        favorite_combobox['values'] = favorite_cities

def auto_detect_location():
    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.geocode("your location")
    if location:
        city_name = location.address
        city_entry.delete(0, tk.END)
        city_entry.insert(0, city_name)
        get_weather()

root = tk.Tk()
root.title("Weather Dashboard")
root.geometry("500x450")

canvas = tk.Canvas(root, width=500, height=400)
canvas.pack(fill="both", expand=True)

header_label = tk.Label(root, text="Weather Dashboard", font=("Helvetica", 20, "bold"), fg="#ffffff", bg="#2c3e50")
header_label.place(x=150, y=10)

input_frame = tk.Frame(root, bg="#2c3e50")
input_frame.place(relx=0.5, y=70, anchor="center")

city_label = tk.Label(input_frame, text="Enter City Name:", font=("Helvetica", 12), fg="#ffffff", bg="#2c3e50")
city_label.grid(row=0, column=0, padx=5)

city_entry = ttk.Entry(input_frame, width=20, font=("Helvetica", 12))
city_entry.grid(row=0, column=1, padx=5)

get_weather_button = ttk.Button(input_frame, text="Get Weather", command=get_weather)
get_weather_button.grid(row=0, column=2, padx=5)

loading_spinner = ttk.Progressbar(root, mode="indeterminate", length=100)
loading_spinner.place(relx=0.5, y=120, anchor="center")

save_button = ttk.Button(input_frame, text="Save to Favorites", command=save_favorite)
save_button.grid(row=1, column=2, padx=5)

favorite_combobox = ttk.Combobox(input_frame, values=favorite_cities, width=20, state="readonly")
favorite_combobox.grid(row=1, column=0, padx=5)

weather_label = tk.Label(root, text="", font=("Helvetica", 14), justify="center", bg="#34495e", fg="#ffffff", padx=20, pady=10, width=50, anchor="center", relief="groove")
weather_label.place(relx=0.5, y=160, anchor="center")

icon_label = tk.Label(root, bg="#34495e")
icon_label.place(relx=0.5, y=250, anchor="center")

footer_label = tk.Label(root, text="Amen Allah Melki, 2024", font=("Helvetica", 10), fg="#bdc3c7", bg="#2c3e50")
footer_label.place(relx=0.5, y=400, anchor="center")

unit_frame = tk.Frame(root, bg="#2c3e50")
unit_frame.place(relx=0.5, y=430, anchor="center")

celsius_button = ttk.Button(unit_frame, text="Celsius", command=lambda: toggle_units('metric'))
celsius_button.grid(row=0, column=0, padx=5)

fahrenheit_button = ttk.Button(unit_frame, text="Fahrenheit", command=lambda: toggle_units('imperial'))
fahrenheit_button.grid(row=0, column=1, padx=5)

kelvin_button = ttk.Button(unit_frame, text="Kelvin", command=lambda: toggle_units('standard'))
kelvin_button.grid(row=0, column=2, padx=5)

def initialize_app():
    try:
        auto_detect_location()
    except Exception as e:
        print(f"Error detecting location: {str(e)}")

initialize_app()

root.mainloop()
