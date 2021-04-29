# PythonScripts

## Weather.py

This script downloads weather data from weather.gov, from a tower near where I live, parses out the information I'm interested in, and packages it into a bytestring that when piped to a thermal receipt printer, outputs a nicely formatted receipt! One that reports on the day's weather. I'm well aware that there's a python library "escpos" made for interfacing with receipt printers, but after doing it myself, this _really_ wasn't that complex of a process. And I learned a bit while doing so!
