import { Injectable } from '@angular/core';
import { connect } from 'mqtt';

@Injectable({
  providedIn: 'root'
})
export class MqttComService {

  constructor() {
    const mqttClient = connect('mqtt://rdisplay1.local')
    mqttClient.on('connect', function () {
      mqttClient.subscribe('test/matrix/1')
    })

    mqttClient.on('message', function (topic, message) {
      // message is Buffer
      console.log("messaggio", topic, message.toString())
    })
  }

  
}
