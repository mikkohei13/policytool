import {defineStore} from 'pinia'
import {api} from '@/utils/api'


export const useStore = defineStore('main', {
    state: () => ({
        policyPacks: []
    }),
    getters: {},
    actions: {
        async updatePolicyPacks() {
            const response = await api.get('/api/policy/pack')
            this.policyPacks = response.data
        }
    }
})
