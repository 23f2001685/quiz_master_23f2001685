import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import store from './store'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import 'bootstrap-icons/font/bootstrap-icons.css';

router.beforeEach((to, from, next) => {
    const authToken = localStorage.getItem('auth_token');

    if ((to.path === '/admin' || to.path === '/quiz') && !authToken) {
      next('/');
    } else {
      next();
    }
  });


createApp(App)
.directive('tooltip', {
  mounted(el) {
    const tooltipTrigList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    tooltipTrigList.map(function (tooltipTrigListEl) {
      return new bootstrap.Tooltip(tooltipTrigListEl)
    })
  }
})
.use(router)
.use(store)
.mount('#app')
