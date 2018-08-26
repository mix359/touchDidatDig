<template>
    <button-box text="Oscura" icon="fa-square-o" active-color="brown" @click="onClick" :is-active="isActive"></button-box>
</template>

<script>
import ButtonBox from './../ButtonBox.vue';

export default {
	name: 'single-blank',
	props: {
		projectorId: {required: true, type: Number}
	},
	components: {ButtonBox},
	computed: {
        isActive() {
			return this.$store.state.projectors[this.projectorId].blanked;
        }
	},
	methods: {
		onClick() {
			this.$store.dispatch("sendCommandToProjector", {projectorId: this.projectorId, command: "blankToggle"});
		}
	}
}
</script>

<style>

</style>
