import paho.mqtt.client as mqtt

class MqttCom:
    def __init__(self, mqttPath, mqttServer, mqttPort=1883):
        self.mqttPath = mqttPath
        self.mqttServer = mqttServer
        self.mqttPort = mqttPort
        self.mqttStarted = False
        self._mqttClient = mqtt.Client()
        self._mqttClient.on_connect = self.mqttConnected
        self._mqttClient.on_message = self.mqttMessageReceived

    def mqttStart(self):
        if(self.mqttStarted):
            return
        
        #self._mqttClient.on_log = lambda client, userdata, level, err: print("error from mqtt client: {}".format(err))
        self._mqttClient.connect_async(self.mqttServer, self.mqttPort, 30)
        self._mqttClient.loop_start()
        self.log("connecting to {0}".format(self.mqttServer))
        self.mqttStarted = True

    def mqttPublish(self, msg, path=""):
        self._mqttClient.publish(self.mqttPath + path, msg)

    def mqttConnected(self, client, userdata, flags, rc):
        self.log("Connected with result code "+str(rc))
        self._mqttClient.subscribe(self.mqttPath)
        self.log("subscribing to {0}".format(self.mqttPath))

    def mqttMessageReceived(self, client, userdata, msg):
        self.log(msg.topic+" "+str(msg.payload))

    def mqttStop(self):
        if(not self.mqttStarted):
            return

        self._mqttClient.loop_stop()
        self._mqttClient.disconnect()
        self.mqttStarted = False

    def log(self, msg):
        print(msg)
