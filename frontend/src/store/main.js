import {defineStore} from 'pinia'
import {api} from '@/utils/api'


export const useStore = defineStore('main', {
    state: () => ({
        policyPacks: []
    }),
    getters: {},
    actions: {
        async updatePolicyPacks() {
            this.policyPacks = await api.get('/api/policy/pack')
        },
    }
})
