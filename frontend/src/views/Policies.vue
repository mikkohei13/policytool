<template>
  <div v-for="institution in store.institutions" class="bg-white">
    {{ institution.name }}
  </div>
</template>

<script setup>
import {onMounted} from 'vue'
import {useStore} from '@/store/main'

const store = useStore()

onMounted(async () => {
  console.log('Updated institutional list')
  await store.update()
})

</script>
