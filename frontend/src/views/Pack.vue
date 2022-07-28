<template>
  <div v-if="Object.keys(pack).length > 0" class="w-full bg-white rounded p-4">
    <div class="flex flex-row border-b-2 border-b-yellow">
      <div class="p-2 pl-4 text-2xl">
        <span v-if="state === states.start">Introduction</span>
        <span v-else-if="state === states.end">Finish</span>
        <span v-else>{{ pack.name }}</span>
      </div>
      <div class="grow"></div>
      <div class="flex flex-row gap-2 h-10">
        <div class="self-center pr-2 border-r-2">
          <span v-if="state === states.questions">
            {{ groupIndex + 1 }} / {{ questionGroups.length }}
          </span>
        </div>
        <div class="h-10 w-10">
          <button class="bg-grey p-1 w-full h-full rounded hover:bg-grey-dark"
                  v-if="state !== states.start" @click="move(-1)">
            <VueFeather type="chevron-left" size="2rem" class="cursor-pointer"/>
          </button>
        </div>
        <div class="h-10 w-10">
          <button class="bg-grey p-1 w-full h-full rounded hover:bg-grey-dark p-1 h-10 w-10"
                  v-if="state !== states.end" @click="move(1)">
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
        <div v-if="state === states.start">
          <PolicyPackStart v-if="pack.type === 'policy'" :pack="pack"/>
          <MaturityPackStart v-if="pack.type === 'maturity'" :pack="pack"/>

          <button
              class="mt-6 p-2 pl-4 w-full flex flex-row justify-center items-center rounded bg-yellow hover:bg-yellow-dark"
              @click="move(1)">
            <span class="text-lg">Click here to begin</span>
            <VueFeather type="chevron-right" size="2rem" class="cursor-pointer"/>
          </button>
        </div>

        <PackEnd v-else-if="state === states.end" :pack="pack"/>

        <template v-else>
          <div v-for="(question, index) in questionGroups[groupIndex]" :key="question.id">
            <div class="p-4">
              <div class="text-xl pb-2 font-bold" v-if="index === 0">
                {{ groupIndex + 1 }}. {{ question.text }}
              </div>
              <div class="pb-6">
                <Markdown :markdown="question.hint"></Markdown>
              </div>
              <component :is="types[question.type]" :question="question"
                         :allowComment="commentable()"
                         @update-answer="updateAnswer">
              </component>
            </div>
          </div>
        </template>
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
import PolicyPackStart from '@/components/packs/PolicyPackStart.vue'
import MaturityPackStart from '@/components/packs/MaturityPackStart.vue'
import PackEnd from '@/components/packs/PackEnd.vue'
import {onMounted, ref} from 'vue'
import {api} from '@/utils/api'
import {notify} from '@kyvg/vue3-notification'
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
const states = {
  'start': 'start',
  'end': 'end',
  'questions': 'questions',
}

const {id, type, responderId} = defineProps(['id', 'type', 'responderId'])
const router = useRouter()
const pack = ref({})
const updatedQuestionIds = new Set()
const questionGroups = ref([])
const groupIndex = ref(0)
const state = ref(states.start)

const getQuestion = (questionId) => {
  return pack.value.questions.find((question) => question.id === questionId)
}

// policy packs can't be commented on
// TODO: make this part of the API pack response? Like add an options/settings section or something?
const commentable = () => type !== 'policy'

const move = async (distance) => {
  if (state.value === states.start || state.value === states.end) {
    state.value = states.questions
  } else {
    const target = groupIndex.value + distance
    if (target < 0) {
      state.value = states.start
    } else if (target > questionGroups.value.length - 1) {
      state.value = states.end
    } else {
      groupIndex.value = target
    }
  }
  await saveAnswers()
}

const leave = async () => {
  await saveAnswers()
  // TODO: once we create an policy landing page similar to the maturity one this logic can go
  if (type === 'maturity') {
    await router.push({name: 'maturity_responder_home', params: {id: responderId}})
  } else {
    await router.push({name: 'policy_assessments'})
  }
}

const saveAnswers = async () => {
  if (updatedQuestionIds.size) {
    for (const questionId of updatedQuestionIds) {
      await api.post(`/api/${type}/${responderId}/pack/${id}/${questionId}/`,
          getQuestion(questionId).answer)
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
  try {
    pack.value = await api.get(`/api/${type}/${responderId}/pack/${id}`)
  } catch (e) {
    switch (e.response.status) {
      case 404:
        await router.push({name: 'not_found', params: {path: router.currentRoute.value.fullPath}})
        return
      case 403:
        await router.push({name: 'login'})
        return
    }
  }

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
  state.value = groupIndex.value === 0 ? states.start : states.questions
})

const updateAnswer = (questionId, value, comment) => {
  getQuestion(questionId).answer = {value, comment}
  updatedQuestionIds.add(questionId)
}

</script>
