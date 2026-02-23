import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { api } from './library/api'
import { urls } from './library/urls'
import { useProcess } from './stores/process'

const app = createApp(App)

app.use(createPinia())
app.use(router)

await api.head(urls.csrf)

const processStore = useProcess()
app.config.globalProperties.$process = processStore

app.mount('#app')
