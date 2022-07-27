<template>
  <div class="pt-4 text-4xl">
    {{ pack.name }}
  </div>
  <div v-if="!!pack.description" class="pt-2 italic text-lg">
    {{ pack.description }}
  </div>
  <div class="prose max-w-none flex flex-col pt-5">
    <div>
      Welcome to the DiSSCo digital maturity self-assessment. This tool is intended for current or
      prospective DiSSCo partners, and can be used to self-assess and to set your own areas for
      improvement whether you represent a team, organisation or national DiSSCo node.
    </div>
    <div>
      To be successful, the digital transformation envisaged by DiSSCo needs partners to contribute
      content, infrastructure, expertise and leadership. DiSSCo Prepare covers five key dimensions
      of readiness: scientific; technical; data; financial and organisational. Digital maturity is
      therefore a broad concept, and this tool covers a wide variety of areas that contribute to an
      organisation’s flexibility and responsiveness to change, as well as the specific resources and
      skills you may need for digitisation, infrastructure and data mobilisation.
    </div>
    <div>
      DiSSCo includes a wide range of different types and sizes of organisations, with different
      needs and approaches - for example in some areas particular skills may be outsourced or
      contracted, or may not be needed at all e.g. if they can be sourced elsewhere in the DiSSCo
      consortium. So this tool allows you to specify which areas or questions are and aren’t
      relevant to your assessment, and to set your own priorities by choosing which areas to target
      for improvement.
    </div>
    <div class="pt-4">
      <div v-if="!!pack.finished_at">
        This assessment has been marked as complete as of {{ pack.finished_at }}.
      </div>
      <div v-else>
        There are {{ pack.questions.length }} questions as part of this self-assessment area.
      </div>
    </div>
    <div class="pt-4">
      <div class="text-lg">Instructions</div>
      <ul>
        <li>Use the arrows to select the previous and next questions</li>
        <li>You may skip questions</li>
        <li>Your responses are automatically saved as you navigate through the questions</li>
        <li>Click the home button at any time to go back to this team's self-assessment home page
        </li>
      </ul>
    </div>

  </div>
</template>

<script setup>

const {pack} = defineProps(['pack'])


</script>
