<template>
    <button-box text="Apple Tv Comune"  icon="fa-apple" :is-active="isActive" @click="onClick"></button-box>
</template>

<script>
import ButtonBox from './../ButtonBox.vue';

export default {
    name: 'single-select-central-apple-tv',
	components: {ButtonBox},
	props: {
		projectorId: {required: true, type: Number}
	},
    computed: {
        isActive() {
			return this.$store.state.projectors[this.projectorId].powered && 
			this.$store.state.projectors[this.projectorId].source === this.$definitions.PROJECTOR_SOURCE_HDMI2 &&
			this.$store.state.videoMatrixes[this.projectorId].channel === this.$definitions.VIDEO_MATRIX_CHANNEL_APPLE_TV;
        }
	},
	methods: {
		onClick() {
			if(!this.$store.state.projectors[this.projectorId].powered) {
				this.$store.dispatch("sendCommandToProjector", {projectorId: this.projectorId, command: "powerOn"});
			}

			if(!this.$store.state.centralAudioPowered && this.projectorId === 2) {
				this.$store.dispatch("sendCommandToCentralGPIO", {command: "centralAudioPowerOn"});
			}

			this.$store.dispatch("sendCommandToProjector", {projectorId: this.projectorId, command: "sourceSet:" + this.$definitions.PROJECTOR_SOURCE_HDMI2});
			this.$store.dispatch("sendCommandToVideoMatrix", {videoMatrixId: this.projectorId, command: "changeChannel:" + this.$definitions.VIDEO_MATRIX_CHANNEL_APPLE_TV});
		}
	}
}
</script>

<style>

</style>
