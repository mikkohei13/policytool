<template>
  <div>
    <div class="text-4xl text-white font-bold pb-6">
      Institution - {{ institution?.name }}
    </div>
  </div>

  <div class="flex flex-col lg:flex-row gap-8">
    <div class="w-full">
      <PackStatusList type="policy" title="All Policy Responses"
                      :responderId="institution.id"></PackStatusList>
    </div>
  </div>
</template>

<script setup>
import PackStatusList from '@/components/packs/PackStatusList.vue'
import {storeToRefs} from 'pinia'
import {useAuth} from '@/store/auth'

const {institution} = storeToRefs(useAuth())
</script>
