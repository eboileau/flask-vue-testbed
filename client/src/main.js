import {createApp} from 'vue'
// import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import PrimeVue from 'primevue/config'

import '@/assets/style/index.css'

import 'primevue/resources/themes/tailwind-light/theme.css'
import 'primevue/resources/primevue.min.css'
import 'primeicons/primeicons.css'

import Divider from 'primevue/divider'
import Button from 'primevue/button'
import Dropdown from 'primevue/dropdown'
import TreeSelect from 'primevue/treeselect'
import CascadeSelect from 'primevue/cascadeselect'
import MultiSelect from 'primevue/multiselect'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'

const app = createApp(App)

// app.use(createPinia())
app.use(router)
app.use(PrimeVue)

app.component('Divider', Divider)
app.component('Button', Button)
app.component('Dropdown', Dropdown)
app.component('TreeSelect', TreeSelect)
app.component('CascadeSelect', CascadeSelect)
app.component('MultiSelect', MultiSelect)
app.component('DataTable', DataTable)
app.component('Column', Column)

app.mount('#app')
