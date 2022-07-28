<template>

  <div>
    <div class="text-4xl text-white font-bold pb-6">
      Alignment: {{ service.name }} {{ "<->" }} {{ institution.name }}
    </div>
  </div>

  <PackStatusList v-if="loaded" type="policy" :title="`${service.name} Policy Components`"
                  :responderId="institution.id" :filter="filterPacksToService">
    <div class="flex flex-row items-center border-r-2 pr-2 cursor-pointer">
      <div class="pr-2 text-lg">Alignment status:</div>
      <div class="rounded h-6 w-6" :class="`bg-status-${status ? 'approved' : 'denied'}`"/>
    </div>
  </PackStatusList>

</template>

<script setup>
import {defineProps, onMounted, ref} from 'vue'
import {useAuth} from '@/store/auth'
import {storeToRefs} from 'pinia'
import {api} from '@/utils/api'
import PackStatusList from '@/components/packs/PackStatusList.vue'

const {id} = defineProps(['id'])
const {institution} = storeToRefs(useAuth())

const service = ref({})
const policyAreaIds = ref(new Set())
const alignments = ref([])
const status = ref(false)
const loaded = ref(false)

const filterPacksToService = (pack) => {
  return policyAreaIds.value.has(pack.id)
}

const load = async () => {
  // get the service
  service.value = await api.get(`/api/dissco/service/${id}`)

  // get all the alignment data
  alignments.value = await api.get('/api/policy/alignment/')
  for (const alignment of alignments.value) {
    if (alignment.service === Number(id)) {
      policyAreaIds.value.add(alignment.policy)
      status.value &&= alignment.status.passed
    }
  }
  loaded.value = true
}

onMounted(load)

</script>
