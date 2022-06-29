import {createApp, nextTick} from 'vue'
import './tailwind.css'
import App from './App.vue'
import {routes} from './routes.js'
import {createRouter, createWebHistory} from 'vue-router'
import {createPinia} from 'pinia'
import {useAuth} from '@/store/auth'
import VueFeather from 'vue-feather'
import Notifications from '@kyvg/vue3-notification'
import {storeToRefs} from 'pinia/dist/pinia'

const app = createApp(App)
// register VueFeather so that it's available for all components implicitly
app.component('VueFeather', VueFeather)

const router = createRouter({
    history: createWebHistory(),
    routes,
})

app.use(Notifications)
app.use(createPinia())
app.use(router)
app.mount('#app')

const auth = useAuth()
const {refreshDetails} = auth
const {notLoggedIn} = storeToRefs(auth)
// update the user details if we have a persisted token
refreshDetails().then()

router.beforeEach((to) => {
    // if the route we're going to is auth only, redirect to the login route
    if (to.meta.auth && notLoggedIn.value) {
        return {name: 'login', query: {to: to.fullPath}}
    }
})

// use the current title set in the index.html as the default
const DEFAULT_TITLE = document.title
router.afterEach(async (to) => {
    await nextTick()
    // set the title of the page using the route meta, if it's available
    let title = DEFAULT_TITLE
    if (!!to.meta.title) {
        title = `${DEFAULT_TITLE} - ${to.meta.title}`
    }
    document.title = title
})
