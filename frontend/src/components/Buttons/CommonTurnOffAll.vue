<template>
    <button-box text="Spegni" active-color="red darken-2" icon="fa-power-off" :is-active="isActive" @click="onClick"></button-box>
</template>

<script>
import ButtonBox from './../ButtonBox.vue';

export default {
    name: 'common-turn-off-all',
    components: {ButtonBox},
    computed: {
        isActive() {
			for(let i = 1; i < 4; i++) {
				if(this.$store.state.projectors[i].powered) {
					return false;
				}
            }
            
            if(this.$store.state.centralAudioPowered) {
                return false;
            }

			return true;
        }
	},
	methods: {
		onClick() {
			for(let i = 1; i < 4; i++) {
				this.$store.dispatch("sendCommandToProjector", {projectorId: i, command: "powerOff"});
            }
            
            this.$store.dispatch("sendCommandToCentralGPIO", {command: "centralAudioPowerOff"});
		}
	}
}
</script>

<style>

</style>
