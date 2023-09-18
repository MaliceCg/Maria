import time
import grovepi
from subprocess import *
from random import *
from subprocess import *
import time
import os
import serial
import json
import requests

grovepi.set_bus("RPI_1")


def try_parse_int(s):
    try:
        return int(s)
    except ValueError:
        return s

# Connect the Grove Button to digital port D3
# SIG,NC,VCC,GND
ultrasonic_ranger = 2
button = 3
cmd= 'echo '
cmdfin= ' > /dev/usb/lp0'
cmd_voc = 'aplay '
cmd_banque3 = 'Banque_son/banque3.wav'
cmd_end=' 2>/dev/null'

cmd_banque1 = "Banque_son/banque1_"
cmd_banque2 = "Banque_son/banque2_"
cmd_nom=randint(1,1)
cmd_fichier='.wav'

counter_audio = 0
bool_firstaudio = False
bool_secondaudio = True

ser = serial.Serial('/dev/ttyACM0', 9600)
grovepi.pinMode(button,"INPUT")

# Opening JSON file
f = open('Banque_conseil/advices.json')
  
# returns JSON object as 
# a dictionary
advices = json.load(f)

f.close()

while True:
    try:
        data = ser.readline().decode("utf-8").strip('\n').strip('\r') # remove newline and carriage return characters
        #ser.flushInput()
    except UnicodeDecodeError:
        print('UnicodeDecodeError')
    
    # try:
    #     montant = float(try_parse_int(data))
    # except ValueError:
    #     print('ValueError')
    
    montant = 2.0
    print(montant)

    try:
        #-----------PARTIE DETECTION MOUVEMENT-----------------------------------------------------
        # Read distance value from Ultrasoniccmd_nom=randint(1,3)
        time.sleep(0.5) # Temps de pause entre chaque tour de boucle 0.5 seconde
        
        counter_audio += 1
        print('counter_audio = ', counter_audio)
        print(grovepi.ultrasonicRead(ultrasonic_ranger))
        cmd_nom=randint(1,3)
        
        if(grovepi.ultrasonicRead(ultrasonic_ranger) < 200 and bool_secondaudio and counter_audio > 100000):
            print(cmd_voc+cmd_banque1+str(cmd_nom)+cmd_fichier+cmd_end)
            run([cmd_voc+cmd_banque1+str(cmd_nom)+cmd_fichier+cmd_end],shell=True)
            bool_firstaudio = True
            bool_secondaudio = False
            counter_audio = 0 
            
        # Pause de 1 minute après la 1ère détéction
        counter_audio += 1
            
        # Si la présence est redéctée après la minute passée on passe à la banque de son 2
        if(grovepi.ultrasonicRead(ultrasonic_ranger) < 200 and bool_firstaudio and counter_audio > 100000): 
                run([cmd_voc+cmd_banque2+str(cmd_nom)+cmd_fichier+cmd_end],shell=True)
                bool_secondaudio = True
                bool_firstaudio = False
                counter_audio = 0
        else:
            print("Pas de nouvelle détection")

        if counter_audio > 240:
            bool_firstaudio = False
            bool_secondaudio = True
   
        #-----------PARTIE COIN INSERTION----------------------------------------------------------
        print("BUTTON : ", grovepi.digitalRead(button))
        if(grovepi.digitalRead(button) == 1):
            if (montant >= 0.10):
                if (montant <= 0.50):
                    num = str(randint(1,3))
                    advice = advices['bad_advice'][num]
                    os.system("sudo chmod 777 /dev/usb/lp0")
                    os.system(cmd+advice+cmdfin)
                    print((cmd+advice+cmdfin))
                    time.sleep(1)
                elif (montant <= 2.00):
                    num = str(randint(1,3))
                    advice = advices['medium_advice'][num]
                    os.system("sudo chmod 777 /dev/usb/lp0")
                    os.system(cmd+advice+cmdfin)
                    print((cmd+advice+cmdfin))
                    time.sleep(1)
                elif (montant > 2.00):
                    print("BUTTON : ")
                    num = str(randint(1,3))
                    advice = advices['good_advice'][num]
                    os.system("sudo chmod 777 /dev/usb/lp0")
                    os.system(cmd+advice+cmdfin)
                    print((cmd+advice+cmdfin))
                    time.sleep(1)
                requests.post("https://docs.google.com/forms/d/1-_jv7JE1_aLBskyqAf0xEBg0B5bbg4e-MOKmUE6tjLs/formResponse?ifq&entry.216786359="+ str(montant)+ "&submit=Submit")    
                ser.write("0".encode())
            else:
                run([cmd_voc+cmd_banque3+cmd_end],shell=True)
            time.sleep(2)
            
    except IOError:
        print ("Error")
        time.sleep(0.1) # don't overload the i2c bus
