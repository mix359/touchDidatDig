import threading, socket, time
from mqttCom import MqttCom

class VideoMatrixCom(threading.Thread, MqttCom):
    localIpInBytes = None
    currentMatrixInfo = None

    def __init__(self, matrixMac, matrixIp, mqttPath, mqttServer, mqttPort=1883):
        self.matrixMac = bytes.fromhex(matrixMac.replace(":","").replace("-",""))
        self.matrixIp = matrixIp
        self.matrixPort = 9001
        self.replyServerPort = 0
        try:
            self._prepareLocalIpInBytes()
        except BaseException as e:
            raise Exception("Error retriving the local ip: {}".format(e))
        
        MqttCom.__init__(self, mqttPath, mqttServer, mqttPort)
        threading.Thread.__init__(self)
        
    def run(self):
        self.mqttStart()

        try:
            self._startReplyServer()
        except:
            self.log("Error initializing the reply server")
            return

        self.nextStatusUpdate = time.process_time() + 1

        while(True):
            if(time.process_time() >= self.nextStatusUpdate):
                try:
                    self.requestStatus()
                except BaseException as e:
                    self.log("error requesting the matrix status: {}".format(e))
                    continue

                time.sleep(0.1)
                self.nextStatusUpdate = time.process_time() + 5

            try:
                self._handleReplyServer()
            except BaseException as e:
                self.log("error handling the matrix reply: {}".format(e))
                continue

    def requestStatus(self):
        msg = self._composeMatrixMessage(b'\x74\x00\xfe\x00\x0b\x09', b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', True)
        try:
            self._sendMatrixMessage(msg)
        except BaseException as e:
            raise Exception("Error requesting the status to the matrix {}".format(e))
       # self.log("-sending status request: " +  ' '.join(hex(letter) for letter in msg))

    def sendChangeRxChannel(self, channel):
        msg = self._composeMatrixMessage(b'\x74\x00\x50\x00\x09\x59', b'\x00' + channel.to_bytes(1, byteorder='big') + (channel + 99).to_bytes(1, byteorder='big'))
        try:
            self._sendMatrixMessage(msg)
        except BaseException as e:
            raise Exception("Error sending the change channel to {} command to the matrix: {}".format(channel, e))
        self.nextStatusUpdate = time.process_time() + 0.5
        self.log("-sending change channel: " + ' '.join(hex(letter) for letter in msg))

    def sendAllInfo(self):
        self.requestStatus()
        time.sleep(0.1)
        self._handleReplyServer()
        self.nextStatusUpdate = time.process_time() + 5

        if(self.currentMatrixInfo is None):
            return

        try:
            self.mqttPublish(self.currentMatrixInfo['channel'], "/channel")
        except BaseException as e:
            raise Exception("Error publishing the channel information: {}".format(e))

    def mqttMessageReceived(self, client, userdata, msg):
        try:
            if(msg.payload == b'sendAll'):
                self.sendAllInfo()
            elif(msg.payload[0:14] == b'changeChannel:'):
                self.sendChangeRxChannel(int(msg.payload[14:]))
        except BaseException as e:
            self.log(e)

    def _composeMatrixMessage(self, command, payload, noMac=False):
        if self.localIpInBytes is None:
            raise TypeError("Invalid local ip")
        
        msg = bytes("IPTV_CMD", "utf-8")
        msg += self.localIpInBytes
        msg += self.replyServerPort.to_bytes(2, byteorder='big')
        msg += command
        if(not noMac):
            msg += self.matrixMac
        msg += payload
        return msg

    def _sendMatrixMessage(self, msg):
        matrixSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        matrixSock.connect((self.matrixIp, self.matrixPort))
        matrixSock.send(msg)
        matrixSock.close()

    def _startReplyServer(self):
        self._replyServerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._replyServerSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._replyServerSock.bind(('', 0))
        self._replyServerSock.listen(5)
        self._replyServerSock.setblocking(False)
        self.replyServerPort = self._replyServerSock.getsockname()[1]
        self.log("-started reply server on port {}".format(self.replyServerPort))

    def _handleReplyServer(self):
        try:
            conn, client_address = self._replyServerSock.accept()
            self.log("-accepted connection from {}".format(client_address))
        except BaseException as e:
            return
            #raise Exception("Error accepting the connection: {}".format(e))
        
        while True:
            try:
                data = conn.recv(1024)
            except:
                break
            if not data:
                break

            cmd = data[14:20]
            payload = data[20:]

            self.log("--received data: {} {}".format(cmd, payload))

            if cmd == b'\x74\x00\xff\x00\x34\x33':
                self._updateMatrixInfo(payload)

    def _updateMatrixInfo(self, payload):
        data = {}
        data['name'] = payload[0:32].decode('utf-8')
        data['ip'] = str(int.from_bytes([payload[32]], byteorder='big')) + "." + str(int.from_bytes([payload[33]], byteorder='big')) + "." + str(int.from_bytes([payload[34]], byteorder='big')) + "." + str(int.from_bytes([payload[35]], byteorder='big'))
        data['port'] = int.from_bytes(payload[36:38], byteorder='big')
        data['channel'] = int.from_bytes([payload[39]], byteorder='big')
        data['mac'] = payload[44:49].hex()
        data['id'] = int.from_bytes([payload[50]], byteorder='big')
        #self.log("matrix data to update {}".format(data.items()))

        if(self.currentMatrixInfo is None or self.currentMatrixInfo['channel'] != data['channel']):
            try:
                self.mqttPublish(data['channel'], "/channel")
            except BaseException as e:
                raise Exception("Error publishing the channel: {}".format(e))
            self.log("---send channel: {}".format(data['channel']))

        self.currentMatrixInfo = data
            
    def _prepareLocalIpInBytes(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        localIp = s.getsockname()[0]
        s.close()

        self.log("local ip {}".format(localIp))
        if(localIp != ""):
            localIpSplitted = localIp.split(".")
            if(len(localIpSplitted) == 4):
                self.localIpInBytes = b''
                for i in range(4):
                    self.localIpInBytes += bytes([int(localIpSplitted[i])])

    def stop(self):
        self.mqttStop()
        self._replyServerSock.close()