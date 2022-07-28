<template>
  <div v-if="field in errors">
    <p class="text-status-denied">
      Error: {{ errors[field][0] }}
    </p>
  </div>
</template>

<script setup>

const {errors, field} = defineProps(['errors', 'field'])

</script>
