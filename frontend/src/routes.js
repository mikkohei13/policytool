import Home from '@/views/Home.vue'
import InstitutionHome from '@/views/policy/Home.vue'
import NotFound from '@/views/NotFound.vue'
import Login from '@/views/auth/Login.vue'
import Logout from '@/views/auth/Logout.vue'
import Pack from '@/views/Pack.vue'
import MaturityHome from '@/views/maturity/Home.vue'
import ResponderHome from '@/views/maturity/ResponderHome.vue'
import CreateTeam from '@/views/maturity/CreateTeam.vue'
import CreatePolicyDoc from '@/views/policy/CreatePolicyDoc.vue'
import PolicyDocs from '@/views/policy/PolicyDocs.vue'
import ServiceAlignment from '@/views/policy/ServiceAlignment.vue'
import ServiceHome from '@/views/policy/ServiceHome.vue'
import AllPolicies from '@/views/policy/AllPolicies.vue'

/** @type {import('vue-router').RouterOptions['routes']} */
export const routes = [
    {path: '/', component: Home, name: 'home', meta: {title: 'Home'}},
    {
        path: '/policy',
        component: InstitutionHome,
        name: 'policy',
        meta: {title: 'Policy', auth: true}
    },
    {
        path: '/policy/docs',
        component: PolicyDocs,
        name: 'policy_docs',
        meta: {title: 'Policies', auth: true}
    },
    {
        path: '/policy/create',
        component: CreatePolicyDoc,
        name: 'policy_doc_create',
        meta: {title: 'Add Policy Document', auth: true}
    },
    {
        path: '/policy/all',
        component: AllPolicies,
        name: 'policy_all',
        meta: {title: 'All Policies', auth: true}
    },
    {
        path: '/policy/service/:id',
        component: ServiceHome,
        name: 'policy_service_home',
        meta: {title: 'DiSSCo Service', auth: true},
        props: true
    },
    {
        path: '/policy/service/:id/alignment',
        component: ServiceAlignment,
        name: 'policy_service_alignment',
        meta: {title: 'DiSSCo Service policy alignment', auth: true},
        props: true
    },
    {
        path: '/maturity',
        component: MaturityHome,
        name: 'maturity',
        meta: {title: 'Maturity Home', auth: true}
    },
    {
        path: '/maturity/:id',
        component: ResponderHome,
        name: 'maturity_responder_home',
        meta: {title: 'Maturity Home', auth: true},
        props: true
    },
    {
        path: '/maturity/create',
        component: CreateTeam,
        name: 'maturity_create_team',
        meta: {title: 'Create new maturity assessment team', auth: true}
    },
    {
        path: '/pack/:responderId/:type/:id',
        component: Pack,
        name: 'pack',
        meta: {title: 'Question Pack', auth: true},
        props: true
    },
    {path: '/login', component: Login, name: 'login', meta: {title: 'Login'}},
    {path: '/logout', component: Logout, name: 'logout', meta: {title: 'Logout'}},
    {path: '/', component: NotFound, name: 'not_found', meta: {title: 'Page not found'}},
]
