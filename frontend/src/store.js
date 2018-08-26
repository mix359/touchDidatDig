import Vue from 'vue'
import Vuex from 'vuex'
import {
	connect
} from 'mqtt'

Vue.use(Vuex)

const mqttPrefix = "test";
const mqttClient = connect('mqtt://192.168.1.130:9001');
//const mqttClient = connect('mqtt://rdisplay1.local:9001');
//const mqttClient = connect('mqtt://test.mosquitto.org:8080');

const store = new Vuex.Store({
	state: {
		page: 0,
		sendingCommand: false,
		errorSendingCommand: false,
		projectors: {
			1: {
				name: "Sinistra",
				comunicationError: false,
				powered: false,
				freezed: false,
				muted: false,
				blanked: false,
				source: 0,
				vol: 0
			},
			2: {
				name: "Centro",
				comunicationError: false,
				powered: false,
				freezed: false,
				muted: false,
				blanked: false,
				source: 0,
				vol: 0
			},
			3: {
				name: "Destra",
				comunicationError: false,
				powered: false,
				freezed: false,
				muted: false,
				blanked: false,
				source: 0,
				vol: 0
			}
		},
		videoMatrixes: {
			1: {
				name: "Sinistra",
				comunicationError: false,
				channel: 0
			},
			2: {
				name: "Centro",
				comunicationError: false,
				channel: 0
			},
			3: {
				name: "Destra",
				comunicationError: false,
				channel: 0
			}
		},
		centralAudioPowered: false
	},
	mutations: {
		handleProjectorMessage(state, payload) {
			if (typeof payload.projectorId === "undefined" ||
				typeof state.projectors[payload.projectorId] === "undefined" ||
				typeof payload.key === "undefined" ||
				typeof payload.value === "undefined") {
				return;
			}

			let projector = state.projectors[payload.projectorId];

			switch (payload.key) {
				case "on":
					projector.powered = payload.value == "1";
					break;

				case "freeze":
					projector.freezed = payload.value == "1";
					break;

				case "mute":
					projector.muted = payload.value == "1";
					break;

				case "blank":
					projector.blanked = payload.value == "1";
					break;

				case "source":
					projector.source = Number(payload.value);
					break;

				case "vol":
					projector.vol = Number(payload.value);
					break;
			}
		},
		handleVideoMatrixMessage(state, payload) {
			if (typeof payload.videoMatrixId === "undefined" ||
				typeof state.videoMatrixes[payload.videoMatrixId] === "undefined" ||
				typeof payload.key === "undefined" ||
				typeof payload.value === "undefined") {
				return;
			}

			let videoMatrix = state.videoMatrixes[payload.videoMatrixId];

			switch (payload.key) {
				case "channel":
					videoMatrix.channel = Number(payload.value);
					break;
			}
		},
		handleCentralGPIOMessage(state, payload) {
			if (typeof payload.key === "undefined" || typeof payload.value === "undefined") {
				return;
			}

			switch (payload.key) {
				case "centralAudioPower":
					state.centralAudioPowered = payload.value == "1";
					break;
			}
		},
		setSendingCommand(state) {
			state.sendingCommand = true;
			state.errorSendingCommand = false;
		},
		setFinishSendingCommand(state) {
			state.sendingCommand = false;
		},
		setErrorSendingCommand(state) {
			state.sendingCommand = false;
			state.errorSendingCommand = true;
		},
		changePage(state, page) {
			state.page = page;
		}
	},
	actions: {
		sendCommandToProjector({commit}, payload) {
			if (typeof payload.projectorId === "undefined" || typeof payload.command === "undefined") {
				return;
			}
			
			commit("setSendingCommand");
			mqttClient.publish(mqttPrefix + "/projector/" + payload.projectorId, payload.command, (error) => {
				if(error) {
					commit("setErrorSendingCommand");
				} else {
					commit("setFinishSendingCommand");
				}
			});
		},
		sendCommandToVideoMatrix({commit}, payload) {
			if (typeof payload.videoMatrixId === "undefined" || typeof payload.command === "undefined") {
				return;
			}
			
			commit("setSendingCommand");
			mqttClient.publish(mqttPrefix + "/videoMatrix/" + payload.videoMatrixId, payload.command, (error) => {
				if(error) {
					commit("setErrorSendingCommand");
				} else {
					commit("setFinishSendingCommand");
				}
			});
		},
		sendCommandToCentralGPIO({commit}, payload) {
			if (typeof payload.command === "undefined") {
				return;
			}
			
			commit("setSendingCommand");
			mqttClient.publish(mqttPrefix + "/centralGPIO", payload.command, (error) => {
				if(error) {
					commit("setErrorSendingCommand");
				} else {
					commit("setFinishSendingCommand");
				}
			});
		},
		requestAllStatusUpdate({dispatch}) {
			if(!mqttClient.connected) {
				return;
			}

			for(let i = 1; i < 4; i++) {
				dispatch("sendCommandToProjector",{projectorId: i, command: "sendAll"});
				dispatch("sendCommandToVideoMatrix",{videoMatrixId: i, command: "sendAll"});
			}
		}
	}
});



mqttClient.on('error', function (e) {
	console.log("errore mqtt", e);
	//mqttClient.subscribe('test/matrix/1')
})

let updateAllInterval;
mqttClient.on('connect', function () {
	console.log("subscribing to mqtt");
	mqttClient.subscribe(mqttPrefix + '/projector/+/+');
	mqttClient.subscribe(mqttPrefix + '/videoMatrix/+/+');
	mqttClient.subscribe(mqttPrefix + '/centralGPIO/+');

	setTimeout(() => store.dispatch("requestAllStatusUpdate"), 500);
	updateAllInterval = setInterval(() => store.dispatch("requestAllStatusUpdate"), 300000);
})

mqttClient.on("close", () => {
	clearInterval(updateAllInterval);
})

mqttClient.on('message', function (topic, message) {
	let topicExploded = topic.split("/");
	if (topicExploded.length < 2 || topicExploded[0] !== mqttPrefix) {
		return;
	}

	console.log("messaggio mqtt", topic, message.toString());

	if (topicExploded[1] === "projector" && topicExploded.length === 4) {
		if (topicExploded[2] === "*") {
			for (let k in store.projectors) {
				try {
					store.commit("handleProjectorMessage", {
						projectorId: k,
						key: topicExploded[3],
						value: message
					});
				} catch (err) {}
			}
		} else {
			try {
				store.commit("handleProjectorMessage", {
					projectorId: Number(topicExploded[2]),
					key: topicExploded[3],
					value: message
				});
			} catch (err) {}
		}
	}

	if (topicExploded[1] === "videoMatrix" && topicExploded.length === 4) {
		if (topicExploded[2] === "*") {
			for (let k in self.videoMatrixes) {
				try {
					store.commit("handleVideoMatrixMessage", {
						videoMatrixId: k,
						key: topicExploded[3],
						value: message
					});
				} catch (err) {}
			}
		} else {
			try {
				store.commit("handleVideoMatrixMessage", {
					videoMatrixId: Number(topicExploded[2]),
					key: topicExploded[3],
					value: message
				});
			} catch (err) {}
		}
	}
})



export default store;
