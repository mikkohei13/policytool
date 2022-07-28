<template>

  <div>
    <div class="text-4xl text-white font-bold pb-6">
      {{ service.name }} - {{ service.description }}
    </div>
  </div>

  <div class="border-2 bg-white p-6 w-full">
    <div class="flex flex-row items-baseline pb-1 border-b-2 border-yellow">
      <div class="text-3xl font-bold">Components</div>
      <div class="grow"></div>
      <a v-if="service.url" :href="service.url" target="_blank" class="underline text-lg pl-4">
        {{ service.url }}
        <VueFeather type="external-link" size="1rem"/>
      </a>
    </div>
    <div>
      <div v-for="component in service.components" class="py-2">
        <div class="text-lg">{{ component.name }}</div>
        <div class="prose max-w-none">{{ component.description }}</div>
      </div>
    </div>
  </div>

</template>

<script setup>
import {onMounted, ref} from 'vue'
import {api} from '@/utils/api'

const {id} = defineProps(['id'])
const service = ref({})

const getService = async () => {
  service.value = await api.get(`/api/dissco/service/${id}`)
}

onMounted(getService)

</script>
