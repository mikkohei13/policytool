import Home from '@/views/Home.vue'
import NotFound from '@/views/NotFound.vue'
import Login from '@/views/auth/Login.vue'
import Logout from '@/views/auth/Logout.vue'
import RequestAccount from '@/views/auth/RequestAccount.vue'
import ResetPassword from '@/views/auth/ResetPassword.vue'
import Policies from '@/views/Policies.vue'

/** @type {import('vue-router').RouterOptions['routes']} */
export const routes = [
  { path: '/', component: Home, name: 'home', meta: { title: 'Home' } },
  { path: '/dashboards', component: NotFound, name: 'dashboards', meta: { title: 'Dashboards' } },
  { path: '/policies', component: Policies, name: 'policies', meta: { title: 'Policies' } },
  { path: '/login', component: Login, name: 'login', meta: { title: 'Login' } },
  { path: '/logout', component: Logout, name: 'logout', meta: { title: 'Logout' } },
  { path: '/register', component: RequestAccount, name: 'requestAccount', meta: { title: 'Request Account' } },
  { path: '/reset', component: ResetPassword, name: 'resetPassword', meta: { title: 'Reset Password' } },
  { path: '/:path(.*)', component: NotFound, meta: {title: 'Page not found'} },
]
