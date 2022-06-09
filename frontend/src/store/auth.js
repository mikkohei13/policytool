import {defineStore} from 'pinia'
import {api} from '@/utils/api'


export const useAuth = defineStore('auth', {
    state: () => ({
        user: null,
        token: null
    }),
    getters: {},
    actions: {
        async login(username, password) {
            // if there is a currently logged-in user, log them out first
            if (!!this.user) {
                await this.logout()
            }

            const data = await api.post('/auth/login/', {username, password})
            this.token = data.key
            // must set the API token before getting the user data
            api.setToken(this.token)
            this.user = await api.get('/api/user')
        },
        async logout() {
            if (!!this.token) {
                await api.post('/auth/logout/', {})
                api.unsetToken()
            }
            this.token = null
            this.user = null
        }
    }
})
