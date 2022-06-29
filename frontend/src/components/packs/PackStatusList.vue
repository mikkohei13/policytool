<template>
  <div v-if="showPicker" @click="showPicker = false"
       class="fixed inset-0 bg-grey-dark bg-opacity-50 overflow-y-auto h-full w-full">
    <div @click.stop=""
         class="absolute w-3/4 left-1/2 transform -translate-x-1/2 top-24 p-5 border shadow-lg rounded-md bg-white">
      <div class="pb-2 mb-2 border-b-2 text-xl">
        Select an option from the list below to start a response.
      </div>

      <PackItem v-for="pack in notStartedPacks" :pack="pack"></PackItem>
    </div>
  </div>

  <div class="border-2 bg-white p-3">
    <div class="flex flex-row gap-2 pb-3 border-b-2 border-black">
      <div class="text-black text-2xl">
        {{ title }}
      </div>
      <div class="grow"></div>
      <button class="bg-yellow rounded py-1 pr-3 pl-1 hover:bg-yellow-dark"
              @click="showPicker = true">
        <VueFeather type="plus" size="1.4rem" class="align-middle mx-1 -mt-1"/>
        Start new response
      </button>
    </div>

    <div class="p-2 pt-4 border-b border-grey-dark text-lg font-bold">
      Completed
    </div>
    <div class="flex flex-col gap-y-3 pt-2">
      <template v-if="completedPacks.length === 0">
        <div class="pl-2 text-grey-dark">Your complete responses will appear here</div>
      </template>
      <template v-else>
        <PackItem v-for="pack in completedPacks" :pack="pack"></PackItem>
      </template>
    </div>

    <div class="p-2 mt-6 border-b border-grey-dark text-lg font-bold">
      In Progress
    </div>
    <div class="flex flex-col gap-y-3 py-2">
      <template v-if="inProgressPacks.length === 0">
        <div class="pl-2 text-grey-dark">Your in progress responses will appear here</div>
      </template>
      <template v-else>
        <PackItem v-for="pack in inProgressPacks" :pack="pack"></PackItem>
      </template>
    </div>
  </div>

</template>

<script setup>
import PackItem from '@/components/packs/PackItem.vue'
import {computed, onMounted, ref} from 'vue'
import {calcPackStatus, PACK_STATUS} from '@/utils/utils'
import {api} from '@/utils/api'

const {type, title} = defineProps(['type', 'title'])
const packs = ref([])
const showPicker = ref(false)

const completedPacks = computed(() => {
  return packs.value.filter(pack => calcPackStatus(pack) === PACK_STATUS.COMPLETE)
})

const inProgressPacks = computed(() => {
  return packs.value.filter(pack => calcPackStatus(pack) === PACK_STATUS.INCOMPLETE)
})

const notStartedPacks = computed(() => {
  return packs.value.filter(pack => calcPackStatus(pack) === PACK_STATUS.NOT_STARTED)
})

const updatePolicyPacks = async () => {
  packs.value = await api.get(`/api/${type}/pack`)
}

onMounted(updatePolicyPacks)

</script>
