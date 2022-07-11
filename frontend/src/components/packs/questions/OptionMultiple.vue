<template>
  <div class="flex flex-col">
    <div v-for="(option, index) in question.options" class="flex flex-row items-center gap-2">
      <input type="checkbox" :id="index" :value="option" v-model="value" class="cursor-pointer" />
      <label :for="index" class="cursor-pointer">{{ option }}</label>
    </div>
    <textarea v-if="allowComment" v-model="comment" placeholder="Comments" class="mt-8"></textarea>
  </div>
</template>

<script setup>
import {ref, watch} from 'vue'

const emit = defineEmits(['updateAnswer'])
const {question, allowComment} = defineProps({
  'question': {type: Array},
  'allowComment': {type: Boolean, default: true}
})

const value = ref(question.answer ? question.answer.value : [])
const comment = ref(question.answer ? question.answer.comment : null)

watch([value, comment], ([newValue, newComment]) => {
  emit('updateAnswer', question.id, newValue, newComment)
})
</script>
