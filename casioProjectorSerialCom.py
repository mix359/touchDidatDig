import threading, serial, time
from mqttCom import MqttCom

class CasioProjectorSerialCom(threading.Thread, MqttCom):
    WAITING_PROJECTOR_RESPONSE_TIMEOUT = 5
    WAIT_TIME_AFTER_COMMAND_TO_PROJECTOR = 0.2
    WAIT_TIME_AFTER_POWER_COMMAND_TO_PROJECTOR = 1.5
    SERIAL_CONNECTION_RETRY_MAX_DELAY = 120

    serialPort = None
    nextSerialConnectionRetry = 0
    serialConnectionRetryDelay = 1
    waitingSerialResponse = False
    currentSerialReadOperation = 0
    waitTimerCommandElaboration = 0
    lastSerialReadTry = 0
    serialCommunicationFail = False
    projectorState = {'on': False, 'freeze': False, 'mute': False, 'blank': False, 'source': 0, 'vol': 0}

    def __init__(self, comPath, mqttPath, mqttServer, mqttPort=1883):
        self.comPath = comPath
        MqttCom.__init__(self, mqttPath, mqttServer, mqttPort)
        threading.Thread.__init__(self)

    def run(self):
        self.mqttStart()

        while True:
            try:
                self._prepareSerialPort()
            except:
                self._updateSerialCommunicationFailStatus(True)
                continue

            try:
                self._sendNextProjectorStateReadCommandToSerial()
            except:
                self.log("Error sending the next status command to the serial")
            
            if(self.serialPort.inWaiting() > 0):
                try:
                    self._readProjectorStateFromSerial()
                except BaseException as e:
                    self.log(e)
                    continue
                
                self.lastSerialReadTry = time.process_time()
                self._updateSerialCommunicationFailStatus(False)
            elif(self.waitingResponse and ((time.process_time() - self.lastSerialReadTry) > (self.WAITING_PROJECTOR_RESPONSE_TIMEOUT * 1000))):
                self._updateSerialCommunicationFailStatus(True)
                self.currentReadOperation = 0
                self.waitingResponse = False
                self.lastSerialReadTry = time.process_time()

    def _sendNextProjectorStateReadCommandToSerial(self):
        if self.waitingSerialResponse:
            return

        self.currentSerialReadOperation += 1
        if self.currentSerialReadOperation > 6 or not self.projectorState['on']:
            self.currentSerialReadOperation = 1

        if self.currentSerialReadOperation == 1:
            self.serialPort.write(b'PWR?')
        elif self.currentSerialReadOperation == 2:
            self.serialPort.write(b'FRZ?')
        elif self.currentSerialReadOperation == 3:
            self.serialPort.write(b'MUT?')
        elif self.currentSerialReadOperation == 4:
            self.serialPort.write(b'BLK?')
        elif self.currentSerialReadOperation == 5:
            self.serialPort.write(b'SRC?')
        elif self.currentSerialReadOperation == 6:
            self.serialPort.write(b'VOL?')
        else:
            return
        
        self.waitingSerialResponse = True

    def _readProjectorStateFromSerial(self):
        try:
            serialData = self.serialPort.read(self.serialPort.inWaiting()).decode('utf-8')
        except BaseException as e:
            raise Exception("Error reading from serial port: {}".format(e))

        if(self.currentSerialReadOperation < 1 or serialData == "" or serialData == "\n" or serialData == "\n\r"):
            return

        serialDataSplitted = serialData.split(",")
        if(len(serialDataSplitted) < 2 or serialDataSplitted[1] == ""):
            return

        if self.currentSerialReadOperation == 1:
            self.updateProjectorState('on', serialDataSplitted[1] == 1)

            if not self.projectorState['on']:
                self.updateProjectorState('freeze', False)
                self.updateProjectorState('mute', False)
                self.updateProjectorState('blank', False)
                self.updateProjectorState('source', 0)
                self.updateProjectorState('vol', 0)
        elif self.currentSerialReadOperation == 2:
            self.updateProjectorState('freeze', serialDataSplitted[1] == 1)
        elif self.currentSerialReadOperation == 3:
            self.updateProjectorState('mute', serialDataSplitted[1] == 1)
        elif self.currentSerialReadOperation == 4:
            self.updateProjectorState('blank', serialDataSplitted[1] == 1)
        elif self.currentSerialReadOperation == 5:
            self.updateProjectorState('source', int(serialDataSplitted[1]))
        elif self.currentSerialReadOperation == 6:
            self.updateProjectorState('vol', int(serialDataSplitted[1]))
        
        self.waitingResponse = False

    def mqttMessageReceived(self, client, userdata, msg):
        if msg.payload == b'sendAll':
            try:
                self.sendAllInfo()
            except BaseException as e:
                self.log(e)
        elif not self.serialPort.isOpen:
            return
        
        try:
            self._sendCommandToProjector(msg.payload.decode('utf-8'))
        except BaseException as e:
            self.log("Error sending the command {} to the projector: {}".format(msg.payload.decode('utf-8'), e))

    def _sendCommandToProjector(self, msg):
        if not self.projectorState['on'] and msg != "powerOn" and msg != "powerToggle":
            return

        if not self.serialPort.isOpen:
            return

        self.currentSerialReadOperation = 0
        self.waitingResponse = False

        if msg == "powerOn":
            self.serialPort.write(b'PWR1')
        elif msg == "powerOff":
            self.serialPort.write(b'PWR0')
        elif msg == "powerToggle":
            self.serialPort.write(b'PWR' + ('1' if self.projectorState['power'] else '0') )
        elif msg[0:9] == "powerSet:":
             self.serialPort.write(b'PWR' + bytes(msg[9:], "utf-8"))
        elif msg == "freezeOn":
            self.serialPort.write(b'PWR1')
        elif msg == "freezeOff":
            self.serialPort.write(b'PWR0')
        elif msg == "freezeToggle":
            self.serialPort.write(b'PWR' + ('1' if self.projectorState['freeze'] else '0') )
        elif msg[0:10] == "freezeSet:":
             self.serialPort.write(b'PWR' + bytes(msg[10:], "utf-8"))
        elif msg == "muteOn":
            self.serialPort.write(b'MUT1')
        elif msg == "muteOff":
            self.serialPort.write(b'MUT0')
        elif msg == "muteToggle":
            self.serialPort.write(b'MUT' + ('1' if self.projectorState['mute'] else '0') )
        elif msg[0:8] == "muteSet:":
             self.serialPort.write(b'MUT' + bytes(msg[8:], "utf-8"))
        elif msg == "blankOn":
            self.serialPort.write(b'BLK1')
        elif msg == "blankOff":
            self.serialPort.write(b'BLK0')
        elif msg == "blankToggle":
            self.serialPort.write(b'BLK' + ('1' if self.projectorState['blank'] else '0') )
        elif msg[0:9] == "blankSet:":
             self.serialPort.write(b'BLK' + bytes(msg[9:], "utf-8"))
        elif msg[0:10] == "sourceSet:":
             self.serialPort.write(b'SRC' + bytes(msg[10:], "utf-8"))
        elif msg == "volUp":
            self.serialPort.write(b'VLP')
        elif msg == "volDown":
            self.serialPort.write(b'VLM')
        elif msg[0:7] == "volSet:":
             self.serialPort.write(b'VOL' + bytes(msg[7:], "utf-8"))

    def sendAllInfo(self):
        try:
            self.mqttPublish(self.serialCommunicationFail, "/connectionFail")
        except BaseException as e:
            raise Exception("Error publishing the connection fail status {}: {}".format(self.serialCommunicationFail, e))

        for key in self.projectorState.keys():
            try:
                self.mqttPublish(self.projectorState[key], "/" + key)
            except BaseException as e:
                raise Exception("Error publishing the projector state {} for {}: {}".format(self.projectorState[key], key, e))

    def updateProjectorState(self, key, val):
        if self.projectorState[key] != val:
            try:
                self.mqttPublish(self.projectorState[key], "/" + key)
            except BaseException as e:
                raise Exception("Error publishing the projector state {} for {}: {}".format(self.projectorState[key], key, e))

        self.projectorState[key] = val
        
    def _updateSerialCommunicationFailStatus(self, status):
        if(status != self.serialCommunicationFail):
            try:
                self.mqttPublish(status, "/connectionFail")
            except BaseException as e:
                self.log("Error publishing the connection fail status {}: {}".format(self.serialCommunicationFail, e))
                return

        self.serialCommunicationFail = status

    def _prepareSerialPort(self):
        if(self.serialPort is None):
            try:
                self.serialPort = serial.Serial(self.comPath, timeout=1)
            except BaseException as e:
                raise Exception("Connection to the serial port " + self.comPath + " failed: {}".format(e))

        if(not self.serialPort.isOpen()):
            if(time.process_time() < self.nextSerialConnectionRetry):
                raise Exception("The serial connection is unavailable, waiting the reconnection")

            try:
                self.serialPort.open()
                self.serialConnectionRetryDelay = 1
            except BaseException as e:
                self.serialConnectionRetryDelay = min(
                    self.serialConnectionRetryDelay * 2,
                    self.SERIAL_CONNECTION_RETRY_MAX_DELAY,
                )
                
                self.nextSerialConnectionRetry = time.process_time() + self.serialConnectionRetryDelay
                raise Exception("Connection to the serial port " + self.comPath + " failed {}".format(e))

    def stop(self):
        self.mqttStop()
        if self.serialPort.isOpen:
            self.serialPort.close()