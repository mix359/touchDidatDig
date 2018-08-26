<template>
	<navbar class="navbar-dark blue darken-3">
	<!-- <navbar SideClass="navbar navbar-expand-lg navbar-dark blue darken-3" [containerInside]="false"> -->
		<mdb-navbar-brand href="#">Controllo Sala Multimediale</mdb-navbar-brand>
		<navbar-collapse>
			<div class="collapse navbar-collapse">
				<ul class="navbar-nav mr-auto mt-lg-0">
					<li class="nav-item ripple-parent" :class="{active: $store.state.page === 0}" @click="wave">
						<a class="nav-link" @click.prevent="$store.commit('changePage', 0)">Home</a>
					</li>
					<li class="nav-item ripple-parent" :class="{active: $store.state.page === 1}" @click="wave">
						<a class="nav-link" @click.prevent="$store.commit('changePage', 1)">Proiettore Sinistra</a>
					</li>
					<li class="nav-item ripple-parent" :class="{active: $store.state.page === 2}" @click="wave">
						<a class="nav-link" @click.prevent="$store.commit('changePage', 2)">Proiettore Centro</a>
					</li>
					<li class="nav-item ripple-parent" :class="{active: $store.state.page === 3}" @click="wave">
						<a class="nav-link" @click.prevent="$store.commit('changePage', 3)">Proiettore Destra</a>
					</li>
				</ul>
				<ul class="navbar-nav">
					<li class="nav-item">
						<i class="fa fa-spinner py-2" v-if="$store.state.sendingCommand"></i>
						<i class="fa fa-exclamation-triangle py-2" v-if="$store.state.errorSendingCommand"></i>
					</li>
					<li class="nav-item">
						<a class="nav-link" href="#">Spegni</a>
					</li>
				</ul>
			</div>
		</navbar-collapse>
	</navbar>
</template>

<script>
import { Navbar, NavbarItem, NavbarNav, NavbarCollapse, waves, mdbNavbarBrand } from 'mdbvue';

export default {
	name: "app-navbar",
	components: {
		Navbar, NavbarItem, NavbarNav, NavbarCollapse, mdbNavbarBrand
	},
	mixins: [waves],
	data: () => ({
        waves: true
	})
};
</script>

<style>
</style>
