<template>
  <div class="flex flex-col">
    <div class="flex flex-row items-center gap-2">
      <input v-model="value" type="radio" :id="yesId" :name="group" value="yes">
      <label :for="yesId">Yes</label>
    </div>
    <div class="flex flex-row items-center gap-2">
      <input v-model="value" type="radio" :id="noId" :name="group" value="no">
      <label :for="noId">No</label>
    </div>
    <div class="flex flex-row items-center gap-2">
      <input v-model="value" type="radio" :id="notSpecifiedId" :name="group" value="notSpecified">
      <label :for="notSpecifiedId">Not specified</label>
    </div>
    <textarea v-model="comment" :id="commentId" placeholder="Comments" class="mt-8"></textarea>
  </div>
</template>

<script setup>
import {ref, watch} from 'vue'

const emit = defineEmits(['updateAnswer'])
const {question} = defineProps(['question'])

const value = ref(question.answer ? question.answer.value : null)
const comment = ref(question.answer ? question.answer.comment : null)

const group = `radio-${question.id}`
const commentId = `comment-${question.id}`
const yesId = `yes-${question.id}`
const noId = `no-${question.id}`
const notSpecifiedId = `notSpecified-${question.id}`

watch([value, comment], ([newValue, newComment]) => {
  emit('updateAnswer', question.id, newValue, newComment)
})
</script>
