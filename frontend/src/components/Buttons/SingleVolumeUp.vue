<template>
    <button-box text="Aumenta Volume" icon="fa-volume-up" @click="onClick"></button-box>
</template>

<script>
import ButtonBox from './../ButtonBox.vue';

export default {
	name: 'single-volume-up',
	props: {
		projectorId: {required: true, type: Number}
	},
    components: {ButtonBox},
	methods: {
		onClick() {
			this.$store.dispatch("sendCommandToProjector", {projectorId: this.projectorId, command: "volumeUp"});
		}
	}
}
</script>

<style>

</style>
