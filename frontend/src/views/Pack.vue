<template>
  <div class="w-full bg-white rounded p-4">
    <div class="flex flex-row border-b-2 border-b-yellow">
      <div class="p-4 text-2xl">
        {{ pack.name }}
      </div>
      <div class="grow"></div>
      <div class="flex flex-row gap-2">
        <div class="h-10 w-10">
          <button class="bg-grey p-1 w-full h-full rounded hover:bg-grey-dark" v-if="showPrevious">
            <VueFeather type="chevron-left" size="2rem"
                        @click="currentIndex--" class="cursor-pointer"/>
          </button>
        </div>
        <div class="h-10 w-10">
          <button class="bg-grey p-1 w-full h-full rounded hover:bg-grey-dark p-1 h-10 w-10" v-if="showNext">
            <VueFeather type="chevron-right" size="2rem" class="cursor-pointer"
                        @click="currentIndex++"/>
          </button>
        </div>
        <button class="bg-yellow rounded hover:bg-yellow-dark p-1 h-10 w-10" @click="saveAnswers">
          <VueFeather type="save" size="2rem" class="cursor-pointer"/>
        </button>
      </div>
    </div>

    <div class="px-12">
      <div class="grow justify-self-start">
        <div v-for="(question, index) in pack.questions">
          <div v-if="index === currentIndex" class="p-4">
            <div class="text-xl pb-2 font-bold">
              {{ question.text }}
            </div>
            <div class="pb-6">
              {{ question.hint }}
            </div>
            <component :is="types[question.type]" :question="question"
                       @update-answer="updateAnswer">
            </component>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Bool from '@/components/packs/questions/Bool.vue'
import {computed, onMounted, ref} from 'vue'
import {api} from '@/utils/api'

const types = {
  'bool': Bool,
  'string': Bool,
  'text': Bool,
  'number': Bool,
  'option': Bool,
  'options': Bool,
}

const {id, type} = defineProps(['id', 'type'])
const pack = ref({})
const updatedQuestionIds = new Set()
// TODO: start at first incomplete answer
let currentIndex = ref(0)

const showPrevious = computed(() => currentIndex.value !== 0)
const showNext = computed(() => {
  if (!pack.value.questions) {
    return false
  } else {
    return currentIndex.value < pack.value.questions.length - 1
  }
})

const getQuestion = (questionId) => {
  return pack.value.questions.find((question) => question.id === questionId)
}


const saveAnswers = async () => {
  for (const questionId of updatedQuestionIds) {
    await api.post(`/api/${type}/pack/answer/${questionId}`, getQuestion(questionId).answer)
  }
  updatedQuestionIds.clear()
}

const updatePack = async () => {
  pack.value = await api.get(`/api/${type}/pack/${id}`)
}

onMounted(async () => {
  await updatePack()
  const index = pack.value.questions.findIndex((question) => !question.answer)
  currentIndex.value = Math.max(index, 0)
})

const updateAnswer = (questionId, value, comment) => {
  getQuestion(questionId).answer = {value, comment}
  updatedQuestionIds.add(questionId)
}

</script>
