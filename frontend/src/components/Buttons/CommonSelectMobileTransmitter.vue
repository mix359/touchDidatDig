<template>
    <button-box text="Trasmettitore Mobile"  icon="fa-square" :is-active="isActive" @click="onClick"></button-box>
</template>

<script>
import ButtonBox from './../ButtonBox.vue';

export default {
    name: 'common-select-mobile-transmitter',
    components: {ButtonBox},
    computed: {
        isActive() {
			for(let i = 1; i < 4; i++) {
				if(!this.$store.state.projectors[i].powered || this.$store.state.projectors[i].source !== this.$definitions.PROJECTOR_SOURCE_HDMI2) {
					return false;
				}

				if(this.$store.state.videoMatrixes[i].channel !== this.$definitions.VIDEO_MATRIX_CHANNEL_MOBILE_TRANSMITTER) {
					return false;
				}
			}

			return true;
        }
	},
	methods: {
		onClick() {
			for(let i = 1; i < 4; i++) {
				if(!this.$store.state.projectors[i].powered) {
					this.$store.dispatch("sendCommandToProjector", {projectorId: i, command: "powerOn"});
				}

				if(!this.$store.state.centralAudioPowered) {
					this.$store.dispatch("sendCommandToCentralGPIO", {command: "centralAudioPowerOn"});
				}

				this.$store.dispatch("sendCommandToProjector", {projectorId: i, command: "sourceSet:" + this.$definitions.PROJECTOR_SOURCE_HDMI2});
				this.$store.dispatch("sendCommandToVideoMatrix", {videoMatrixId: i, command: "changeChannel:" + this.$definitions.VIDEO_MATRIX_CHANNEL_MOBILE_TRANSMITTER});
			}
		}
	}
}
</script>

<style>

</style>
