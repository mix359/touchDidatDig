<template>
    <button-box text="Muto" icon="fa-volume-off" active-color="orange darken-1" @click="onClick" :is-active="isActive"></button-box>
</template>

<script>
import ButtonBox from './../ButtonBox.vue';

export default {
	name: 'single-mute',
	props: {
		projectorId: {required: true, type: Number}
	},
	components: {ButtonBox},
	computed: {
        isActive() {
			return this.$store.state.projectors[this.projectorId].muted;
        }
	},
	methods: {
		onClick() {
			this.$store.dispatch("sendCommandToProjector", {projectorId: this.projectorId, command: "volumeToggle"});
		}
	}
}
</script>

<style>

</style>
