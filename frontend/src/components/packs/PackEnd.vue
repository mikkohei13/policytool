<template>
  <div class="pt-4">
    <p class="font-bold">Your responses have all been saved.</p>

    <template v-if="!isFinished">
      <p>
        If you are happy you have answered as many questions as you can, you can mark this set of
        questions as complete below.
      </p>
      <p>Don't forget, you can always come back and update them later!</p>
      <button v-if="!isFinished"
              class="mt-10 p-2 w-full flex flex-row justify-center items-center rounded bg-yellow hover:bg-yellow-dark"
              @click="setFinished(true)">
        <span class="text-lg pr-2">Finish and return home</span>
        <VueFeather type="check-square" size="2rem" class="cursor-pointer"/>
      </button>
    </template>

    <template v-else>
      <p>
        This set of questions has been marked as complete.
        If you want to change this, click the button below.
        Only do this if you would like to specifically assert that this assessment is incomplete.
      </p>
      <p>
        Answers can be modified on a finished set of questions and therefore you do not need to
        change this status to edit answers after marking a set of questions as finished.
      </p>
      <button
          class="mt-6 p-2 pl-4 w-full flex flex-row justify-center items-center rounded bg-grey hover:bg-grey-dark"
          @click="setFinished(false)">
        <span class="text-lg pr-2">Mark as incomplete</span>
        <VueFeather type="x-square" size="2rem" class="cursor-pointer"/>
      </button>
    </template>
  </div>
</template>

<script setup>

import {api} from '@/utils/api'
import {ref} from "vue";
import {useRouter} from 'vue-router'

const {pack} = defineProps(['pack'])
const router = useRouter()
const isFinished = ref(!!pack.finished_at)

const finishURL = `/api/${pack.type}/${pack.responder_id}/pack/${pack.id}/finish`

const setFinished = async (finished) => {
  await api.put(finishURL, {finished: finished})
  isFinished.value = finished
  if (finished) {
    await router.push({name: pack.type})
  }
}

</script>
