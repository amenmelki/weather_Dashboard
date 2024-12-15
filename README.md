# Weather Dashboard

This is a simple weather dashboard application built using Python and Tkinter. The app allows users to check the current weather in any city, view weather details like temperature, humidity, wind speed, and more. The app also features a weather icon display and allows saving favorite cities for easy access.

## Features
- Search and display weather information for a city.
- Display weather icon and update background according to weather conditions.
- Save favorite cities for quick access.
- Toggle between Celsius and Fahrenheit units.
- Display recent searches and show error messages for invalid cities.
- Auto-detect location and show weather for the user's location.

## Libraries Used
- **Tkinter**: For creating the graphical user interface (GUI).
- **Pillow**: For handling image loading and resizing of weather icons.
- **Requests**: To fetch weather data from the OpenWeather API.
- **Geopy**: To detect the user's location using geolocation.
- **ttk**: For enhanced widgets in the Tkinter GUI.

## Python Version
This project uses Python 3.9.13.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/amenmelki/weather_Dashboard.git

## Requirements
requests==2.28.1
Pillow==9.0.1
geopy==2.2.0
