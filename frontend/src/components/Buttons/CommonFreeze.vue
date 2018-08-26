<template>
    <button-box text="Congela" active-color="blue" icon="fa-snowflake-o" :is-active="isActive" @click="onClick"></button-box>
</template>

<script>
import ButtonBox from './../ButtonBox.vue';

export default {
    name: 'common-freeze',
    components: {ButtonBox},
    computed: {
        isActive() {
			for(let i = 1; i < 4; i++) {
				if(!this.$store.state.projectors[i].freezed) {
					return false;
				}
            }

			return true;
        }
	},
	methods: {
		onClick() {
			for(let i = 1; i < 4; i++) {
				this.$store.dispatch("sendCommandToProjector", {projectorId: i, command: "freezeToggle"});
            }
		}
	}
}
</script>

<style>

</style>
