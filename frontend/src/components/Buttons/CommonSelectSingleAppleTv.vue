<template>
    <button-box text="Apple Tv Singole"  icon="fa-apple" :is-active="isActive" @click="onClick"></button-box>
</template>

<script>
import ButtonBox from './../ButtonBox.vue';

export default {
    name: 'common-select-single-apple-tv',
    components: {ButtonBox},
    computed: {
        isActive() {
			for(let i = 1; i < 4; i++) {
				if(!this.$store.state.projectors[i].powered || this.$store.state.projectors[i].source !== this.$definitions.PROJECTOR_SOURCE_HDMI1) {
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

				this.$store.dispatch("sendCommandToProjector", {projectorId: i, command: "sourceSet:" + this.$definitions.PROJECTOR_SOURCE_HDMI1});
			}
		}
	}
}
</script>

<style>

</style>
