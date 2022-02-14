import serial
import time

#Macros for the characters used to navigate the menu
BACK_CHARACTER = b'\033\0'
LEFT_CHARACTER = b'\033[D'
RIGHT_CHARACTER = b'\033[C'
ENTER_CHARACTER = b'\r'

def writeSerialPort(character, serialPort):
    serialPort.write(character)
    #time.sleep(0.05)

class menuNavigation:
    def __init__(self):
        self.action = ""
        self.actionParameter = ""
        self.actionType = ""
        self.menuStep = -2
        self.sendActionFlag = False
        self.alreadySentFlag = False
        self.endOfStep0String = ""
        self.endOfStep2String = ""

    def getAction(self):
        return self.action
    def setAction(self, string):
        self.action = string
    def getActionParameter(self):
        return self.actionParameter
    def setActionParameter(self, string):
        self.actionParameter = string        
    def getActionType(self):
        return self.actionType
    def setActionType(self, string):
        self.actionType = string        
    def getMenuStep(self):
        return self.menuStep
    def setMenuStep(self, step):
        self.menuStep = step
    def getSendActionFlag(self):
        return self.sendActionFlag
    def setSendActionFlag(self, flag):
        self.sendActionFlag = flag
    def getAlreadySentFlag(self):
        return self.alreadySentFlag
    def setAlreadySentFlag(self, flag):
        self.alreadySentFlag = flag
    def getEndOfStep0String(self):
        return self.EndOfStep0String
    def setEndOfStep0String(self, string):
        self.EndOfStep0String = string
    def getEndOfStep2String(self):
        return self.EndOfStep2String
    def setEndOfStep2String(self, string):
        self.EndOfStep2String = string

    def sendAction(self, action, actionParameter=""):
        if "FORM_NETWORK" in action:
            self.setAction("FORM_NETWORK")
            self.setActionParameter("")
            self.setActionType("Normal")
            self.setEndOfStep0String("<   NETWORK ACTIONS   >")
            self.setEndOfStep2String("<       FORM NWK      >")
        elif "OPEN_NETWORK" in action:
            self.setAction("OPEN_NETWORK")
            self.setActionParameter("")
            self.setActionType("Normal")
            self.setEndOfStep0String("<   NETWORK ACTIONS   >")
            self.setEndOfStep2String("<       OPEN NWK      >")
        elif "CLOSE_NETWORK" in action:
            self.setAction("CLOSE_NETWORK")
            self.setActionParameter("")
            self.setActionType("Normal")
            self.setEndOfStep0String("<   NETWORK ACTIONS   >")
            self.setEndOfStep2String("<       CLOSE NWK     >")
        elif "SET_REPORT_INTERVAL" in action:
            self.setAction("SET_REPORT_INTERVAL")
            self.setActionParameter(actionParameter)
            self.setActionType("Interceptable")
            self.setEndOfStep0String("<         APP         >")
            self.setEndOfStep2String("< SET REPORT INTERVAL >")             
        else:
            return
        self.setSendActionFlag(True)
        self.setAlreadySentFlag(False) 
        self.setMenuStep(0)

    def processWriting(self, serialPort):
        if self.getActionType() == "Normal":
            if self.getMenuStep() == -2:
                writeSerialPort(BACK_CHARACTER, serialPort)
                self.setMenuStep(-1)
                Menu.setAlreadySentFlag(False)
                print("Llegó al step -2")
            elif self.getMenuStep() == -1:
                writeSerialPort(BACK_CHARACTER, serialPort)
                self.setMenuStep(0)
                Menu.setAlreadySentFlag(False)
                print("Llegó al step -1")
            elif self.getMenuStep() == 0:
                writeSerialPort(RIGHT_CHARACTER, serialPort)
                Menu.setAlreadySentFlag(True)
                print("Llegó al step 0")
            elif self.getMenuStep() == 1:
                writeSerialPort(ENTER_CHARACTER, serialPort)
                self.setMenuStep(2)
                Menu.setAlreadySentFlag(False)
                print("Llegó al step 1")
            elif self.getMenuStep() == 2:
                writeSerialPort(RIGHT_CHARACTER, serialPort)
                Menu.setAlreadySentFlag(True)
                print("Llegó al step 2")
            elif self.getMenuStep() == 3:
                writeSerialPort(ENTER_CHARACTER, serialPort)
                self.setMenuStep(4)
                Menu.setAlreadySentFlag(False)
                self.setSendActionFlag(False)
                print("Llegó al step 3")
            else:
                pass
        elif self.getActionType() == "Interceptable":
            if self.getMenuStep() == -2:
                writeSerialPort(BACK_CHARACTER, serialPort)
                self.setMenuStep(-1)
                Menu.setAlreadySentFlag(False)
                print("Llegó al step -2")
            elif self.getMenuStep() == -1:
                writeSerialPort(BACK_CHARACTER, serialPort)
                self.setMenuStep(0)
                Menu.setAlreadySentFlag(False)
                print("Llegó al step -1")
            elif self.getMenuStep() == 0:
                writeSerialPort(RIGHT_CHARACTER, serialPort)
                Menu.setAlreadySentFlag(True)
                print("Llegó al step 0")
            elif self.getMenuStep() == 1:
                writeSerialPort(ENTER_CHARACTER, serialPort)
                self.setMenuStep(2)
                Menu.setAlreadySentFlag(False)
                print("Llegó al step 1")
            elif self.getMenuStep() == 2:
                writeSerialPort(RIGHT_CHARACTER, serialPort)
                Menu.setAlreadySentFlag(True)
                print("Llegó al step 2")
            elif self.getMenuStep() == 3:
                writeSerialPort(ENTER_CHARACTER, serialPort)
                self.setMenuStep(4)
                Menu.setAlreadySentFlag(False)
                print("Llegó al step 3")
            elif self.getMenuStep() == 4:
                writeSerialPort(b'00009000', serialPort)
                self.setMenuStep(5)
                Menu.setAlreadySentFlag(False)
                print("Llegó al step 4")
            elif self.getMenuStep() == 5:
                writeSerialPort(ENTER_CHARACTER, serialPort)
                self.setMenuStep(6)
                Menu.setAlreadySentFlag(False)
                self.setSendActionFlag(False)
                print("Llegó al step 5")                
            else:
                pass    


Menu = menuNavigation()
