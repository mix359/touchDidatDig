<template>
    <button-box text="Oscura" icon="fa-square-o" active-color="brown" :is-active="isActive" @click="onClick"></button-box>
</template>

<script>
import ButtonBox from './../ButtonBox.vue';

export default {
    name: 'common-blank',
    components: {ButtonBox},
    computed: {
        isActive() {
			for(let i = 1; i < 4; i++) {
				if(!this.$store.state.projectors[i].blanked) {
					return false;
				}
            }

			return true;
        }
	},
	methods: {
		onClick() {
			for(let i = 1; i < 4; i++) {
				this.$store.dispatch("sendCommandToProjector", {projectorId: i, command: "blankToggle"});
            }
		}
	}
}
</script>

<style>

</style>
