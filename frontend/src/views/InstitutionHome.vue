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
          Review Policy Alignment Responses
        </div>
        <div class="grow"></div>
        <!-- TODO: create button component -->
        <button class="bg-grey border rounded py-1 pl-3 pr-1 hover:bg-grey-dark">
          Filter
          <VueFeather type="chevron-down" size="1.4rem" class="align-middle mx-1 -mt-1"/>
        </button>
      </div>
      <div class="flex flex-col gap-y-3 pt-2">
        <div v-for="pack in packs" class="flex flex-row items-center p-2 hover:bg-grey-light">
          <div>
            <span>{{ pack.name }} - </span>
            <span class="italic">{{ pack.size }} questions</span>
          </div>
          <div class="grow"></div>
          <PackAction :pack="pack"></PackAction>
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
import PackAction from '@/components/packs/PackAction.vue'
import {useAuth} from '@/store/auth'
import {computed, onMounted, ref} from 'vue'
import {storeToRefs} from 'pinia'
import {api} from '@/utils/api'

const {institution} = storeToRefs(useAuth())

const packs = ref([])

// use a computed guard for the institution name in case the institution hasn't been loaded yet
const institutionName = computed(() => !institution.value ? '' : institution.value.name)


const updatePolicyPacks = async () => {
  packs.value = await api.get('/api/policy/pack')
}

onMounted(updatePolicyPacks)

</script>
