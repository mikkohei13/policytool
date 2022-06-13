import {createApp, nextTick} from 'vue'
import './tailwind.css'
import App from './App.vue'
import {routes} from './routes.js'
import {createRouter, createWebHistory} from 'vue-router'
import {createPinia} from 'pinia'
import {useAuth} from "@/store/auth";

const app = createApp(App)

const router = createRouter({
    history: createWebHistory(),
    routes,
})

// use the current title set in the index.html as the default
const DEFAULT_TITLE = document.title;
router.afterEach(async (to) => {
    await nextTick()
    let title = DEFAULT_TITLE
    if (!!to.meta.title) {
        title = `${DEFAULT_TITLE} - ${to.meta.title}`
    }
    document.title = title
});

app.use(createPinia())
app.use(router)
app.mount('#app')

// update the user details if we have a persisted token
const {refreshDetails} = useAuth()
await refreshDetails()
