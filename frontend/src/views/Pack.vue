<template>
  <div class="w-full bg-white rounded p-4">
    <div class="flex flex-row border-b-2 border-b-yellow">
      <div class="p-4 text-2xl">
        {{ pack.name }}
      </div>
      <div class="grow"></div>
      <div class="flex flex-row gap-2 h-10">
        <div class="self-center pr-2 border-r-2">
          {{ groupIndex + 1 }} / {{ questionGroups.length }}
        </div>
        <div class="h-10 w-10">
          <button class="bg-grey p-1 w-full h-full rounded hover:bg-grey-dark" v-if="showPrevious">
            <VueFeather type="chevron-left" size="2rem"
                        @click="groupIndex--" class="cursor-pointer"/>
          </button>
        </div>
        <div class="h-10 w-10">
          <button class="bg-grey p-1 w-full h-full rounded hover:bg-grey-dark p-1 h-10 w-10"
                  v-if="showNext">
            <VueFeather type="chevron-right" size="2rem" class="cursor-pointer"
                        @click="groupIndex++"/>
          </button>
        </div>
        <button class="bg-yellow rounded hover:bg-yellow-dark p-1 h-10 w-10" @click="saveAnswers">
          <VueFeather type="save" size="2rem" class="cursor-pointer"/>
        </button>
        <router-link class="bg-yellow rounded hover:bg-yellow-dark p-1 h-10 w-10" :to="{name: type}">
          <VueFeather type="home" size="2rem" class="cursor-pointer"/>
        </router-link>
      </div>
    </div>

    <div class="px-12">
      <div class="grow justify-self-start">
        <div v-for="(question, index) in questionGroups[groupIndex]">
          <div class="p-4">
            <div class="text-xl pb-2 font-bold" v-if="index === 0">
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
import String from '@/components/packs/questions/String.vue'
import Text from '@/components/packs/questions/Text.vue'
import Number from '@/components/packs/questions/Number.vue'
import OptionSingle from '@/components/packs/questions/OptionSingle.vue'
import OptionMultiple from '@/components/packs/questions/OptionMultiple.vue'
import Maturity from '@/components/packs/questions/Maturity.vue'
import {computed, onMounted, ref} from 'vue'
import {api} from '@/utils/api'
import {notify} from '@kyvg/vue3-notification'

const types = {
  'bool': Bool,
  'string': String,
  'text': Text,
  'number': Number,
  'option': OptionSingle,
  'options': OptionMultiple,
  'maturity': Maturity,
}

const {id, type} = defineProps(['id', 'type'])
const pack = ref({})
const updatedQuestionIds = new Set()
const questionGroups = ref([])
const groupIndex = ref(0)

const showPrevious = computed(() => groupIndex.value !== 0)
const showNext = computed(() => {
  if (!questionGroups.value) {
    return false
  } else {
    return groupIndex.value < questionGroups.value.length - 1
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
  notify({
    title: 'Success',
    text: 'Answers saved',
    type: 'success'
  });
}

const updatePack = async () => {
  pack.value = await api.get(`/api/${type}/pack/${id}`)

  // group the questions by order value in an array
  questionGroups.value = []
  let order = 0
  let group = []
  for (const question of pack.value.questions) {
    if (question.order === order) {
      group.push(question)
    } else {
      order = question.order
      if (group.length) {
        questionGroups.value.push(group)
      }
      group = [question]
    }
  }
  if (group.length) {
    questionGroups.value.push(group)
  }
}

onMounted(async () => {
  await updatePack()

  const index = pack.value.questions.findIndex((question) => !question.answer)
  groupIndex.value = Math.max(index, 0)
})

const updateAnswer = (questionId, value, comment) => {
  getQuestion(questionId).answer = {value, comment}
  updatedQuestionIds.add(questionId)
}

</script>
