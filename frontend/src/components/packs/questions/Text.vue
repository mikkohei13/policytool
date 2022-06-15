<template>
  <div class="flex flex-col">
    <textarea v-model="value" :id="inputId" class="border rounded p-2" placeholder="Answer"></textarea>
    <textarea v-model="comment" :id="commentId" placeholder="Comments" class="mt-8"></textarea>
  </div>
</template>

<script setup>
import {ref, watch} from 'vue'

const emit = defineEmits(['updateAnswer'])
const {question} = defineProps(['question'])

const value = ref(question.answer ? question.answer.value : null)
const comment = ref(question.answer ? question.answer.comment : null)

const inputId = `text-${question.id}`
const commentId = `text-comment-${question.id}`

watch([value, comment], ([newValue, newComment]) => {
  emit('updateAnswer', question.id, newValue, newComment)
})
</script>
