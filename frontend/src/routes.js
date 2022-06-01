import Home from './views/Home.vue'
import NotFound from './views/NotFound.vue'

/** @type {import('vue-router').RouterOptions['routes']} */
export const routes = [
  { path: '/', component: Home, name: 'home', meta: { title: 'Home' } },
  { path: '/:path(.*)', component: NotFound },
]
