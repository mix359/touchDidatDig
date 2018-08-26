<template>
    <button-box text="Spegni" active-color="red darken-2" icon="fa-power-off" :is-active="isActive" @click="onClick"></button-box>
</template>

<script>
import ButtonBox from './../ButtonBox.vue';

export default {
    name: 'single-turn-off',
    components: {ButtonBox},
    props: {
		projectorId: {required: true, type: Number}
	},
    computed: {
        isActive() {
			return !this.$store.state.projectors[this.projectorId].powered;
        }
	},
	methods: {
		onClick() {
			this.$store.dispatch("sendCommandToProjector", {projectorId: this.projectorId, command: "powerOff"});
            
            if(this.projectorId === 2) {
                this.$store.dispatch("sendCommandToCentralGPIO", {command: "centralAudioPowerOff"});
            }
		}
	}
}
</script>

<style>

</style>
