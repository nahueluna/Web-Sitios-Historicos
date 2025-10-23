import './assets/main.css'

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

app.mount('#app')
