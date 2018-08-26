<template>
	<div id="app">
		<app-navbar></app-navbar>
    	<div class="container-fluid my-2">
        	<home v-if="$store.state.page === 0"></home>
			<projector v-if="$store.state.page > 0" :projector-id="$store.state.page"></projector>
    	</div>
    </div>
</template>

<script>
import AppNavbar from "./components/AppNavbar.vue";
import Home from "./components/Home.vue";
import Projector from "./components/Projector.vue";

export default {
  name: "app",
  components: {
	AppNavbar,
	Home,
    Projector
  }
};
</script>

<style>
body {
  padding: 0;
  margin: 0;
  background: #0d47a1;
  color: white;
}
</style>
