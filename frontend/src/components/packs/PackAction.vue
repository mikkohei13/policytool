<template>
  <router-link :to="{name: 'pack', params: {id: pack.id, type: pack.type}}"
               :class="statusOption.class" class="py-1 pl-4 pr-2 rounded">
    {{ statusOption.text }}
    <VueFeather type="chevron-right" size="1.4rem" class="align-middle -mt-1"/>
  </router-link>
</template>

<script setup>
import {computed} from 'vue'
import {calcPackStatus, PACK_STATUS} from '@/utils/utils'

const options = {
  [PACK_STATUS.NOT_STARTED]: {
    'class': ['bg-yellow', 'hover:bg-yellow-dark'],
    'text': 'Start'
  },
  [PACK_STATUS.INCOMPLETE]: {
    'class': ['bg-blue', 'hover:bg-blue-dark'],
    'text': 'Continue'
  },
  [PACK_STATUS.COMPLETE]: {
    'class': ['bg-grey', 'hover:bg-grey-dark'],
    'text': 'Edit'
  }
}

const {pack} = defineProps(['pack'])
const statusOption = computed(() => options[calcPackStatus(pack)])

</script>
