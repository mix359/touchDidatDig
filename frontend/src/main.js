import Vue from 'vue'
import 'font-awesome/css/font-awesome.min.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'mdbvue/build/css/mdb.css';
import App from './App.vue'
import store from './store'
import definitions from './definitions';

Vue.config.productionTip = false
Vue.use(definitions);

new Vue({
  store,
  render: h => h(App)
}).$mount('#app')
