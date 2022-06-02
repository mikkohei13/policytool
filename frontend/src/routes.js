import Home from './views/Home.vue'
import NotFound from './views/NotFound.vue'

/** @type {import('vue-router').RouterOptions['routes']} */
export const routes = [
  { path: '/', component: Home, name: 'home', meta: { title: 'Home' } },
  { path: '/dashboards', component: Home, name: 'dashboards', meta: { title: 'Dashboards' } },
  { path: '/policies', component: Home, name: 'policies', meta: { title: 'Policies' } },
  { path: '/institutions', component: Home, name: 'institutions', meta: { title: 'Institutions' } },
  { path: '/login', component: Home, name: 'login', meta: { title: 'login' } },
  { path: '/:path(.*)', component: NotFound },
]
