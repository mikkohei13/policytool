<template>
  <div>
    <div class="text-4xl text-white font-bold pb-6">
      Institution - {{ institution?.name }}
    </div>
  </div>

  <PackStatusList type="policy" title="Review Policy Alignment Responses"
                  :responderId="institution.id"></PackStatusList>
</template>

<script setup>
import PackStatusList from '@/components/packs/PackStatusList.vue'
import {useAuth} from '@/store/auth'
import {storeToRefs} from 'pinia'

const {institution} = storeToRefs(useAuth())
</script>
