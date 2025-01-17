import {defineStore} from 'pinia'
import {api} from '@/utils/api'
import {useLocalStorage} from '@vueuse/core'
import {DateTime} from 'luxon'

const DEFAULT_TOKEN = ''

export const useAuth = defineStore('auth', {
    state: () => ({
        token: useLocalStorage('token', DEFAULT_TOKEN),
        user: useLocalStorage('user', {}),
        institution: useLocalStorage('institution', null),
        lastCheck: useLocalStorage('lastCheck', null),
    }),
    getters: {
        loggedIn: (state) => !!state.token,
        notLoggedIn: (state) => !state.token,
    },
    actions: {
        async login(username, password) {
            console.log('Attempting login for:', username);
            // if there is a currently logged-in user, log them out first
            if (!!this.user) {
                await this.logout()
            }

            api.unsetToken()

            try {
                console.log('Making login request...');
                const data = await api.post('/auth/login/', {username, password})
                console.log('Login response:', data);
                this.token = data.key
                // must set the API token before getting the user data
                api.setToken(this.token)
                await this.refreshDetails()
                return true
            } catch (error) {
                console.error('Login error:', error);
                this.reset()
                return false
            }
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
