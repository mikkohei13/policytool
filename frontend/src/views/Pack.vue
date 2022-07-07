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
          <button class="bg-grey p-1 w-full h-full rounded hover:bg-grey-dark" v-if="showPrevious"
                  @click="move(-1)">
            <VueFeather type="chevron-left" size="2rem" class="cursor-pointer"/>
          </button>
        </div>
        <div class="h-10 w-10">
          <button class="bg-grey p-1 w-full h-full rounded hover:bg-grey-dark p-1 h-10 w-10"
                  v-if="showNext" @click="move(1)">
            <VueFeather type="chevron-right" size="2rem" class="cursor-pointer"/>
          </button>
        </div>
        <div class="h-10 w-10">
          <button class="bg-yellow rounded hover:bg-yellow-dark p-1 h-10 w-10"
                  @click="leave">
            <VueFeather type="home" size="2rem" class="cursor-pointer"/>
          </button>
        </div>
      </div>
    </div>

    <div class="px-12">
      <div class="grow justify-self-start">
        <div v-for="(question, index) in questionGroups[groupIndex]" :key="question.id">
          <div class="p-4">
            <div class="text-xl pb-2 font-bold" v-if="index === 0">
              {{ groupIndex + 1 }}. {{ question.text }}
            </div>
            <div class="pb-6">
              <Markdown :markdown="question.hint"></Markdown>
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
import Markdown from '@/components/Markdown.vue'
import {computed, onMounted, ref} from 'vue'
import {api} from '@/utils/api'
import {notify} from '@kyvg/vue3-notification'
import {clamp} from '@/utils/utils'
import {useRouter} from 'vue-router'

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
const router = useRouter()
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

const move = async (distance) => {
  groupIndex.value = clamp(groupIndex.value + distance, 0, questionGroups.value.length - 1)
  await saveAnswers()
}

const leave = async () => {
  await saveAnswers()
  await router.push({name: type})
}

const saveAnswers = async () => {
  if (updatedQuestionIds.size) {
    for (const questionId of updatedQuestionIds) {
      await api.post(`/api/${type}/pack/${id}/${questionId}/`, getQuestion(questionId).answer)
    }
    updatedQuestionIds.clear()
    notify({
      title: 'Success',
      text: 'Answers saved',
      type: 'success',
      duration: 5000
    })
  }
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

  const index = questionGroups.value.findIndex(
      (questions) => questions.some(question => !question.answer)
  )
  groupIndex.value = Math.max(index, 0)
})

const updateAnswer = (questionId, value, comment) => {
  getQuestion(questionId).answer = {value, comment}
  updatedQuestionIds.add(questionId)
}

</script>
