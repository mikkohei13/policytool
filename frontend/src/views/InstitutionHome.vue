<template>
  <div>
    <div class="text-4xl text-white font-bold pb-6">
      Institution - {{ institutionName }}
    </div>
  </div>
  <div class="flex flex-col md:flex-row gap-8">
    <div class="w-3/5 border-2 bg-white p-3">
      <div class="flex flex-row gap-2 pb-2 border-b-2 border-grey-darker">
        <div class="text-black text-2xl">
          Review Policies
        </div>
        <div class="grow"></div>
        <!-- TODO: create button component -->
        <button class="bg-yellow border py-1 pr-3">
          <VueFeather type="plus" size="1.4rem" class="align-middle mx-1 -mt-1"/>
          Start new
        </button>
        <button class="bg-grey border py-1 pr-3">
          <VueFeather type="chevron-down" size="1.4rem" class="align-middle mx-1 -mt-1"/>
          Filter
        </button>
      </div>
      <div>

      </div>
    </div>
    <div class="w-2/5 text-blue">
    </div>
  </div>
</template>

<script setup>
import {useAuth} from '@/store/auth'
import {useStore} from '@/store/main'
import {storeToRefs} from 'pinia'
import {computed, onMounted} from "vue";

const {institution} = storeToRefs(useAuth())
const mainStore = useStore()
const {policyPacks} = storeToRefs(mainStore)
const {updatePolicyPacks} = mainStore

// use a computed guard for the institution name in case the institution hasn't been loaded yet
const institutionName = computed(() => !institution.value ? '' : institution.value.name)

onMounted(async () => {
  await updatePolicyPacks()
})

</script>
