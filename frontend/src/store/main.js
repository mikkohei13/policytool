import {defineStore} from 'pinia'
import {api} from '@/utils/api'

export const PACK_STATUS = {
    COMPLETE: 'complete',
    INCOMPLETE: 'incomplete',
    NOT_STARTED: 'not_started',
}

const IN_PROGRESS = [PACK_STATUS.COMPLETE, PACK_STATUS.INCOMPLETE]

export const useStore = defineStore('main', {
    state: () => ({
        policyPacks: []
    }),
    getters: {
        inProgressPolicyPacks: (state) => {
            return state.policyPacks.filter((pack) => IN_PROGRESS.includes(pack.status))
        },
        getPack: (state) => {
            return (id) => state.policyPacks.find((pack) => pack.id === Number(id))
        }
    },
    actions: {
        async updatePolicyPacks() {
            this.policyPacks = await api.get('/api/policy/pack')
        },
    }
})
