<template>
  <!-- TODO: this needs to be made responsive as it's horrible on a small screen -->
  <div class="flex flex-col">
    <div class="flex flex-row gap-4 bg-grey-light">
      <div class="pr-4 w-1/5 bg-white">{{ periods[question.period] }}</div>
      <div v-for="(score, label) in scores"
           class="flex flex-col items-center gap-2 w-1/4 py-3">
        <label :for="generateScoreId(score)" class="text-center">{{ label }}</label>
        <div class="grow"></div>
        <input v-model="value" type="radio" :id="generateScoreId(score)" :name="group"
               :value="score" class="w-5 h-5">
      </div>
    </div>
    <textarea v-model="comment" :id="commentId" placeholder="Comments" class="mt-8"></textarea>
  </div>
</template>

<script setup>
import {ref, watch} from 'vue'

const emit = defineEmits(['updateAnswer'])
const {question} = defineProps(['question'])

const value = ref(question.answer ? Number(question.answer.value) : null)
const comment = ref(question.answer ? question.answer.comment : null)

const scores = {
  'Disagree': 0,
  'Partly agree / true for particular individuals or teams': 1,
  'Mostly agree / true for most teams': 2,
  'Completely agree': 3
}
const periods = {
  'current': 'Current state:',
  'future_12': 'Aim in 12 months:',
}

const generateScoreId = (score) => `maturity-${score}-${question.id}`

const group = `maturity-${question.id}`
const commentId = `maturity-comment-${question.id}`

watch([value, comment], ([newValue, newComment]) => {
  emit('updateAnswer', question.id, newValue, newComment)
})
</script>
