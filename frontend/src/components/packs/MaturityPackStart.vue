<template>
  <div class="pt-4 text-4xl">
    {{ pack.name }}
  </div>
  <div class="pt-4 text-xl">
    Policy component scope
  </div>
  <div class="pt-2 prose max-w-none">
    {{ pack.scope }}
  </div>
</template>

<script setup>

const {pack} = defineProps(['pack'])


</script>
