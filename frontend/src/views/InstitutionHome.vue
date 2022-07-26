<template>
  <div>
    <div class="text-4xl text-white font-bold pb-6">
      Institution - {{ institution?.name }}
    </div>
  </div>

  <div class="flex flex-col lg:flex-row gap-8">
    <div class="w-full lg:w-3/5">
      <PackStatusList type="policy" title="Review Policy Alignment Responses"></PackStatusList>
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
import PackStatusList from '@/components/packs/PackStatusList.vue'
import {useAuth} from '@/store/auth'
import {storeToRefs} from 'pinia'
import {onMounted, ref} from 'vue'
import {api} from '@/utils/api'

const {institution} = storeToRefs(useAuth())

const policies = ref([])

const updatePolicies = async () => {
  policies.value = await api.get(`/api/policy/${institution.value.id}/pack`)
}

onMounted(updatePolicies)

</script>
