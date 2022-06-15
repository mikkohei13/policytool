<template>
  <div class="flex flex-col">
    <select v-model="value" :id="inputId">
      <option disabled value="">Please select one</option>
      <option v-for="option in question.options">{{ option }}</option>
    </select>
    <textarea v-model="comment" :id="commentId" placeholder="Comments" class="mt-8"></textarea>
  </div>
</template>

<script setup>
import {ref, watch} from 'vue'

const emit = defineEmits(['updateAnswer'])
const {question} = defineProps(['question'])

const value = ref(question.answer ? question.answer.value : null)
const comment = ref(question.answer ? question.answer.comment : null)

const inputId = `optionSingle-${question.id}`
const commentId = `optionSingle-comment-${question.id}`

watch([value, comment], ([newValue, newComment]) => {
  emit('updateAnswer', question.id, newValue, newComment)
})
</script>
