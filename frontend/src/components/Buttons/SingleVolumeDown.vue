<template>
    <button-box text="Diminuisci Volume" icon="fa-volume-down" @click="onClick"></button-box>
</template>

<script>
import ButtonBox from './../ButtonBox.vue';

export default {
	name: 'single-volume-down',
	props: {
		projectorId: {required: true, type: Number}
	},
    components: {ButtonBox},
	methods: {
		onClick() {
			this.$store.dispatch("sendCommandToProjector", {projectorId: this.projectorId, command: "volumeDown"});
		}
	}
}
</script>

<style>

</style>
