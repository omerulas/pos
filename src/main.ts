import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { api } from './library/api'
import { urls } from './library/urls'
import { useProcess } from './stores/process'
import { useOrderData } from './stores/order'

const app = createApp(App)

app.use(createPinia())
app.use(router)

const processStore = useProcess()
app.config.globalProperties.$process = processStore

const orderStore = useOrderData()
app.config.globalProperties.$order = orderStore

await api.head(urls.csrf)

app.mount('#app')
