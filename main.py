######les bibliotheques######
from machine import Pin,ADC # pour les pins 
from time import sleep # pour la temporisation
import dht # pour le capteur d'humidite DHT11
from i2c_lcd import I2cLcd,I2C # 
import network # Pour la connection internet WIFI
from urequests import * # Protocole HTTP POST / GET
url='http://things.ubidots.com/api/v1.6/devices/security_esp'
token='BBFF-df8kCGai9vzCUXviDZr3F9y8HJV7VT'
headers={'X-Auth-Token':token ,'Content-Type':'application/json'}
######Initialisation des pins#####
ssid ="ETUDIANT" # le nom de point d'acces
pwd="#$et2022*$" # le mot de passe de point d'acces
led = Pin(0,Pin.OUT) #D3
buz= Pin(13,Pin.OUT) #D7
flam=Pin(12,Pin.IN) #D6
gaz=ADC(0) #A0
######MESURE DE TEMPERATURE ET HUMIDITE#######
ht = dht.DHT11(Pin(14)) #D5
############initialisation LCD############
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=3000) #D1,D2
lcd = I2cLcd(i2c,0x27,2,16)
lcd.move_to(0,0)
lcd.putstr('zeineb arbi')
lcd.move_to(0,1)
lcd.putstr('IOT PROJECT')
sleep(2)
lcd.clear()
def alarm(nb,t):
    for i in range(nb):
        led.on()
        buz.on()
        sleep(t)
        led.off()
        buz.off()
        sleep(t)
####################Connexion###########
st=network.WLAN(network.STA_IF)
st.active(True)
st.connect(ssid,pwd)
while not st.isconnected():
    print('Connexion en cours')
    sleep(0.5)
alarm(2,0.1)
sleep(5)
######Programme#####
while True:
    ht.measure()
    sleep(1)
    print(flam.value())
    print(gaz.read())
    t = ht.temperature()
    h = ht.humidity()
    print('temperarure : ',t,'  humidité : ',h)
    fl =flam.value()
    gz=gaz.read()
    if fl==0:
        alarm(5,1)
    if gz>500:
        alarm(5,0.1)
    lcd.move_to(0,1)
    lcd.putstr('T:'+str(t)+ ' H:'+ str(h)+ '% G:'+ str(int(gaz.read())) +'%')
    data={"temperatre":t,"humidite":h,"flame":fl,"gaz":gz}
    req=post(url=url,headers=headers,json=data)
    print(req.text)
    
    
        
        
    
    



    
    