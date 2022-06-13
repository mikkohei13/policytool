<template>
  <div>
    <div class="text-4xl text-white font-bold pb-6">
      Institution - {{ institutionName }}
    </div>
  </div>
  <div class="flex flex-col md:flex-row gap-8">
    <div class="w-3/5 border-2 bg-white p-3">
      <div class="flex flex-row pb-2 border-b-2">
        <div class="text-black text-2xl">
          Review Policies
        </div>
        <div class="grow"></div>
        <button class="bg-yellow border py-1 px-3">
          Filter
          <VueFeather type="chevron-down" size="1.4rem" class="align-middle" />
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
