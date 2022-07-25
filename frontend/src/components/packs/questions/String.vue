<template>
  <div class="flex flex-col">
    <input v-model="value" :id="inputId" class="border rounded p-2" placeholder="Answer">
    <textarea v-if="allowComment" v-model="comment" :id="commentId" placeholder="Comments"
              class="mt-8"></textarea>
  </div>
</template>

<script setup>
import {ref, watch} from 'vue'

const emit = defineEmits(['updateAnswer'])
const {question, allowComment} = defineProps({
  'question': {type: Object},
  'allowComment': {type: Boolean, default: true}
})

const value = ref(question.answer ? question.answer.value : null)
const comment = ref(question.answer ? question.answer.comment : null)

const inputId = `string-${question.id}`
const commentId = `string-comment-${question.id}`

watch([value, comment], ([newValue, newComment]) => {
  emit('updateAnswer', question.id, newValue, newComment)
})
</script>
