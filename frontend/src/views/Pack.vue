<template>
  <p class="text-white">
    {{ id }}
  </p>
</template>

<script setup>
const {id} = defineProps(['id'])
</script>
