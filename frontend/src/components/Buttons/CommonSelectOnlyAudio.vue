<template>
    <button-box text="Solo Audio" icon="fa-volume-up" :is-active="isActive" @click="onClick"></button-box>
</template>

<script>
import ButtonBox from './../ButtonBox.vue';

export default {
    name: 'common-select-only-audio',
    components: {ButtonBox},
    computed: {
        isActive() {
            if(!this.$store.state.centralAudioPowered) {
                return false;
            }

			for(let i = 1; i < 4; i++) {
				if(this.$store.state.projectors[i].powered) {
					return false;
				}
            }

			return true;
        }
	},
	methods: {
		onClick() {
			for(let i = 1; i < 4; i++) {
				this.$store.dispatch("sendCommandToProjector", {projectorId: i, command: "powerOff"});
            }
            
            this.$store.dispatch("sendCommandToCentralGPIO", {command: "centralAudioPowerOn"});
		}
	}
}
</script>

<style>

</style>
