import Home from './views/Home.vue'
import NotFound from './views/NotFound.vue'

/** @type {import('vue-router').RouterOptions['routes']} */
export const routes = [
  { path: '/', component: Home, name: 'home', meta: { title: 'Home' } },
  { path: '/dashboards', component: NotFound, name: 'dashboards', meta: { title: 'Dashboards' } },
  { path: '/policies', component: NotFound, name: 'policies', meta: { title: 'Policies' } },
  { path: '/institutions', component: NotFound, name: 'institutions', meta: { title: 'Institutions' } },
  { path: '/login', component: NotFound, name: 'login', meta: { title: 'login' } },
  { path: '/:path(.*)', component: NotFound },
]
