<template>
  <div>
    <div class="text-4xl text-white font-bold pb-6">
      Institution - {{ institutionName }}
    </div>
  </div>
  <div class="flex flex-col lg:flex-row gap-8">
    <div class="w-full lg:w-3/5 border-2 bg-white p-3">
      <div class="flex flex-row gap-2 pb-2 border-b-2 border-black">
        <div class="text-black text-2xl">
          Review Policies
        </div>
        <div class="grow"></div>
        <!-- TODO: create button component -->
        <button class="bg-grey border py-1 pl-3 pr-1 hover:bg-grey-dark">
          Filter
          <VueFeather type="chevron-down" size="1.4rem" class="align-middle mx-1 -mt-1"/>
        </button>
      </div>
      <div class="flex flex-col gap-y-3 pt-2">
        <!-- TODO: create a list component? -->
        <div v-for="pack in policyPacks" class="flex flex-row items-center p-2 hover:bg-grey-light">
          <div>{{ pack.name }}</div>
          <div class="grow"></div>
          <button :class="packActionButtonClass[pack.status]" @click="packAction(pack)"
                  class="py-1 pl-4 pr-2">
            {{ packActionButtonTexts[pack.status] }}
            <VueFeather type="chevron-right" size="1.4rem" class="align-middle -mt-1"/>
          </button>
        </div>
      </div>
    </div>
    <div class="w-full lg:w-2/5 border-2 bg-white p-3">
      <div class="text-black text-2xl pb-2 border-b-2 border-black">
        Institutional Policies
      </div>
      <div class="pt-2 text-sm">
        Insert a list of institution policies...
      </div>
    </div>
  </div>
</template>

<script setup>
import {useAuth} from '@/store/auth'
import {PACK_STATUS, useStore} from '@/store/main'
import {storeToRefs} from 'pinia'
import {computed, onMounted} from 'vue'
import {useRouter} from 'vue-router'

const router = useRouter()
const {institution} = storeToRefs(useAuth())
const mainStore = useStore()
const {policyPacks} = storeToRefs(mainStore)
const {updatePolicyPacks} = mainStore

// TODO: make components out of the policy action buttons and then we don't need this?
const packActionButtonClass = {
  [PACK_STATUS.COMPLETE]: ['bg-status-approved', 'hover:bg-statusDark-approved'],
  [PACK_STATUS.INCOMPLETE]: ['bg-status-handled', 'hover:bg-statusDark-handled'],
  [PACK_STATUS.NOT_STARTED]: ['bg-status-new', 'hover:bg-statusDark-new'],
}
const packActionButtonTexts = {
  [PACK_STATUS.COMPLETE]: 'Edit',
  [PACK_STATUS.INCOMPLETE]: 'Continue',
  [PACK_STATUS.NOT_STARTED]: 'Start',
}

// use a computed guard for the institution name in case the institution hasn't been loaded yet
const institutionName = computed(() => !institution.value ? '' : institution.value.name)

onMounted(async () => {
  await updatePolicyPacks()
})

const packAction = (pack) => {
  router.push({name: 'pack', params: { id: pack.id}})
}

</script>
