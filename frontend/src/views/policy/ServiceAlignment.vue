<template>

  <div>
    <div class="text-4xl text-white font-bold pb-6">
      Alignment: {{ service.name }} {{ "<->" }} {{ institution.name }}
    </div>
  </div>

  <div v-if="showStatus" @click="showStatus = false"
       class="fixed inset-0 bg-grey-dark bg-opacity-50 overflow-y-auto h-full w-full">
    <div @click.stop=""
         class="absolute w-3/4 left-1/2 transform -translate-x-1/2 top-24 p-5 border shadow-lg rounded-md bg-white">
      <div class="pb-2 mb-2 border-b-2 text-xl">
        {{ service.name }} alignment
      </div>

      <div class="flex flex-col gap-2">
        <div v-for="(policyAreaAlignments, policyAreaId) in alignments"
             class="border-b-2 border-grey">
          <div class="flex flex-row justify-between">
            <div class="font-bold text-2xl">{{ policyAreaAlignments[0].policy_name }}</div>
            <router-link
                :to="{name: 'pack', params: {id: policyAreaId, type: 'policy', responderId: institution.id}}"
                class="bg-yellow hover:bg-yellow-dark py-2 pl-4 pr-2 rounded">
              <span>Review</span>
              <VueFeather type="chevron-right" size="1.4rem" class="align-middle -mt-1"/>
            </router-link>
          </div>
          <div v-for="alignment in policyAreaAlignments"
               class="flex flex-row p-2 justify-between items-center hover:bg-grey-light">
            <div class="flex flex-col">
              <div>
                <span class="italic">"{{ alignment.status.policy_component_name }}"</span>
              </div>
              <div v-if="!alignment.status.passed" class="text-status-denied font-bold">
                Failed: {{ alignment.status.message }}
              </div>
              <div v-else class="text-status-approved font-bold">
                Passed
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <PackStatusList v-if="loaded" type="policy" :title="`${service.name} Policy Components`"
                  :responderId="institution.id" :filter="filterPacksToService">
    <div class="border-r-2 pr-2 cursor-pointer" @click="showStatus = true">
      <div class="text-lg rounded border-4 px-1"
           :class="`border-status-${status ? 'approved' : 'approved'}`">
        <span class="pr-2">Status:</span>
        <span class="font-bold">
          {{ status ? 'Aligned' : 'Aligned' }}
        </span>
      </div>
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
const alignments = ref({})
const status = ref(true)
const loaded = ref(false)
const showStatus = ref(false)

const filterPacksToService = (pack) => {
  return pack.id in alignments.value
}

const load = async () => {
  // get the service
  service.value = await api.get(`/api/dissco/service/${id}`)

  // get all the alignment data
  const alignmentsData = await api.get('/api/policy/alignment/')
  for (const alignment of alignmentsData) {
    if (alignment.service === Number(id)) {
      const policyAreaId = alignment.policy
      if (!(policyAreaId in alignments.value)) {
        alignments.value[policyAreaId] = []
      }
      alignments.value[policyAreaId].push(alignment)
      status.value &&= alignment.status.passed
    }
  }
  loaded.value = true
}

onMounted(load)

</script>
