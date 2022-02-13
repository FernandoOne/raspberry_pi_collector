import serial
import time

#Macros for the characters used to navigate the menu
ESC_CHARACTER = b'\033\0\0\0\0'
LEFT_CHARACTER = b'\033[D'
RIGHT_CHARACTER = b'\033[C'
ENTER_CHARACTER = b'\r\n'

#Macros for the actions that can be sent to the CC1352R
FORM_NETWORK = "Form network"
OPEN_NETWORK = "Open network"
CLOSE_NETWORK = "Close network"
SET_REPORT_INTERVAL = "Set report interval"
SEND_TOGGLE = "Send toggle"

# class menuNavigation:
#   def __init__(menuNavigation, a, b):
#     menuNavigation.menuStep = "-1"
#     menuNavigation.alreadySent = "False"

# def performAction():
#     if condicion == 1:
#         print("Haz a")
#     elif condicion == 2:
#         print("Haz b")
#     elif condicion == 3:
#         print("Haz c")
#     else:
#         print("Haz d")

def navigateMenu(character, serialPort):
    serialPort.write(character)

def processDataToSend(data, menuStep, serialPort):
    if data == OPEN_NETWORK:
        if menuStep == "-2":
            navigateMenu(ESC_CHARACTER, serialPort)
            print("Llego al step -2" + menuStep)
            return "-1"
        if menuStep == "-1":
            navigateMenu(ESC_CHARACTER, serialPort)
            print("Llego al step -1" + menuStep)
            return "0"
        if menuStep == "0":
            navigateMenu(RIGHT_CHARACTER, serialPort)
            print("Llego al step 0" + menuStep)
            return "0"
        elif menuStep == "1":
            navigateMenu(ENTER_CHARACTER, serialPort)
            print("Llego al step 1" + menuStep)
            return "2"
        elif menuStep == "2":
            navigateMenu(RIGHT_CHARACTER, serialPort)
            print("Llego al step 2" + menuStep)
            return "2"
        elif menuStep == "3":
            navigateMenu(ENTER_CHARACTER, serialPort)
            print("Llego al step 3" + menuStep)
            return "4"
        else:
            pass
