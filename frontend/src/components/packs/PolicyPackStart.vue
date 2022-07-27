<template>
  <div class="pt-4 text-4xl">
    {{ pack.name }}
  </div>
  <div class="pt-2 italic text-lg">
    {{ pack.scope }}
  </div>

  <div class="pt-4 prose max-w-none flex flex-col">
    <div>
      This policy area is part of the wider <span class="italic">{{ pack.category.name }}</span>
      category.
    </div>
    <div v-if="!!pack.finished_at">
      This assessment has been marked as complete as of {{ pack.finished_at }}.
    </div>
    <div v-else>
      There are {{ pack.questions.length }} questions as part of the assessment for this policy
      area.
    </div>
    <div class="pt-4">
      <div class="text-lg">Instructions</div>
      <ul>
        <li>Use the arrows to select the previous and next questions</li>
        <li>
          You may skip questions, though if these questions are part of the service alignment
          assessment, the lack of response may be marked as inadequate for policy alignment
        </li>
        <li>Your responses are automatically saved as you navigate through the questions</li>
        <li>Click the home button at any time to go back to your institution's policy home page. Any
          changes made prior to navigating away will be saved automatically</li>
      </ul>
    </div>
  </div>

</template>

<script setup>

const {pack} = defineProps(['pack'])
const answered = pack.questions.filter(question => !!question.answer).length

</script>
