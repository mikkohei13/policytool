<template>
  <div class="flex flex-row gap-3 items-center p-2 hover:bg-grey-light">
    <div>
      <span>{{ pack.name }} - </span>
      <span class="italic">{{ pack.size }} questions</span>
    </div>
    <div class="grow"></div>
    <button v-if="status !== PACK_STATUS.NOT_STARTED" @click="reset"
            class="bg-status-denied hover:bg-statusDark-denied py-1 pl-4 pr-3 rounded">
      <span class="pr-2">Reset</span>
      <VueFeather type="delete" size="1.4rem" class="align-middle -mt-1"/>
    </button>
    <router-link
        :to="{name: 'pack', params: {id: pack.id, type: pack.type, responderId: pack.responder_id}}"
        :class="statusOption.class" class="py-1 pl-4 pr-2 rounded">
      {{ statusOption.text }}
      <VueFeather type="chevron-right" size="1.4rem" class="align-middle -mt-1"/>
    </router-link>
  </div>
</template>

<script setup>
import {computed} from 'vue'
import {calcPackStatus, PACK_STATUS} from '@/utils/utils'
import {api} from '@/utils/api'
import {notify} from "@kyvg/vue3-notification";

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
    'class': ['bg-status-approved', 'hover:bg-statusDark-approved'],
    'text': 'Edit'
  }
}

const {pack} = defineProps(['pack'])
const emit = defineEmits(['refresh'])

const status = calcPackStatus(pack)
const statusOption = computed(() => options[status])

const reset = async () => {
  if (!confirm('Are you sure you want to reset all the answers in this component?')) {
    return
  }

  let notification = {
    type: 'success',
    duration: 5000
  }
  try {
    await api.delete(`/api/${pack.type}/${pack.responder_id}/pack/${pack.id}`)
    notification.title = 'Answers reset'
    emit('refresh')
  } catch (e) {
    notification.title = 'An error occurred while resetting answers'
    notification.type = 'error'
  }
  notify(notification)
}

</script>
