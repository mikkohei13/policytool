<template>
  <div>
    <div class="text-4xl text-white font-bold">Institution - {{ institutionName }}</div>
  </div>
</template>

<script setup>
import {useAuth} from '@/store/auth'
import {storeToRefs} from 'pinia'
import {computed} from "vue";

const {institution} = storeToRefs(useAuth())

// use a computed guard for the institution name in case the institution hasn't been loaded yet
const institutionName = computed(() => !institution.value ? '' : institution.value.name)

</script>
