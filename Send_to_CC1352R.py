import serial
import time
import json

#Macros for the characters used to navigate the menu
RIGHT_CHARACTER = b'\033[C'
ENTER_CHARACTER = b'\r'

def writeSerialPort(character, serialPort):
    serialPort.write(character)
    time.sleep(0.05)

class menuNavigation:
    def __init__(self):
        self.actionName = ""
        self.actionAddress = ""
        self.actionParameter = ""
        self.actionType = ""
        self.menuStep = -2
        self.sendActionFlag = False
        self.alreadySentFlag = False
        self.endOfStep0String = ""
        self.endOfStep2String = ""
        self.backString = "<      BACK      >"
        self.backCounter = 0
        self.sendTwoStepsActionFlag = False
        self.sensorSelectedFlag = False
        self.stepTwoAction = ""
        self.stepTwoActionParameter = ""

    def getActionName(self):
        return self.actionName
    def setActionName(self, string):
        self.actionName = string
    def getActionAddress(self):
        return self.actionAddress
    def setActionAddress(self, string):
        self.actionAddress = string        
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
    def getBackString(self):
        return self.backString
    def setBackString(self, string):
        self.backString = string
    def getBackCounter(self):
        return self.backCounter
    def increaseBackCounter(self):
        self.backCounter = self.backCounter + 1
    def resetBackCounter(self):
        self.backCounter = 0
    def setSensorSelectedFlag(self, string):
        self.sensorSelectedFlag = string
    def getSensorSelectedFlag(self):
        return self.sensorSelectedFlag
    def getSendTwoStepsActionFlag(self):
        return self.sendTwoStepsActionFlag
    def setSendTwoStepsActionFlag(self, flag):
        self.sendTwoStepsActionFlag = flag
    def setStepTwoAction(self, string):
        self.stepTwoAction = string
    def getStepTwoAction(self):
        return self.stepTwoAction
    def setStepTwoActionParameter(self, string):
        self.stepTwoActionParameter = string
    def getStepTwoActionParameter(self):
        return self.stepTwoActionParameter

    def getActionParametersFromJSON(self, actionJSON):
        action = json.loads(actionJSON)
        self.setActionName(action['Action_name'])
        if 'Address' in action:
            self.setActionAddress(action['Address'])
        if 'Parameter' in action:
            self.setActionParameter(action['Parameter'])

    def sendAction(self, action, actionAdress="", actionParameter=""):
        print(action)
        if action == "FORM_NETWORK":
            self.setActionName("FORM_NETWORK")
            self.setActionParameter("")
            self.setActionType("Normal")
            self.setEndOfStep0String("<   NETWORK ACTIONS   >")
            self.setEndOfStep2String("<       FORM NWK      >")
        elif action == "OPEN_NETWORK":
            self.setActionName("OPEN_NETWORK")
            self.setActionParameter("")
            self.setActionType("Normal")
            self.setEndOfStep0String("<   NETWORK ACTIONS   >")
            self.setEndOfStep2String("<       OPEN NWK      >")
        elif action == "CLOSE_NETWORK":
            self.setActionName("CLOSE_NETWORK")
            self.setActionParameter("")
            self.setActionType("Normal")
            self.setEndOfStep0String("<   NETWORK ACTIONS   >")
            self.setEndOfStep2String("<       CLOSE NWK     >")
        elif action == "SELECT_SENSOR":
            self.setActionName("SELECT_SENSOR")
            self.setActionParameter(actionParameter)
            self.setActionType("Interceptable")
            self.setEndOfStep0String("<         APP         >")
            self.setEndOfStep2String("<     SELECT SENSOR   >")            
        elif action == "SET_REPORT_INTERVAL":
            self.setActionName("SET_REPORT_INTERVAL")
            self.setActionParameter(actionParameter)
            self.setActionType("Interceptable")
            self.setEndOfStep0String("<         APP         >")
            self.setEndOfStep2String("< SET REPORT INTERVAL >")
        elif action == "SEND_TOOGLE":
            self.setActionName("SEND_TOOGLE")
            self.setActionType("Normal")
            self.setEndOfStep0String("<         APP         >")
            self.setEndOfStep2String("<     SEND TOGGLE     >")
        elif action == "SEND_DISASSOCIATION":
            self.setActionName("SEND_DISASSOCIATION")
            self.setActionType("Normal")
            self.setEndOfStep0String("<         APP         >")
            self.setEndOfStep2String("< SEND DISASSOCIATION >")
        elif action == "OPEN_VALVE":
            self.setActionName("OPEN_VALVE")
            self.setActionType("Normal")
            self.setEndOfStep0String("<         APP         >")
            self.setEndOfStep2String("<     OPEN VALVE      >")  
        elif action == "CLOSE_VALVE":
            self.setActionName("CLOSE_VALVE")
            self.setActionType("Normal")
            self.setEndOfStep0String("<         APP         >")
            self.setEndOfStep2String("<     CLOSE VALVE     >")
        elif action == "SELECT_SENSOR_AND_SET_REPORT_INTERVAL":
            self.setAlreadySentFlag(False)
            self.setMenuStep(-2)
            self.setSendTwoStepsActionFlag(True)
            self.sendTwoStepsAction(action, actionAdress, actionParameter)                     
        else:
            return
        self.setSendActionFlag(True)
        self.setAlreadySentFlag(False) 
        self.setMenuStep(-2)

    def sendTwoStepsAction(self, action="", actionAdress="", actionParameter=""):
        if (self.getSensorSelectedFlag() == False):
            self.setStepTwoAction("SET_REPORT_INTERVAL")
            self.setStepTwoActionParameter(actionParameter)
            self.sendAction("SELECT_SENSOR", "", actionAdress)
        else:
            self.setSendTwoStepsActionFlag(False)
            self.setSensorSelectedFlag(False)
            self.sendAction(self.getStepTwoAction(), "", self.getStepTwoActionParameter())

    def processWriting(self, serialPort):
        if self.getActionType() == "Normal":
            if self.getMenuStep() == -2:
                writeSerialPort(RIGHT_CHARACTER, serialPort)
                self.increaseBackCounter()
                if self.getBackCounter() == 9:
                    self.setMenuStep(0)
                    self.resetBackCounter()
                self.setAlreadySentFlag(True)
                print("It reached step -2")
            elif self.getMenuStep() == -1:
                writeSerialPort(ENTER_CHARACTER, serialPort)
                self.resetBackCounter()
                self.setMenuStep(0)
                self.setAlreadySentFlag(False)
                print("It reached step -1")
            elif self.getMenuStep() == 0:
                writeSerialPort(RIGHT_CHARACTER, serialPort)
                self.setAlreadySentFlag(True)
                print("It reached step 0")
            elif self.getMenuStep() == 1:
                writeSerialPort(ENTER_CHARACTER, serialPort)
                self.setMenuStep(2)
                self.setAlreadySentFlag(False)
                print("It reached step 1")
            elif self.getMenuStep() == 2:
                writeSerialPort(RIGHT_CHARACTER, serialPort)
                self.setAlreadySentFlag(True)
                print("It reached step 2")
            elif self.getMenuStep() == 3:
                writeSerialPort(ENTER_CHARACTER, serialPort)
                self.setMenuStep(4)
                self.setAlreadySentFlag(False)
                self.setSendActionFlag(False)
                print("It reached step 3")
            else:
                pass
        elif self.getActionType() == "Interceptable":
            if self.getMenuStep() == -2:
                writeSerialPort(RIGHT_CHARACTER, serialPort)
                self.increaseBackCounter()
                if self.getBackCounter() == 9:
                    self.setMenuStep(0)
                    self.resetBackCounter()
                self.setAlreadySentFlag(True)
            elif self.getMenuStep() == -1:
                writeSerialPort(ENTER_CHARACTER, serialPort)
                self.resetBackCounter()
                self.setMenuStep(0)
                self.setAlreadySentFlag(False)
                print(self.getActionName())
                print("It reached step -1")
            elif self.getMenuStep() == 0:
                writeSerialPort(RIGHT_CHARACTER, serialPort)
                self.setAlreadySentFlag(True)
                print(self.getActionName())
                print("It reached step 0")
            elif self.getMenuStep() == 1:
                writeSerialPort(ENTER_CHARACTER, serialPort)
                self.setMenuStep(2)
                self.setAlreadySentFlag(False)
                print(self.getActionName())
                print("It reached step 1")
            elif self.getMenuStep() == 2:
                writeSerialPort(RIGHT_CHARACTER, serialPort)
                self.setAlreadySentFlag(True)
                print(self.getActionName())
                print("It reached step 2")
            elif self.getMenuStep() == 3:
                writeSerialPort(ENTER_CHARACTER, serialPort)
                self.setMenuStep(4)
                self.setAlreadySentFlag(False)
                print(self.getActionName())
                print("It reached step 3")
            elif self.getMenuStep() == 4:
                for character in self.getActionParameter():
                    writeSerialPort(bytes(character, 'ascii'), serialPort)
                self.setMenuStep(5)
                self.setAlreadySentFlag(False)
                print(self.getActionName())
                print("It reached step 4")
            elif self.getMenuStep() == 5:
                writeSerialPort(ENTER_CHARACTER, serialPort)
                self.setMenuStep(6)
                self.setAlreadySentFlag(False)
                self.setSendActionFlag(False)
                print(self.getActionName())
                print("It reached step 5")
                if self.getSendTwoStepsActionFlag() == True:
                    print("Entr[o al if 1")
                    if (self.getSensorSelectedFlag() == False):
                        print("Entr[o al if 2")
                        self.setSensorSelectedFlag(True)
                        self.sendTwoStepsAction()
            else:
                pass   
 
    def postProcessWriting(self, outputString):
        if self.getMenuStep() == -2:
            if self.getBackString() in outputString:
                self.setMenuStep(-1)
        if self.getMenuStep() == 0:    
            if self.getEndOfStep0String() in outputString:
                self.setMenuStep(1)
        if self.getMenuStep() == 2:
            if self.getEndOfStep2String() in outputString:
                self.setMenuStep(3)
        self.setAlreadySentFlag(False)
