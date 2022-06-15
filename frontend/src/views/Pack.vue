<template>
  <div class="w-full bg-white rounded p-4">
    <div class="flex flex-row border-b-2 border-b-yellow">
      <div class="p-4 text-2xl">
        {{ pack.name }}
      </div>
      <div class="grow"></div>
      <div class="flex flex-row gap-2 h-8">
        <button class="bg-grey rounded hover:bg-grey-dark">
          <VueFeather type="chevron-left" size="2rem" v-if="showPrevious"
                      @click="currentIndex--" class="cursor-pointer"/>
        </button>
        <button class="bg-grey rounded hover:bg-grey-dark">
          <VueFeather type="chevron-right" size="2rem" class="cursor-pointer" v-if="showNext"
                      @click="currentIndex++"/>
        </button>
        <button class="bg-yellow rounded hover:bg-yellow-dark">
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
const updatedAnswers = {}
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

const updatePack = async () => {
  pack.value = await api.get(`/api/${type}/pack/${id}`)
}

onMounted(updatePack)

const updateAnswer = (questionId, value, comment) => {
  updatedAnswers[questionId] = {value, comment}
}

</script>
