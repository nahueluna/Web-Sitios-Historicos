import './assets/main.css'

// Import custom styles
import './styles/custom.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import vue3GoogleLogin from 'vue3-google-login'

import App from './App.vue'
import router from './router'
import * as BootstrapVueNext from 'bootstrap-vue-next'

// Importar CSS
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-next/dist/bootstrap-vue-next.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(BootstrapVueNext.BootstrapVueNext)

app.use(vue3GoogleLogin, {
  clientId: "293951950999-3o52dhr2ouqr0rdp54lcrplj9d9m7h82.apps.googleusercontent.com"
})


import { useSessionStore } from './stores/sessionStore';

// Restaurar sesión al iniciar la aplicación
const sessionStore = useSessionStore();
sessionStore.restoreSession().then(success => {
  if (success) {
    console.log('Sesión restaurada al iniciar la app');
  }
});

app.mount('#app')
