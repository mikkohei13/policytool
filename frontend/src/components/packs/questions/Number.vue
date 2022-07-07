<template>
  <div class="flex flex-col">
    <input v-model="value" type="number" :id="inputId" class="w-full sm:w-40">
    <textarea v-if="allowComment" v-model="comment" :id="commentId" placeholder="Comments"
              class="mt-8"></textarea>
  </div>
</template>

<script setup>
import {ref, watch} from 'vue'

const emit = defineEmits(['updateAnswer'])
const {question, allowComment} = defineProps({
  'question': {type: Array},
  'allowComment': {type: Boolean, default: true}
})

const value = ref(question.answer ? Number(question.answer.value) : null)
const comment = ref(question.answer ? question.answer.comment : null)

const inputId = `number-${question.id}`
const commentId = `number-comment-${question.id}`

watch([value, comment], ([newValue, newComment]) => {
  emit('updateAnswer', question.id, newValue, newComment)
})
</script>
