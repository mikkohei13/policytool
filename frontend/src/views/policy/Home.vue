<template>
  <div>
    <div class="text-4xl text-white font-bold pb-6">
      Institution - {{ institution?.name }}
    </div>
  </div>

  <div class="flex flex-col gap-10">
    <div>
      <router-link :to="{name: 'policy_assessments'}"
                   class="bg-yellow p-3 rounded hover:bg-yellow-dark">
        View your institution's self-assessments
      </router-link>
    </div>

    <div>
      <router-link :to="{name: 'policy_policies'}"
                   class="bg-yellow p-3 rounded hover:bg-yellow-dark">
        View your institution's policies
      </router-link>
    </div>
  </div>
</template>

<script setup>
import {useAuth} from '@/store/auth'
import {storeToRefs} from 'pinia'

const {institution} = storeToRefs(useAuth())
</script>
