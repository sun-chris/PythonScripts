#!/usr/bin/python3
from lxml import etree
import requests

#Shorthand for the escape character and mode setting (stuff used often)
ESC = b'\x1b'               #ESC
MODE = ESC + b'\x21'        #ESC !

#Command to reset all formattings, and also the bytes representation of Newline char
RESET = ESC + b'\x40'       #ESC @
LF = b'\x0a'                #LF

#Different character combinations that act as formatting commands in ESC/POS
f = {
    "J-LEFT":       ESC + b'\x61\x00',  #ESC a 0
    "J-CENTER":     ESC + b'\x61\x01',  #ESC a 1
    "J-RIGHT":      ESC + b'\x61\x02',  #ESC a 2
    "EMPHASIS":     ESC + b'\x45\x01',  #ESC E 1
    "NO-EMPHASIS":  ESC + b'\x45\x00',  #ESC E 0
    "FONT-A":       MODE + b'\x00',     #ESC ! 0
    "FONT-B":       MODE + b'\x01',     #ESC ! 1
    "BOLD":         MODE + b'\x08',     #ESC ! 8
    "TALL":         MODE + b'\x10',     #ESC ! 16
    "WIDE":         MODE + b'\x20',     #ESC ! 32
    "UNDERLINE":    MODE + b'\x80'      #ESC ! 128
}

#Request XML for Gilbert,AZ weather data from weather.gov
r = requests.get("https://forecast.weather.gov/MapClick.php?lat=33.3031&lon=-111.7606&unit=0&lg=english&FcstType=dwml")

if r.ok:
    #Parse XML data
    data = etree.fromstring(r.content)

    #Get Station location, and publish date
    location = data.xpath("//location/area-description/text()")[0]
    refresh = data.xpath("//product/creation-date/text()")[0].split("T")[0]

    #Get list of times (Tonight, Thursday, Thursday Night...), and their corresponding forecast texts
    times = data.xpath("/dwml/data[1]/time-layout[1]/start-valid-time/@period-name")
    forecasts = data.xpath("/dwml/data[1]/parameters/wordedForecast/text/text()")

    #Start building receipt contents, starting with the header
    payload = RESET + f['EMPHASIS'] + f['J-CENTER'] + f['TALL']
    payload += bytes(f"Weather for {refresh}",'utf8') + LF
    payload += RESET + f['J-CENTER']
    payload += bytes(location,'utf8') + LF

    #Divider
    payload += RESET
    payload += b"-"*32 + LF

    #Body of receipt
    for i in range(3):
        payload += RESET + f['EMPHASIS'] + f['J-CENTER']
        payload += bytes(times[i],'utf8') + LF
        payload += RESET
        payload += bytes(forecasts[i],'utf8') + LF*2


#Save to printing queue folder
fp = open('queue/weather.txt','wb')
fp.write(payload)
fp.close()
