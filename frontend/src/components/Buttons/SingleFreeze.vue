<template>
    <button-box text="Congela" icon="fa-snowflake-o" active-color="blue" @click="onClick" :is-active="isActive"></button-box>
</template>

<script>
import ButtonBox from './../ButtonBox.vue';

export default {
	name: 'single-freeze',
	props: {
		projectorId: {required: true, type: Number}
	},
	components: {ButtonBox},
	computed: {
        isActive() {
			return this.$store.state.projectors[this.projectorId].freezed;
        }
	},
	methods: {
		onClick() {
			this.$store.dispatch("sendCommandToProjector", {projectorId: this.projectorId, command: "freezeToggle"});
		}
	}
}
</script>

<style>

</style>
