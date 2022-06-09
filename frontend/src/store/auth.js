import {defineStore} from 'pinia'
import {api} from '@/utils/api'


export const useAuth = defineStore('auth', {
    state: () => ({
        user: null,
        token: null,
    }),
    getters: {
        /**
         * Getter that tells you if there is a logged-in user or not.
         *
         * @param state the state
         * @returns {boolean}
         */
        loggedIn: (state) => !!state.user,
        /**
         * The inverse of loggedIn. This is provided for convenience because if loggedIn is used as
         * a ref it can't be inverted directly with a "!" and maintain reactivity.
         *
         * @param state
         * @returns {boolean}
         */
        notLoggedIn: (state) => !state.user,
    },
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
