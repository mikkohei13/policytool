import {defineStore} from 'pinia'
import {api} from '@/utils/api'
import {StorageSerializers, useLocalStorage} from '@vueuse/core'


export const useAuth = defineStore('auth', {
    state: () => ({
        user: null,
        institution: null,
        token: useLocalStorage('policy-tool-auth-token', null,
            {serializer: StorageSerializers.string}),
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
            await this.refreshDetails()
        },
        async logout() {
            if (!!this.token) {
                await api.post('/auth/logout/', {})
                api.unsetToken()
            }
            this.token = null
            await this.refreshDetails()
        },
        async refreshDetails() {
            if (!!this.token) {
                api.setToken(this.token)
                const whoami = await api.get('/api/whoami')
                this.user = whoami.user
                this.institution = whoami.institution || null
            } else {
                this.user = null
                this.institution = null
            }
        }
    }
})
