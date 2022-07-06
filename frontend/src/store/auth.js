import {defineStore} from 'pinia'
import {api} from '@/utils/api'
import {useLocalStorage} from '@vueuse/core'
import {DateTime} from 'luxon'

const DEFAULT_TOKEN = ''

export const useAuth = defineStore('auth', {
    state: () => ({
        user: null,
        institution: null,
        token: useLocalStorage('policy-tool-auth-token', DEFAULT_TOKEN),
        nextCheck: null
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

            api.unsetToken()

            try {
                const data = await api.post('/auth/login/', {username, password})
                this.token = data.key
                // must set the API token before getting the user data
                api.setToken(this.token)
                await this.refreshDetails()
            } catch (error) {
                // TODO: show an error?
                this.reset()
            }
            return !!this.token
        },
        async logout() {
            if (!!this.token) {
                try {
                    await api.post('/auth/logout/', {})
                } catch (error) {
                    console.log('Failed to logout, ignoring')
                }
            }
            this.reset()
        },
        /**
         * Resets the auth state back to logged out defaults.
         */
        reset() {
            this.token = DEFAULT_TOKEN
            this.user = null
            this.institution = null
            api.unsetToken()
        },
        async refreshDetails() {
            if (!!this.token) {
                api.setToken(this.token)
                try {
                    const whoami = await api.get('/api/whoami')
                    this.user = whoami.user
                    this.institution = whoami.institution || null
                } catch (error) {
                    // good chance this means the token is wrong, log them out so that they have to
                    // get a new one
                    this.reset()
                }
            } else {
                this.reset()
            }
        },
        /**
         * Checks if there is a logged in user or not and returns a boolean to indicate as such.
         * This action can be called repeatedly and will only check every hour.
         *
         * @returns {Promise<Boolean>}
         */
        async check() {
            if (!!this.token && (this.nextCheck === null || this.nextCheck < DateTime.now())) {
                await this.refreshDetails()
                this.nextCheck = DateTime.now().plus({hours: 1})
            }
            return this.loggedIn
        }
    }
})
